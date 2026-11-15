import json,sys,numpy as np,cv2
from PIL import Image
for n in sys.argv[1:]:
  r=json.load(open(f'/home/claude/coll/out/{n}-report.json'));e=r['exposure_scalar']
  M=np.asarray(Image.open(f'/home/claude/coll/out/{n}-master.png')).astype(np.float32)
  rows=[]
  for k,it in enumerate(r['items']):
    c=np.asarray(Image.open(it['cutout']).convert('RGBA')).astype(np.float32)
    w,h=it['px'];rr=cv2.resize(c,(w,h),interpolation=cv2.INTER_AREA)
    x0,y0=it['xy'];al=rr[...,3]/255
    # occlusion by later items
    occ=np.zeros((h,w),bool)
    for j,o in enumerate(r['items']):
      if j>k:
        ox,oy=o['xy'];ow,oh=o['px']
        xa,ya,xb,yb=max(x0,ox),max(y0,oy),min(x0+w,ox+ow),min(y0+h,oy+oh)
        if xa<xb and ya<yb: occ[ya-y0:yb-y0,xa-x0:xb-x0]=True
    sel=(al>0.995)&~occ
    pred=np.clip(rr[...,:3]*e,0,255);act=M[y0:y0+h,x0:x0+w]
    d=(act-pred)[sel & (pred.max(-1)<245)&(pred.min(-1)>10)]
    fl=act[:, ::-1]; dm=np.abs(fl-pred)[sel].mean()
    rows.append((it['cutout'].split('/')[-1][:30],round(float(np.abs(d.mean(0)).max()),2),d.mean(0).round(2).tolist(),round(float(d.std()),2),round(float(np.abs(d).mean()),2),round(float(dm),1)))
  print(n,'expo',e)
  for x in rows: print('  ',x)
