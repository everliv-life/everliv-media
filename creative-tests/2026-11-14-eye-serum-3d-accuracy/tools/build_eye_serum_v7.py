"""
EverLiv Peptide Eye Serum — PROVISIONAL 3D packaging model + neutral render (internal accuracy test).

ALL DIMENSIONS ARE UNVERIFIED: estimated from the supplier front render
(peptide-eye-serum--front.jpg, 2048 px), 1 model unit = 1000 render px.
Label artwork: label_extracted.png = exact pixel crop (174,344)-(1874,1704) of the supplier
presentation image peptide-eye-serum--flat-label-ingredients.png. Not resized, recoloured, redrawn
or edited; mapped at uniform scale (no stretch: identical horizontal and vertical scale).

Measured / derived (front render px):
  body width 432 -> radius 0.216 ; overall height y250..y1800 -> 1.550
  cap: y250..y704 ; collar band y704..y776 (width ~437) ; label y777..y1741 ; unlabelled base y1741..y1800
  label scale 0.709 front px per label px (v2) -> label 1.205 x 0.964 units
  label arc = 1.205 / r -> ~319 deg ; label x=884 (of 1700) faces camera
UNVERIFIED materials: matte/satin white plastic cap & body, matte white paper label.
"""
import bpy, math, sys, os

LS = float(os.environ.get('LS','1.0')); RES = int(os.environ.get('RES','2048')); SAMP = int(os.environ.get('SAMP','256'))
OUT = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else '/home/claude/es3d/render'
LABEL = '/home/claude/es3d/label_extracted.png'
LW, LH = 1700, 1360
# ---- v6: camera re-solved from the supplier render's top AND base ellipses (cap top seen almost edge-on,
# base front rim sagging ~30 px). Camera at height CAM_H, distance D, aimed at (0,0,AIM_Z); focal F_PX.
import math as _m
R = 0.216; D = 11.0; CAM_H = 1.70
def _proj(x, y, z, aim_z, F):
    # camera looks from (0,-D,CAM_H) toward (0,0,aim_z); returns image row (2048 frame, y down)
    fwd = (0.0, D, aim_z - CAM_H); n = _m.sqrt(sum(c * c for c in fwd)); fwd = tuple(c / n for c in fwd)
    up = (0.0, -fwd[2], fwd[1])                                   # perpendicular to fwd in the y-z plane
    v = (x, y + D, z - CAM_H); depth = sum(a * b for a, b in zip(v, fwd)); vy = sum(a * b for a, b in zip(v, up))
    return 1024 - F * vy / depth, depth
def _solve_row(target, aim_z, F, yy):                             # z on surface y=yy whose image row = target
    lo, hi = -0.5, 2.5
    for _ in range(80):
        mid = (lo + hi) / 2
        if _proj(0, yy, mid, aim_z, F)[0] > target: lo = mid
        else: hi = mid
    return (lo + hi) / 2
F_PX = 432 * _m.sqrt(D * D + (CAM_H - 0.75) ** 2) / (2 * R)       # silhouette width 432 px near mid-height
lo, hi = -1.0, 3.0                                                 # aim so the base front rim lands on row 1800
for _ in range(80):
    mid = (lo + hi) / 2
    if _proj(0, -R, 0.0, mid, F_PX)[0] > 1800: hi = mid          # aiming higher pushes the base down the frame
    else: lo = mid
AIM_Z = (lo + hi) / 2
zf = lambda y: _solve_row(y, AIM_Z, F_PX, -R)                      # front-surface feature at image row y
Z_BASE_TOP, Z_LAB_TOP = zf(1741), zf(777)
Z_SEAM2, Z_CAP0 = zf(720), zf(695)
Z_TOP = _solve_row(250, AIM_Z, F_PX, +R)                            # silhouette top = BACK rim of cap top (camera above)
K = (Z_LAB_TOP - Z_BASE_TOP) / LH
R_LAB = R + 0.0006
FRONT_X = 884.0
ZC = AIM_Z
print('v6 geometry: CAM_H %.3f D %.2f AIM %.4f |' % (CAM_H, D, AIM_Z), 'v6: ZC %.4f F_PX %.1f label z %.4f..%.4f  K %.6f  seam2 %.4f cap0 %.4f top %.4f' % (ZC, F_PX, Z_BASE_TOP, Z_LAB_TOP, K, Z_SEAM2, Z_CAP0, Z_TOP))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat(name, rgb, rough=0.45, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Roughness'].default_value = rough
    if 'Coat Weight' in b.inputs: b.inputs['Coat Weight'].default_value = coat
    return m

def srgb2lin(c): return ((c / 255 + 0.055) / 1.055) ** 2.4 if c / 255 > 0.04045 else c / 255 / 12.92
WHITE_PLASTIC = tuple(srgb2lin(v) for v in (246, 246, 246))   # UNVERIFIED colour/finish

def cyl(name, r, z0, z1, m, bevel=0.0, verts=256):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=z1 - z0, location=(0, 0, (z0 + z1) / 2))
    o = bpy.context.object; o.name = name; o.data.materials.append(m)
    bpy.ops.object.shade_smooth()
    if bevel:
        bm = o.modifiers.new('bevel', 'BEVEL'); bm.width = bevel; bm.segments = 12; bm.limit_method = 'ANGLE'
    return o

