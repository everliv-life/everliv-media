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
res=relight(base,mask,bb,key_col=(262,256,246),shadow_col=(214,204,194),fall_pow=1.3,spec_pos=0.12,spec_w=0.045,spec_amt=0.16,term=0.52,term_w=0.08,top_tame=0.15,grain_match=1.0,soften=0)
# restore the fingertips over the cap from the scene itself (skin pixels only)
a=np.asarray(res).astype(float); scn=np.asarray(sc).astype(float)
y0=max(0,bb[1]-T(60)); y1=bb[1]+int(0.07*(bb[3]-bb[1]))
reg=scn[y0:y1, bb[0]-T(10):bb[2]+T(10)]
skin=((reg[...,0]-reg[...,1])>45)&((reg[...,0]-reg[...,2])>60)&(reg[...,0]>90)
m=np.zeros(a.shape[:2],np.uint8); m[y0:y1, bb[0]-T(10):bb[2]+T(10)]=skin*255
m=np.asarray(Image.fromarray(m).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.8))).astype(float)/255
a=a*(1-m[...,None])+scn*m[...,None]
# soft shadow of the fingertips falling right/down onto the cap top (light from the left)
from PIL import ImageDraw
sk=np.zeros(a.shape[:2],np.uint8); sk[y0:y1, bb[0]-T(10):bb[2]+T(10)]=skin*255
ys,xs=np.where(sk>0)
if len(xs):
    fx0,fx1=xs.min(),xs.max()
    shm=Image.new('L',(a.shape[1],a.shape[0]),0)
    ImageDraw.Draw(shm).ellipse((fx0+T(14),bb[1]-T(2),fx1+T(26),bb[1]+T(34)),fill=255)
    shm=np.asarray(shm.filter(ImageFilter.GaussianBlur(T(9)))).astype(float)/255*0.32
    shm=shm*mask*(1-m)
    a=a*(1-shm[...,None]*np.array([0.45,0.55,0.65]))
res=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
res.save(OUT); print(bb)
