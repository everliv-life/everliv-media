import sys; sys.path.insert(0,'/home/claude/serum')
import numpy as np, cv2, transfer
from relight import relight
from PIL import Image, ImageFilter, ImageDraw
CUT='/home/claude/everliv-media-repo/library/peptide-eye-serum/peptide-eye-serum--front-cutout.png'
OW,OH=int(sys.argv[1]),int(sys.argv[2]); OUT=sys.argv[3]; SHRINK=float(sys.argv[4]) if len(sys.argv)>4 else 0.88
src=cv2.imread('/home/claude/serum/B3_0.png'); H,W=src.shape[:2]
M=np.load('/home/claude/serum/hand_mask.npy').astype(np.uint8)
# geometry (native px). Previous approved composite: real bottle 706 px tall on base y=1129, centred x=540.5
base_y=1129; cx=540.5; h_old=706; h_new=int(round(h_old*SHRINK)); w_new=h_new*436/1547
d=h_old-h_new                                   # how far the cap top drops -> how far the hand moves
nb=(cx-w_new/2, base_y-h_new, cx+w_new/2, base_y)
# 1) stand-in region (generated blank bottle incl. top edge) and moved hand
standin=np.zeros((H,W),np.uint8); cv2.rectangle(standin,(446,418),(635,base_y-6),1,-1)
Ms=np.zeros_like(M); Ms[d:,:]=M[:-d,:]
newb=np.zeros((H,W),np.uint8); cv2.rectangle(newb,(int(nb[0])+2,int(nb[1])+2),(int(nb[2])-2,base_y),1,-1)
# displacement field: hand moves down by d; the sleeve stretches (0 at the frame top -> d lower down)
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
wx=np.clip((xx-880)/120,0,1)                       # 0 = hand side, 1 = sleeve side
dy=d*(1-wx)+d*wx*np.clip(yy/320,0,1)
mapx=xx; mapy=yy-dy                                # output(y) samples input(y-dy)
hand=cv2.remap(src,mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
Ms=cv2.remap(M.astype(np.float32),mapx,mapy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT,borderValue=0)
Ms=(Ms>0.5).astype(np.uint8)
# clean plate: inpaint the WHOLE hand + stand-in area from pure background edges
hole=cv2.dilate(((M|standin)==1).astype(np.uint8),np.ones((7,7),np.uint8)); hole[base_y-4:,:]=0
plate=cv2.inpaint(src,hole,15,cv2.INPAINT_TELEA)
blur=cv2.GaussianBlur(plate,(0,0),3); hm=(cv2.GaussianBlur(hole.astype(np.float32),(0,0),1.5)*hole)[...,None]
plate=(plate*(1-hm)+blur*hm).astype(np.uint8)
# texture-preserving fill for the thin stand-in slivers beside the smaller bottle: mirror the
# neighbouring background columns (keeps counter/wall grain instead of smearing it)
L0,L1=444,int(nb[0])+3; R0,R1=int(nb[2])-3,638
for y in range(int(nb[1])-2,min(H,base_y+70)):
    wl=L1-L0; plate[y,L0:L1]=src[y,L0-wl:L0][::-1]
    wr=R1-R0; plate[y,R0:R1]=src[y,R1:R1+wr][::-1]
# feather the sliver seams (3 px) so no straight edge shows
for xs_ in (L0,L1,R0,R1):
    seg=plate[int(nb[1])-2:min(H,base_y+70), xs_-3:xs_+3].astype(np.float32)
    plate[int(nb[1])-2:min(H,base_y+70), xs_-3:xs_+3]=cv2.GaussianBlur(seg,(0,0),1.2).astype(np.uint8)
am=cv2.GaussianBlur(Ms.astype(np.float32),(0,0),0.8)[...,None]
plate=(plate*(1-am)+hand*am).astype(np.uint8)
edited=Image.fromarray(plate[...,::-1])
orig=Image.fromarray(src[...,::-1])
# 3) everything to output resolution, then the authentic product at its final pixel size
s=OW/W; T=lambda v:int(round(v*s))
E=edited.resize((OW,OH),Image.LANCZOS); O=orig.resize((OW,OH),Image.LANCZOS)
box=(T(nb[0]),T(nb[1]),T(nb[2]),T(base_y))
prodimg,bb=transfer.composite(O,CUT,box,box[3]-box[1],seam_rows=[(T(640),T(656))],white_ref=252,contact=0,grain=0,soften=0)
pm=transfer.LAST_MASK
P=np.asarray(prodimg).astype(float); e=np.asarray(E).astype(float)
# contact + slightly shortened cast shadow for the smaller bottle on the edited plate
cs=Image.new('L',(OW,OH),0); ImageDraw.Draw(cs).ellipse((bb[0]-T(2),bb[3]-T(9),bb[2]+T(2),bb[3]+T(5)),fill=255)
cs=np.asarray(cs.filter(ImageFilter.GaussianBlur(T(5)))).astype(float)/255*0.7
e=e*(1-cs[...,None]*np.array([0.55,0.62,0.72]))
comp=e*(1-pm[...,None])+P*pm[...,None]
res=Image.fromarray(np.clip(comp,0,255).astype(np.uint8))
res=relight(res,pm,bb,key_col=(262,256,246),shadow_col=(214,204,194),fall_pow=1.3,spec_pos=0.12,spec_w=0.045,spec_amt=0.16,term=0.52,term_w=0.08,top_tame=0.15,grain_match=1.0,soften=0)
# 4) fingertips back in front of the cap (from the moved hand) + their soft shadow on the cap
a=np.asarray(res).astype(float); Hs=np.asarray(Image.fromarray((Ms*255).astype(np.uint8)).resize((OW,OH),Image.LANCZOS)).astype(float)/255
handO=np.asarray(Image.fromarray(hand[...,::-1]).resize((OW,OH),Image.LANCZOS)).astype(float)
a=a*(1-Hs[...,None])+handO*Hs[...,None]
ys,xs=np.where((Hs>0.5)&(pm>0.5)|((Hs>0.5)&(np.arange(OH)[:,None]>bb[1]-T(30))&(np.arange(OH)[:,None]<bb[1]+T(10))&(np.arange(OW)[None,:]>bb[0])&(np.arange(OW)[None,:]<bb[2])))
if len(xs):
    shm=Image.new('L',(OW,OH),0); ImageDraw.Draw(shm).ellipse((xs.min()+T(14),bb[1]-T(2),xs.max()+T(26),bb[1]+T(34)),fill=255)
    shm=np.asarray(shm.filter(ImageFilter.GaussianBlur(T(9)))).astype(float)/255*0.32*pm*(1-Hs)
    a=a*(1-shm[...,None]*np.array([0.45,0.55,0.65]))
Image.fromarray(np.clip(a,0,255).astype(np.uint8)).save(OUT)
print('d',d,'new box',bb)