# v5 materials (UNVERIFIED finishes, read from supplier renders): glossy overcap, satin body
cap_gloss = mat('cap_gloss_white_UNVERIFIED', WHITE_PLASTIC, rough=0.12, coat=0.6)
body_satin = mat('body_satin_white_UNVERIFIED', WHITE_PLASTIC, rough=0.32, coat=0.1)
groove_m = mat('seam_line', tuple(srgb2lin(v) for v in (205, 205, 205)), rough=0.5)
cyl('body', R, 0.0, Z_CAP0, body_satin, bevel=0.016)
# seam lines: shallow inset rings at the cap edge (y695) and shoulder step (y720) — geometry per supplier render
for zc_ in (Z_CAP0, Z_SEAM2):
    cyl('seam', R + 0.0002, zc_ - 0.0009, zc_ + 0.0009, groove_m, verts=256)
cyl('cap', R, Z_CAP0 + 0.0009, Z_TOP, cap_gloss, bevel=0.032)   # v6: top corner radius measured from supplier silhouette inset (33 px @ y256, 8 px @ y270)
# ---- label: open cylinder shell, uniform-scale UV of the unaltered artwork
import bmesh
me = bpy.data.meshes.new('label'); bm = bmesh.new()
arc = LW * K / R_LAB
segs = 512
uv_layer = bm.loops.layers.uv.new()
cols = []
for i in range(segs + 1):
    u = i / segs                                   # 0..1 across label width
    s = u * LW - FRONT_X                           # label px from the camera-facing line
    th = s * K / R_LAB                             # angle (0 = facing camera at -Y)
    x, y = R_LAB * math.sin(th), -R_LAB * math.cos(th)
    cols.append((bm.verts.new((x, y, Z_BASE_TOP)), bm.verts.new((x, y, Z_LAB_TOP)), u))
for (a0, a1, u0), (b0, b1, u1) in zip(cols[:-1], cols[1:]):
    f = bm.faces.new((a0, b0, b1, a1))
    for lp, uv in zip(f.loops, ((u0, 0), (u1, 0), (u1, 1), (u0, 1))):
        lp[uv_layer].uv = uv
bm.to_mesh(me); bm.free()
lab = bpy.data.objects.new('label', me); sc.collection.objects.link(lab)
for p in me.polygons: p.use_smooth = True
lm = bpy.data.materials.new('label_artwork_UNALTERED'); lm.use_nodes = True
nt = lm.node_tree; b = nt.nodes['Principled BSDF']
tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = bpy.data.images.load(LABEL)
tex.image.colorspace_settings.name = 'sRGB'; tex.interpolation = 'Closest'   # v7: point sampling + supersampling (sharper type, no aliasing at 160 spp)
nt.links.new(tex.outputs['Color'], b.inputs['Base Color'])
b.inputs['Roughness'].default_value = 0.85         # matte uncoated paper label — UNVERIFIED (v4; v3 = 0.6)
if 'Specular IOR Level' in b.inputs: b.inputs['Specular IOR Level'].default_value = 0.2   # low sheen matte stock — UNVERIFIED
lab.data.materials.append(lm)
print('label arc deg', math.degrees(arc))

# ---- neutral studio: white seamless world + soft key/fill (supplier-render style)
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (1, 1, 1, 1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.55 * LS
def area(name, loc, size, power, rot):
    d = bpy.data.lights.new(name, 'AREA'); d.size = size; d.energy = power * LS
    o = bpy.data.objects.new(name, d); o.location = loc; o.rotation_euler = rot; sc.collection.objects.link(o)
area('key', (2.2, -2.6, 1.5), 2.5, 260, (math.radians(70), 0, math.radians(40)))
area('fill', (-2.4, -2.2, 1.2), 3.0, 140, (math.radians(75), 0, math.radians(-47)))
area('top', (0, 0, 3.4), 2.0, 60, (0, 0, 0))

# floor shadow catcher
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
fl = bpy.context.object; fl.is_shadow_catcher = True

# ---- camera: mid-height, long lens (near-orthographic like the supplier render)
cam_d = bpy.data.cameras.new('cam'); cam_d.sensor_fit = 'VERTICAL'; cam_d.sensor_height = 36; cam_d.sensor_width = 36
cam_d.lens = F_PX * 36 / 2048
cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam.location = (0, -D, CAM_H)
cam.rotation_euler = (_m.pi / 2 + _m.atan2(AIM_Z - CAM_H, D), 0, 0)
sc.render.resolution_x = sc.render.resolution_y = 2048
sc.render.resolution_percentage = int(100 * RES / 2048)
sc.render.engine = 'CYCLES'; sc.cycles.samples = SAMP; sc.cycles.use_denoising = False
sc.cycles.device = 'CPU'
sc.cycles.filter_width = 0.5          # v7: label sharpness 97% of supplier (p99-gradient) in crop test
sc.render.film_transparent = True
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
sc.view_settings.exposure = 0; sc.view_settings.gamma = 1
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.render.filepath = OUT + '.png'
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=OUT + '.blend')
print('done', OUT)
