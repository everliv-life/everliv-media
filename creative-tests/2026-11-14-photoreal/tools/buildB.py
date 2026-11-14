import sys; sys.path.insert(0,'/home/claude/serum')
import numpy as np, transfer
from relight import relight, hard_shadow, scene_noise
from PIL import Image
KEY=tuple(float(v) for v in sys.argv[1].split(',')); SH=tuple(float(v) for v in sys.argv[2].split(','))
FP=float(sys.argv[3]); RIM=float(sys.argv[4]); OUT=sys.argv[5]
sc=Image.open('/home/claude/serum/B0.png').convert('RGB')
cut='/home/claude/everliv-media-repo/library/peptide-eye-serum/peptide-eye-serum--front-cutout.png'
base,bb=transfer.composite(sc,cut,(318,516,438,1002),486,seam_rows=[(626,642)],flat=True,arc=9,cap_from=None,contact=0.75)
mask=transfer.LAST_MASK
sh=hard_shadow(base,(312,998),(444,998),(250,26),softness=4,alpha=0.5,col=(0.60,0.50,0.44),taper=0.8)
m=mask[...,None]; o=np.asarray(sh).astype(float)*(1-m)+np.asarray(base).astype(float)*m
out=Image.fromarray(o.astype(np.uint8))
gn=scene_noise(sc,(100,1100,600,1300))
res=relight(out,mask,bb,key_col=KEY,shadow_col=SH,fall_pow=FP,spec_pos=0.16,spec_w=0.05,spec_amt=0.12,rim=RIM,top_tame=0.2,grain_match=gn*0.8)
# cap top: the real cap top is plain white; draw it as the visible ellipse in the scene's light
x0,y0,x1,y1=bb
s=np.asarray(sc).astype(float); capc=np.array([240.,226.,208.])
from PIL import ImageDraw, ImageFilter
r=res.convert('RGBA'); w=x1-x0; eh=18
disc=Image.new('RGBA',(w,eh),tuple(int(c) for c in capc)+(0,))
dm=Image.new('L',(w,eh),0); ImageDraw.Draw(dm).ellipse((1,0,w-2,eh-1),fill=255)
# subtle gradient on disc: lit left
g=np.linspace(1.03,0.86,w)[None,:,None]; da=np.ones((eh,w,3))*capc*g
disc=Image.fromarray(np.dstack([np.clip(da,0,255),np.asarray(dm.filter(ImageFilter.GaussianBlur(0.8)))]).astype(np.uint8),'RGBA')
r.alpha_composite(disc,(x0,y0-eh//2))
r=r.convert('RGB'); r.save(OUT); r.crop((230,440,560,1060)).save(OUT.replace('.png','-crop.png'))
print(capc)
