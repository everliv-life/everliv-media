import sys; sys.path.insert(0,'/home/claude/serum')
import numpy as np, transfer
from relight import relight, hard_shadow
from PIL import Image
KEY=tuple(float(v) for v in sys.argv[1].split(',')); SH=tuple(float(v) for v in sys.argv[2].split(','))
TERM=float(sys.argv[3]); OUT=sys.argv[4]
sc=Image.open('/home/claude/serum/B2_0.png').convert('RGB')
cut='/home/claude/everliv-media-repo/library/peptide-eye-serum/peptide-eye-serum--front-cutout.png'
base,bb=transfer.composite(sc,cut,(298,563,406,933),383,seam_rows=[(684,696)],flat=True,contact=0.85,arc=4,grain=0)
mask=transfer.LAST_MASK
# long sharp cast shadow parallel to the window-mullion shadows on the counter (toward the right)
sh=hard_shadow(base,(300,931),(404,931),(520,22),softness=3,alpha=0.62,col=(0.55,0.42,0.30),taper=0.75)
m=mask[...,None]; o=np.asarray(sh).astype(float)*(1-m)+np.asarray(base).astype(float)*m
out=Image.fromarray(o.astype(np.uint8))
res=relight(out,mask,bb,key_col=KEY,shadow_col=SH,fall_pow=1.2,spec_pos=0.07,spec_w=0.035,spec_amt=0.22,rim=0.10,term=TERM,term_w=0.045,top_tame=0.25,grain_match=2.6,soften=0.4)
res.save(OUT)
# push in ~1.25x so the label holds at feed size; keep 4:5
c=res.crop((80,330,980,1455)).resize((1080,1350),Image.LANCZOS); c.save(OUT.replace('.png','-final.png'))
c.resize((540,675)).save(OUT.replace('.png','-small.jpg'))
