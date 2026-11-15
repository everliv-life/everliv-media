import json,sys,numpy as np
from PIL import Image
n=sys.argv[1]
r=json.load(open(f'/home/claude/coll/out/{n}-report.json'))
M=np.asarray(Image.open(f'/home/claude/coll/out/{n}-master.png')).astype(float).mean(-1)
P=np.asarray(Image.open('/home/claude/coll/'+r['plate']).convert('RGB')).astype(float)
g=np.array(r.get('scene_wb_gain',[1,1,1]));P=(P*g).mean(-1)
R=M/np.maximum(P,1)
for it in r['items']:
  x0,y0=it['xy'];w,h=it['px'];nm=it['cutout'].split('/')[-1][:22]
  yb=y0+h
  # min ratio in a box to the right of base and behind
  box=R[yb-int(h*0.25):yb+5, x0+w:x0+w+int(w*0.6)]
  front=R[yb+2:yb+12, x0+w//4:x0+3*w//4]
  print(nm,'base y',yb,'right-of-base min/median',round(box.min(),3),round(np.median(box),3),'front-of-base median',round(np.median(front),3))
