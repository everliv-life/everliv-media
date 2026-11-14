import sys; sys.path.insert(0,'/home/claude/serum')
import numpy as np, transfer
from relight import relight, hard_shadow
from PIL import Image, ImageFilter, ImageEnhance
CUT='/home/claude/everliv-media-repo/library/peptide-eye-serum/peptide-eye-serum--front-cutout.png'
OW,OH=int(sys.argv[1]),int(sys.argv[2]); OUT=sys.argv[3]
crop=(196,220,928,1135); s=OW/(crop[2]-crop[0])
# 1) scene first: crop + upscale to the OUTPUT size (the scene may soften; the product will not)
sc=Image.open('/home/claude/serum/A1.png').convert('RGB').crop(crop).resize((OW,OH),Image.LANCZOS)
T=lambda x,y:((x-crop[0])*s,(y-crop[1])*s)
bx0,by0=T(486,372); bx1,by1=T(637,1014); box=tuple(int(round(v)) for v in (bx0,by0,bx1,by1))
seam=[tuple(int(round(T(0,v)[1])) for v in (516,530))]
# 2) product scaled ONCE from the authentic source straight to its final pixel size; no blur
base,bb=transfer.composite(sc,CUT,box,int(round(642*s)),seam_rows=seam,flat=True,contact=1.0,grain=0,soften=0)
mask=transfer.LAST_MASK
L=lambda v:int(round(v*s))
sh=hard_shadow(base,(bb[0]+L(4),bb[3]),(bb[2]-L(4),bb[3]),(L(300),-L(46)),softness=L(5),alpha=0.5,col=(0.62,0.50,0.40))
m=mask[...,None]; o=np.asarray(sh).astype(float)*(1-m)+np.asarray(base).astype(float)*m
out=Image.fromarray(o.astype(np.uint8))
# 3) leaf shadow continued from the wall onto the cap
x0,y0,x1,y1=bb; sa=np.asarray(sc).astype(float)
wall=sa[y0:y1, x0-L(200):x0-L(200)+(x1-x0)].mean(-1)
p10,p90=np.percentile(wall,10),np.percentile(wall,90)
d=np.clip((p90-wall)/(p90-p10),0,1)
d=np.asarray(Image.fromarray((d*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3*s))).astype(float)/255
fade=np.clip(1-(np.arange(y1-y0)/(y1-y0)-0.26)/0.12,0,1)[:,None]
D=np.zeros(mask.shape,np.float32); D[y0:y1,x0:x1]=d*fade
# 4) relight (light only: colour, terminator, specular) - no softening; light grain only
res=relight(out,mask,bb,key_col=(256,248,236),shadow_col=(150,134,118),fall_pow=1.15,spec_pos=0.17,spec_w=0.05,spec_amt=0.24,term=0.56,term_w=0.08,dapple=D,dapple_amt=0.26,top_tame=0.3,grain_match=1.0,soften=0)
# 5) global grade toward warm beige (applies equally to scene and product, like a camera)
res=ImageEnhance.Color(res).enhance(0.88)
res.save(OUT); print(bb)
