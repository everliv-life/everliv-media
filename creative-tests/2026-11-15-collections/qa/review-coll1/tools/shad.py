import json,sys,numpy as np
from PIL import Image
n=sys.argv[1]
r=json.load(open(f'/home/claude/coll/out/{n}-report.json'))
M=np.asarray(Image.open(f'/home/claude/coll/out/{n}-master.png')).astype(float).mean(-1)
P=np.asarray(Image.open('/home/claude/coll/'+r['plate']).convert('RGB')).astype(float)
g=np.array(r.get('scene_wb_gain',[1,1,1]));P=(P*g).mean(-1)
for it in r['items']:
  x0,y0=it['xy'];w,h=it['px'];nm=it['cutout'].split('/')[-1][:28]
  out=[]
  # right side, mid height, offsets
  for d in [3,10,25,50,90]:
    xs=x0+w+d; ys=slice(y0+h//3,y0+2*h//3)
    if xs<M.shape[1]: out.append(round(float(np.median(M[ys,xs]/np.maximum(P[ys,xs],1))),3))
  outb=[]
  for d in [3,10,25,50,90]:
    yy=y0+h+d; xs=slice(x0+w//3,x0+2*w//3)
    if yy<M.shape[0]: outb.append(round(float(np.median(M[yy,xs]/np.maximum(P[yy,xs],1))),3))
  outl=[]
  for d in [3,10,25]:
    xs=x0-d; ys=slice(y0+h//3,y0+2*h//3); outl.append(round(float(np.median(M[ys,xs]/np.maximum(P[ys,xs],1))),3))
  print(nm,'R',out,'B',outb,'L',outl)
