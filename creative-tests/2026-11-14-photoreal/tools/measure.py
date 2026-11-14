import numpy as np
from PIL import Image, ImageFilter
CUT='/home/claude/everliv-media-repo/library/peptide-eye-serum/peptide-eye-serum--front-cutout.png'
def sharp(img):
    a=np.asarray(img.convert('L')).astype(float)
    gx=np.diff(a,axis=1)[:-1,:]; gy=np.diff(a,axis=0)[:,:-1]
    g=np.hypot(gx,gy); return float(np.percentile(g,99))   # edge strength of the crispest 1% (text strokes)
def label_region(img, box):
    x0,y0,x1,y1=box; w=x1-x0; h=y1-y0
    return img.crop((int(x0+0.12*w),int(y0+0.40*h),int(x0+0.88*w),int(y0+0.90*h)))
def source_at(width):
    c=Image.open(CUT).convert('RGBA'); c=c.crop(c.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox())
    h=round(c.height*width/c.width); r=c.resize((width,h),Image.LANCZOS)
    bg=Image.new('RGB',r.size,(255,255,255)); bg.paste(r,(0,0),r); return bg,(0,0,width,h)
