import sys; sys.path.insert(0,'/home/claude/serum')
import numpy as np, transfer
from relight import relight, hard_shadow, scene_noise
from PIL import Image, ImageFilter
KEY=tuple(float(v) for v in sys.argv[1].split(',')); SH=tuple(float(v) for v in sys.argv[2].split(','))
FP=float(sys.argv[3]); DAP=float(sys.argv[4]); OUT=sys.argv[5]
sc=Image.open('/home/claude/serum/A1.png').convert('RGB'); s=np.asarray(sc).astype(float)
cut='/home/claude/everliv-media-repo/library/peptide-eye-serum/peptide-eye-serum--front-cutout.png'
base,bb=transfer.composite(sc,cut,(486,372,637,1014),642,seam_rows=[(516,530)],flat=True,contact=1.0)
mask=transfer.LAST_MASK
sh=hard_shadow(base,(474,1012),(650,1012),(300,-46),softness=5,alpha=0.5,col=(0.62,0.50,0.40))
m=mask[...,None]; o=np.asarray(sh).astype(float)*(1-m)+np.asarray(base).astype(float)*m
out=Image.fromarray(o.astype(np.uint8))
x0,y0,x1,y1=bb
wall=s[y0:y1, x0-200:x0-200+(x1-x0)].mean(-1)
p10,p90=np.percentile(wall,10),np.percentile(wall,90)
d=np.clip((p90-wall)/(p90-p10),0,1)
d=np.asarray(Image.fromarray((d*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(float)/255
fade=np.clip(1-(np.arange(y1-y0)/(y1-y0)-0.40)/0.2,0,1)[:,None]
D=np.zeros(mask.shape,np.float32); D[y0:y1,x0:x1]=d*fade
gn=scene_noise(sc,(700,450,1000,700))
res=relight(out,mask,bb,key_col=KEY,shadow_col=SH,fall_pow=FP,spec_pos=0.10,spec_w=0.045,spec_amt=0.20,term=0.66,term_w=0.05,dapple=D,dapple_amt=DAP,top_tame=0.3,grain_match=2.6,soften=0.7)
res.save(OUT); res.crop((380,300,800,1100)).save(OUT.replace('.png','-crop.png'))
