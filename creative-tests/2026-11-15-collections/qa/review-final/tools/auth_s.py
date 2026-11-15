import sys,numpy as np,cv2
from PIL import Image
# auth_s.py master cutout x y w h
f,cut=sys.argv[1],sys.argv[2];x0,y0,w,h=map(int,sys.argv[3:7])
M=np.asarray(Image.open(f).convert('RGB')).astype(np.float32)
c=np.asarray(Image.open(cut).convert('RGBA')).astype(np.float32)
rr=cv2.resize(c,(w,h),interpolation=cv2.INTER_AREA);al=rr[...,3]/255
sel=cv2.erode(((al>0.995)*1).astype(np.uint8),np.ones((9,9),np.uint8))>0
xa,ya=max(0,-x0),max(0,-y0);xb,yb=min(w,M.shape[1]-x0),min(h,M.shape[0]-y0)
pred=rr[ya:yb,xa:xb,:3];act=M[y0+ya:y0+yb,x0+xa:x0+xb];s=sel[ya:yb,xa:xb]
m=s&(pred.max(-1)<245)&(pred.min(-1)>10)
gain=[float((act[...,i][m]*pred[...,i][m]).sum()/(pred[...,i][m]**2).sum()) for i in range(3)]
g=np.mean(gain);d=(act-pred*g)[m];lum=d.mean(1);chroma=(d-lum[:,None]).std()
# low-pass residual
R=np.zeros(act.shape[:2]);R[m]=(act-pred*g).mean(-1)[m]
W=cv2.GaussianBlur(m.astype(np.float32),(0,0),25);L=cv2.GaussianBlur(R.astype(np.float32),(0,0),25)/np.maximum(W,1e-3)
lp=L[m&(W>0.5)]
fl=pred[:, ::-1]*g; dm=np.abs(act-fl)[s].mean(); dn=np.abs(act-pred*g)[s].mean()
print('gain',np.round(gain,4),'resid sd %.2f chromaSD %.2f lowpass %.2f..%.2f  |d| %.1f mirror|d| %.1f'%(d.std(),chroma,lp.min(),lp.max(),dn,dm))
