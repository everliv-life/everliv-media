import sys
from PIL import Image
# usage: crop.py name x0 y0 x1 y1 outname [zoom]
n,x0,y0,x1,y1,o=sys.argv[1],*map(int,sys.argv[2:6]),sys.argv[6]
z=float(sys.argv[7]) if len(sys.argv)>7 else 1
im=Image.open(f'/home/claude/coll/out/{n}-master.png').crop((x0,y0,x1,y1))
if z!=1: im=im.resize((int(im.width*z),int(im.height*z)),Image.NEAREST)
im.save(f'/home/claude/review-coll2/{o}.png')
