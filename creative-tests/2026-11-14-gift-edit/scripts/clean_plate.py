"""Remove dark residue specks the generator left around the removed stand-in (scene plate only; product untouched).
Usage: clean_plate.py plate.jpg standin_mask.npy out.png [ring_px=30] [thresh=10]"""
import sys, numpy as np, cv2
from PIL import Image
p, mp, out = sys.argv[1:4]; ring = int(sys.argv[4]) if len(sys.argv) > 4 else 30; th = float(sys.argv[5]) if len(sys.argv) > 5 else 10
P = np.asarray(Image.open(p).convert('RGB')); M = np.load(mp).astype(np.uint8)
band = cv2.dilate(M, np.ones((2*ring+1, 2*ring+1), np.uint8)) - cv2.erode(M, np.ones((2*ring+1, 2*ring+1), np.uint8))
L = P.mean(-1).astype(np.float32); bl = cv2.medianBlur(L.astype(np.uint8), 21).astype(np.float32)
dip = ((L - bl) < -th) & (band > 0)
ymax = int(sys.argv[6]) if len(sys.argv) > 6 else P.shape[0]     # optional: leave the surface below this row untouched
dip[ymax:] = False
dip = cv2.morphologyEx(dip.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
dip = cv2.dilate(dip, np.ones((5, 5), np.uint8))
fixed = cv2.inpaint(P, dip, 6, cv2.INPAINT_TELEA)
Image.fromarray(fixed).save(out); print('inpainted px', int(dip.sum()))
