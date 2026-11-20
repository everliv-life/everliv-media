"""Mixed product family for the MPC invite. v6.1 02-Product-Images supplier renders, scaled once uniformly,
merged on their own studio grey (247) with a darken blend: product pixels are untouched except pure-white
highlights above 247 (cap tops), which read identical on the matching background. No cutting, recolouring or redrawing."""
import numpy as np
from PIL import Image
S='src/v6/'
items=[('collagen','everliv-collagen-peptides-powder__01__everliv-collagen-peptides-powder-v5-mockup-1.jpg',252),
       ('nad','everliv-nad__01__everliv-nad-v5-mockup-0.jpg',240),
       ('energy','energy-strips__01__energy-strips-v5-mockup-4.jpg',122),
       ('hydrate','everliv-hydrate-strips__01__everliv-hydrate-strips-v5-mockup-4.jpg',122),
       ('serum','everliv-peptide-eye-serum__01__everliv-peptide-eye-serum-v5-mockup-3.jpg',246),
       ('creatine','everliv-pure-creatine-monohydrate__01__everliv-pure-creatine-monohydrate-v5-mockup-0.jpg',252)]
W,H,BASE=1700,470,425
crops=[]
for k,f,ht in items:
    im=Image.open(S+f).convert('RGB'); a=np.asarray(im).astype(int)
    m=(np.abs(a-247).max(2)>14)
    from scipy import ndimage
    lab,n=ndimage.label(ndimage.binary_closing(m,iterations=4)); sz=ndimage.sum(m,lab,range(1,n+1)); m=lab==(1+np.argmax(sz))
    ys,xs=np.where(m); x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    pad=int((y1-y0)*0.10)
    c=im.crop((max(0,x0-pad),max(0,y0-pad),min(2048,x1+pad),min(2048,y1+pad)))
    s=ht/(y1-y0); c=c.resize((round(c.width*s),round(c.height*s)),Image.LANCZOS)
    crops.append((k,c,round(pad*s)))
gap=24; total=sum(c.width for _,c,_ in crops)-sum(2*p for _,_,p in crops)+gap*(len(crops)-1)
x=(W-total)//2
can=np.full((H,W,3),247,np.uint8)
for k,c,p in crops:
    arr=np.asarray(c); top=BASE-(c.height-p)
    px=x-p; y0=max(0,top); ys=y0-top
    sub=arr[ys:ys+min(H-y0,arr.shape[0]-ys)]
    xs0=max(0,px); xx=xs0-px; sub=sub[:, xx:xx+min(W-xs0,sub.shape[1]-xx)]
    reg=can[y0:y0+sub.shape[0], xs0:xs0+sub.shape[1]].astype(float)
    hh,ww=sub.shape[:2]; f=max(4,int(p*0.8))
    ax=np.clip(np.minimum(np.arange(ww),ww-1-np.arange(ww))/f,0,1); ay=np.clip(np.minimum(np.arange(hh),hh-1-np.arange(hh))/f,0,1)
    al=(ay[:,None]*ax[None,:])[...,None]
    mn=np.minimum(reg,sub)
    can[y0:y0+hh, xs0:xs0+ww]=np.round(reg*(1-al)+mn*al).astype(np.uint8)
    print(k,'x',x,'w',c.width-2*p)
    x+=c.width-2*p+gap
mid=can[200:330].astype(int); cols=np.where((np.abs(mid-247).max(2)>3).any(0))[0]
l,r=cols.min(),cols.max(); cx=(l+r)//2; print('content',l,r,r-l)
out=Image.fromarray(can).crop((cx-600,140,cx+600,452))
out.save('email/v4/MPC-invite-product-family_1200x312.png',optimize=True)
