import sys,numpy as np
from PIL import Image
a=np.asarray(Image.open(sys.argv[1])).astype(int);b=np.asarray(Image.open(sys.argv[2])).astype(int)
d=np.abs(a-b).max(-1)
m=d>12
ys,xs=np.where(m);print('diff bbox',xs.min(),ys.min(),xs.max(),ys.max(),'n',m.sum())
# columns/rows profile
for y in range(0,2700,100):
  r=np.where(m[y])[0]
  if len(r): print(y,r.min(),r.max(),len(r))
Image.fromarray((np.clip(d*4,0,255)).astype(np.uint8)).resize((540,675)).save(sys.argv[3])
