import json,sys,numpy as np,cv2
from PIL import Image
# shadow map: master/plate on scene pixels (product pixels painted magenta); saves crop
n,x0c,y0c,x1c,y1c,o=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
r=json.load(open(f'/home/claude/coll/out/{n}-report.json'))
M=np.asarray(Image.open(f'/home/claude/coll/out/{n}-master.png')).astype(float)
P=np.asarray(Image.open('/home/claude/coll/'+r['plate']).convert('RGB')).astype(float)
g=np.array(r.get('scene_wb_gain',[1,1,1]));P=np.clip(P*g,0,255)
R=(M.mean(-1)+.5)/np.maximum(P.mean(-1),1)
mask=np.zeros(R.shape,bool)
for it in r['items']:
  c=np.asarray(Image.open(it['cutout']).convert('RGBA'))[...,3]
  w,h=it['px'];a=cv2.resize(c,(w,h),interpolation=cv2.INTER_AREA)>8
  x,y=it['xy'];ya,xa=max(0,y),max(0,x);yb,xb=min(R.shape[0],y+h),min(R.shape[1],x+w)
  mask[ya:yb,xa:xb]|=a[ya-y:yb-y,xa-x:xb-x]
img=np.clip((R-0.4)/0.65,0,1)*255
out=np.stack([img]*3,-1);out[mask]=[255,0,255]
Image.fromarray(out[y0c:y1c,x0c:x1c].astype(np.uint8)).save(f'/home/claude/review-coll3/{o}.png')
sc=~mask[y0c:y1c,x0c:x1c]; rr=R[y0c:y1c,x0c:x1c][sc]
print(o,'scene ratio min %.3f p1 %.3f p5 %.3f'%(rr.min(),np.percentile(rr,1),np.percentile(rr,5)))
