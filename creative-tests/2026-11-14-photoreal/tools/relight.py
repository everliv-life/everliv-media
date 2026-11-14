"""Photographic relight pass applied only inside the product mask (label geometry untouched)."""
import numpy as np
from PIL import Image, ImageFilter, ImageDraw


def relight(img, mask, bbox, key_col, shadow_col, lit_side='left', key_gain=1.0, fall_pow=1.6,
            spec_pos=0.18, spec_w=0.05, spec_amt=0.18, rim=0.0, dapple=None, dapple_amt=0.0,
            top_tame=0.0, grain_match=None, term=None, term_w=0.06, soften=0.0):
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    x0, y0, x1, y1 = bbox
    H, W = a.shape[:2]
    xx = np.zeros((H, W), np.float32)
    xr = (np.arange(W) - x0) / max(1, (x1 - x0))
    xx[:] = np.clip(xr, 0, 1)[None, :]
    if lit_side != 'left':
        xx = 1 - xx
    # cylinder light: key colour on the lit side -> shadow colour, cosine falloff with a harder terminator
    t = (0.5 - 0.5 * np.cos(np.pi * xx)) ** (1 / fall_pow)
    if term is not None:
        sig = 1 / (1 + np.exp(-(xx - term) / term_w))
        t = np.clip(0.35 * t + 0.65 * sig, 0, 1)
    kc, sc = np.array(key_col) / 255, np.array(shadow_col) / 255
    tint = kc[None, None] * (1 - t[..., None]) + sc[None, None] * t[..., None]
    # normalise: tint relative to neutral, applied to existing pixels
    lum = a.mean(-1, keepdims=True)
    base = a / 255
    rel = tint * key_gain
    out = base * rel
    # specular streak (warm white), plus optional rim on the lit edge
    spec = np.exp(-((xx - spec_pos) / spec_w) ** 2) * spec_amt
    out = out + spec[..., None] * kc[None, None]
    if rim:
        r = np.exp(-((xx - 0.015) / 0.02) ** 2) * rim
        out = out + r[..., None] * kc[None, None]
    if dapple is not None:
        out = out * (1 - dapple_amt * dapple[..., None])
    if top_tame:
        yy = (np.arange(H) - y0)[:, None].astype(np.float32)
        out = out * (1 - top_tame * np.exp(-(yy / 3.0) ** 2))[..., None]
    out = np.clip(out, 0, 1) * 255
    if grain_match:
        out = out + np.random.default_rng(11).normal(0, grain_match, (H, W, 1))
    if soften:
        o_img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(soften))
        out = np.asarray(o_img).astype(np.float32)
        if grain_match:
            out = out + np.random.default_rng(12).normal(0, grain_match, (H, W, 1))
    m = mask[..., None]
    res = a * (1 - m) + out * m
    return Image.fromarray(np.clip(res, 0, 255).astype(np.uint8))


def hard_shadow(img, base_l, base_r, vec, softness=3, alpha=0.55, col=(0.55, 0.45, 0.38), taper=0.6):
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    H, W = a.shape[:2]
    m = Image.new('L', (W, H), 0)
    (lx, ly), (rx, ry) = base_l, base_r
    dx, dy = vec
    cx = (lx + rx) / 2
    hw = (rx - lx) / 2 * taper
    poly = [(lx, ly), (rx, ry), (cx + dx + hw, ry + dy), (cx + dx - hw, ly + dy)]
    ImageDraw.Draw(m).polygon(poly, fill=255)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(softness))).astype(np.float32) / 255
    # fade along length
    a2 = a * (1 - (m * alpha)[..., None] * (1 - np.array(col)))
    return Image.fromarray(np.clip(a2, 0, 255).astype(np.uint8))


def scene_noise(img, box):
    a = np.asarray(img.convert('L')).astype(np.float32)
    x0, y0, x1, y1 = box
    r = a[y0:y1, x0:x1]
    hp = r - np.asarray(Image.fromarray(r.astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32)
    return float(hp.std())
