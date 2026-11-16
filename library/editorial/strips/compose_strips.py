"""Clean strip-tin lineups from authentic supplier front renders (cut-outs). Product pixels: uniform scale only.
Soft contact shadow drawn on the background layer only. Outputs transparent PNG + Capsule Ivory preview."""
import sys, json, numpy as np, cv2
from PIL import Image
IVORY=(233,228,223)
def lineup(keys, layout, W, H, tile, name):
    canvas=np.zeros((H,W,4),np.float32); shadow=np.zeros((H,W),np.float32)
    placed=[]
    for k,(cx,cy) in zip(keys,layout):
        c=Image.open(f'{k}--cutout.png').convert('RGBA'); s=tile/c.size[0]
        c=c.resize((round(c.size[0]*s),round(c.size[1]*s)),Image.LANCZOS); a=np.asarray(c).astype(np.float32)
        x0,y0=int(cx-c.size[0]/2),int(cy-c.size[1]/2); h,w=a.shape[:2]
        # contact shadow: soft ellipse under the tin's bottom edge
        sh=np.zeros((H,W),np.float32); cv2.ellipse(sh,(int(cx),int(y0+h*0.985)),(int(w*0.46),int(h*0.045)),0,0,360,1,-1)
        shadow=np.maximum(shadow,cv2.GaussianBlur(sh,(0,0),h*0.03))
        placed.append((a,x0,y0)); 
    for a,x0,y0 in placed:
        h,w=a.shape[:2]; al=a[...,3:4]/255
        reg=canvas[y0:y0+h,x0:x0+w]; reg[...,:3]=a[...,:3]*al+reg[...,:3]*(1-al); reg[...,3:4]=np.maximum(reg[...,3:4],al)
    # transparent output with shadow baked as semi-transparent black
    out=canvas.copy(); sa=np.clip(shadow*0.35,0,1)[...,None]
    base_a=out[...,3:4]; rgb=out[...,:3]*base_a; a_tot=base_a+sa*(1-base_a)
    rgb_tot=(rgb+0*sa*(1-base_a))/np.maximum(a_tot,1e-6)
    png=np.dstack([rgb_tot,a_tot*255]).clip(0,255).astype(np.uint8)
    Image.fromarray(png,'RGBA').save(name+'--transparent.png')
    bg=np.ones((H,W,3),np.float32)*np.array(IVORY); bg*=(1-shadow*0.25)[...,None]
    al=canvas[...,3:4]; prev=(canvas[...,:3]*al+bg*(1-al)).clip(0,255).astype(np.uint8)
    Image.fromarray(prev).save(name+'--ivory-preview.jpg',quality=93)
    return name
five=['energy','hydrate','iron','d3k2','collagen']; six=['energy','hydrate','sleep','iron','d3k2','collagen']
T=440; g=60
row=lambda n,W,y: [(W/2+(i-(n-1)/2)*(T+g),y) for i in range(n)]
lineup(five, row(5,2700,450), 2700, 900, T, 'strips-lineup-5--row')
lineup(six,  row(6,3200,450), 3200, 900, T, 'strips-lineup-6-incl-sleep--row')
# 3 + 2 / 3 + 3 non-overlapping grids (no clipping), for hero right half or square cards
def grid(keys, top, bottom, W, H, y1, y2):
    return [(x,y1) for x in top]+[(x,y2) for x in bottom]
W=1800;H=1500
lineup(five, grid(five,[W/2-(T+g),W/2,W/2+(T+g)],[W/2-(T+g)/2,W/2+(T+g)/2],W,H,0,0) and [(W/2-(T+g),450),(W/2,450),(W/2+(T+g),450),(W/2-(T+g)/2,1050),(W/2+(T+g)/2,1050)], W, H, T, 'strips-grid-5--3over2')
lineup(six, [(W/2-(T+g),450),(W/2,450),(W/2+(T+g),450),(W/2-(T+g),1050),(W/2,1050),(W/2+(T+g),1050)], W, H, T, 'strips-grid-6-incl-sleep--3over3')
print('ok')
