#!/usr/bin/env python3
"""EverLiv cover QC: samples a video, scores frames, picks a cover, renders grid-crop previews.
Score = edge detail (text/branding) + contrast; flags blank/near-uniform frames.
Usage: cover_qc.py video.mp4 [outdir]  -> prints JSON with per-frame stats and recommended cover ms."""
import sys,subprocess,json,os
import numpy as np
from PIL import Image, ImageFilter
def frames(v,step=0.25):
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v]).decode().strip())
    out=[];t=0.0
    while t<d-0.05:
        raw=subprocess.check_output(['ffmpeg','-v','error','-ss',f'{t:.3f}','-i',v,'-frames:v','1','-f','image2pipe','-vcodec','png','-'])
        from io import BytesIO
        out.append((t,Image.open(BytesIO(raw)).convert('RGB')));t+=step
    return d,out
def score(im):
    g=np.asarray(im.convert('L').resize((270,int(270*im.height/im.width))),dtype=np.float32)
    e=np.asarray(im.convert('L').resize((270,int(270*im.height/im.width))).filter(ImageFilter.FIND_EDGES),dtype=np.float32)
    return dict(std=float(g.std()),edge=float((e>40).mean()*100),mean=float(g.mean()))
def grid_crops(im):
    W,H=im.size; r={}
    # IG profile grid 3:4 (1080x1440) centre crop; TikTok grid 3:4 centre crop; FB/YT 9:16 full.
    for k,ar in (('ig_grid_3x4',3/4),('tiktok_grid_3x4',3/4),('square_1x1',1.0)):
        ch=min(H,int(W/ar)); top=(H-ch)//2; r[k]=im.crop((0,top,W,top+ch))
    return r
if __name__=='__main__':
    v=sys.argv[1]; od=sys.argv[2] if len(sys.argv)>2 else '/tmp/cov'; os.makedirs(od,exist_ok=True)
    d,fr=frames(v); rows=[]
    for t,im in fr:
        s=score(im); gc={k:score(c) for k,c in grid_crops(im).items()}
        s['grid_edge_min']=min(x['edge'] for x in gc.values()); s['t']=round(t,2); rows.append(s)
    blank=[r['t'] for r in rows if r['grid_edge_min']<2.0 or r['std']<6]
    best=max(rows,key=lambda r:(r['grid_edge_min'],r['std']))
    base=os.path.splitext(os.path.basename(v))[0]
    res=dict(file=v,duration=round(d,2),first_frame=rows[0],first_frame_blank=rows[0]['t'] in blank,blank_times=blank,recommended_ms=int(best['t']*1000),recommended=best)
    im=dict(fr)[best['t']]; im.save(f'{od}/{base}--cover.png')
    for k,c in grid_crops(im).items(): c.resize((300,int(300*c.height/c.width))).save(f'{od}/{base}--cover-{k}.png')
    dict(fr)[0.0].save(f'{od}/{base}--frame0.png')
    # GATE (standard 2026-11-19): TikTok, X, Threads and IG/TikTok carousel video slides must open on
    # a meaningful frame because their cover setting is absent or unverified. Pass --platform to enforce.
    plat=os.environ.get('QC_PLATFORM','')
    for a in sys.argv[3:]:
        if a.startswith('--platform='): plat=a.split('=',1)[1]
    if plat.lower() in ('tiktok','x','twitter','threads','carousel'):
        # first 0.5 s must all be non-blank (covers platforms that sample slightly after frame 0)
        early=[r for r in rows if r['t']<0.5]
        res['gate']=dict(platform=plat,passed=not any(r['t'] in blank for r in early),
                         rule='first 0.5 s non-blank in full frame and every grid crop')
    print(json.dumps(res))
    if res.get('gate') and not res['gate']['passed']: sys.exit(2)
