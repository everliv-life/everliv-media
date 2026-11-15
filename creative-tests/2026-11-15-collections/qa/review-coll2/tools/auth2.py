import json,sys,numpy as np,cv2
from PIL import Image
# authenticity with interior mask (eroded 4px) + per-channel gain fit + mirror test
for n in sys.argv[1:]:
  r=json.load(open(f'/home/claude/coll/out/{n}-report.json'));e=r['exposure_scalar']
  M=np.asarray(Image.open(f'/home/claude/coll/out/{n}-master.png')).astype(np.float32)
  print(n,'expo',e,'items',len(r['items']))
  for k,it in enumerate(r['items']):
    c=np.asarray(Image.open(it['cutout']).convert('RGBA')).astype(np.float32)
    w,h=it['px'];rr=cv2.resize(c,(w,h),interpolation=cv2.INTER_AREA)
    x0,y0=it['xy'];al=rr[...,3]/255
    sel=cv2.erode(((al>0.995)*1).astype(np.uint8),np.ones((9,9),np.uint8))>0
    for j,o in enumerate(r['items']):
      if j>k:
        ox,oy=o['xy'];ow,oh=o['px']
        xa,ya,xb,yb=max(x0,ox),max(y0,oy),min(x0+w,ox+ow),min(y0+h,oy+oh)
        if xa<xb and ya<yb: sel[ya-y0:yb-y0,xa-x0:xb-x0]=False
    xa,ya=max(0,-x0),max(0,-y0); xb,yb=min(w,M.shape[1]-x0),min(h,M.shape[0]-y0)
    pred=np.clip(rr[...,:3]*e,0,255)[ya:yb,xa:xb];act=M[y0+ya:y0+yb,x0+xa:x0+xb];s=sel[ya:yb,xa:xb]
    m=s&(pred.max(-1)<245)&(pred.min(-1)>10)
    d=(act-pred)[m]
    gain=[float((act[...,i][m]*pred[...,i][m]).sum()/(pred[...,i][m]**2).sum()) for i in range(3)]
    fl=pred[:, ::-1]; dm=np.abs(act-fl)[s].mean()
    lum=d.mean(1); chroma=(d-lum[:,None]).std()
    print('   %-32s mean %s sd %.2f chromaSD %.2f gain %s mirror %.1f cut %s'%(it['cutout'].split('/')[-1][:32],d.mean(0).round(2),d.std(),chroma,np.round(gain,4),dm,(xa,ya,w-xb,h-yb)))
