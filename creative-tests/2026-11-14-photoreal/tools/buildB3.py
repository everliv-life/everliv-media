import sys; sys.path.insert(0,'/home/claude/serum')
import numpy as np, transfer
from relight import relight
from PIL import Image, ImageFilter, ImageEnhance
CUT='/home/claude/everliv-media-repo/library/peptide-eye-serum/peptide-eye-serum--front-cutout.png'
OW,OH=int(sys.argv[1]),int(sys.argv[2]); OUT=sys.argv[3]
src=Image.open('/home/claude/serum/B3_0.png').convert('RGB'); s=OW/src.width
sc=src.resize((OW,OH),Image.LANCZOS)
T=lambda v:int(round(v*s))
box=(T(448),T(423),T(633),T(1129)); h=box[3]-box[1]
# real bottle fitted to the stand-in's height (aspect preserved); light transferred from the stand-in
base,bb=transfer.composite(sc,CUT,box,h,seam_rows=[(T(640),T(656))],white_ref=252,contact=0.5,grain=0,soften=0)
mask=transfer.LAST_MASK
# gentle extra warmth/terminator so the bottle matches the amber sun (light only, no blur)
res=relight(base,mask,bb,key_col=(262,246,222),shadow_col=(250,232,206),fall_pow=1.3,spec_pos=0.08,spec_w=0.04,spec_amt=0.08,top_tame=0.15,grain_match=1.0,soften=0)
# restore the fingertips over the cap from the scene itself (skin pixels only)
a=np.asarray(res).astype(float); scn=np.asarray(sc).astype(float)
y0=max(0,bb[1]-T(60)); y1=bb[1]+int(0.07*(bb[3]-bb[1]))
reg=scn[y0:y1, bb[0]-T(10):bb[2]+T(10)]
skin=((reg[...,0]-reg[...,1])>45)&((reg[...,0]-reg[...,2])>60)&(reg[...,0]>90)
m=np.zeros(a.shape[:2],np.uint8); m[y0:y1, bb[0]-T(10):bb[2]+T(10)]=skin*255
m=np.asarray(Image.fromarray(m).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.8))).astype(float)/255
a=a*(1-m[...,None])+scn*m[...,None]
res=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
res.save(OUT); print(bb)
