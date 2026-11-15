import json,sys,numpy as np,cv2
from PIL import Image
n=sys.argv[1]
r=json.load(open(f'/home/claude/coll/out/{n}-report.json'))
M=np.asarray(Image.open(f'/home/claude/coll/out/{n}-master.png')).astype(float)
for it in r['items']:
  x,y=it['xy'];w,h=it['px']
  # kraft: upper body region, label white: label centre
  k=M[y+int(h*.62):y+int(h*.66),x+int(w*.05):x+int(w*.15)].mean(-1)
  lab=M[y+int(h*.80):y+int(h*.83),x+int(w*.45):x+int(w*.55)].mean(-1)
  print(it['cutout'].split('/')[-1][7:20],'kraft med',np.median(k).round(),'label p90',np.percentile(lab,90).round(),'w',w,'h',h,'xy',x,y)
for b in sys.argv[2:]:
  x0,y0,x1,y1=map(int,b.split(','));print('region',b,'median',np.median(M[y0:y1,x0:x1].mean(-1)).round(),'p90',np.percentile(M[y0:y1,x0:x1].mean(-1),90).round())
