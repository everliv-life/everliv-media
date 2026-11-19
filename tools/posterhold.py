#!/usr/bin/env python3
"""Build a poster-hold variant: hold the frame at <cover_ms> for <hold_s> seconds,
then play the original video unchanged (audio, if any, delayed by the hold).
Validates: first decoded frame == hold frame, body PSNR vs source, cover_qc on output.
Usage: posterhold.py SRC OUT COVER_MS [HOLD_S=0.5]"""
import json, subprocess as sp, sys, os, tempfile, re
src, out, cover_ms = sys.argv[1], sys.argv[2], int(sys.argv[3])
hold = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
def run(*a): return sp.run(a, capture_output=True, text=True)
pr = json.loads(run('ffprobe','-v','error','-show_streams','-of','json',src).stdout)['streams']
v = [s for s in pr if s['codec_type']=='video'][0]; has_a = any(s['codec_type']=='audio' for s in pr)
fps = eval(v['r_frame_rate']); W, H = v['width'], v['height']
td = tempfile.mkdtemp(); hp = os.path.join(td,'hold.png')
run('ffmpeg','-v','error','-y','-ss',str(cover_ms/1000),'-i',src,'-frames:v','1',hp)
fc = f"[0:v]scale={W}:{H},format=yuv420p,setsar=1[a];[1:v]format=yuv420p,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]"
cmd = ['ffmpeg','-v','error','-y','-loop','1','-framerate',str(fps),'-t',str(hold),'-i',hp,'-i',src,'-filter_complex',fc,'-map','[v]']
if has_a:
    d = int(hold*1000); cmd[cmd.index('-filter_complex')+1] += f";[1:a]adelay={d}|{d}[aa]"; cmd += ['-map','[aa]','-c:a','aac','-b:a','192k']
tmp = out[:-4]+'.tmp.mp4'
cmd += ['-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-r',str(fps),'-movflags','+faststart',tmp]
r = run(*cmd); assert r.returncode==0, r.stderr; os.replace(tmp,out)
nf = int(round(hold*fps))
ps = run('ffmpeg','-i',out,'-i',src,'-filter_complex',f"[0:v]trim=start_frame={nf},setpts=PTS-STARTPTS[a];[a][1:v]psnr",'-f','null','-').stderr
body = float(re.search(r'average:([\d.inf]+)',ps).group(1)) if 'average:' in ps else None
ff = os.path.join(td,'f0.png'); run('ffmpeg','-v','error','-y','-i',out,'-frames:v','1',ff)
p0 = run('ffmpeg','-i',ff,'-i',hp,'-lavfi','psnr','-f','null','-').stderr
f0 = re.search(r'average:([\d.inf]+)',p0).group(1)
qc = json.loads(run('python3',os.path.join(os.path.dirname(__file__),'cover_qc.py'),out).stdout)
print(json.dumps({'out':out,'hold_s':hold,'cover_src_ms':cover_ms,'audio':has_a,'first_frame_vs_hold_psnr':f0,
  'body_psnr_vs_source':body,'first_frame_blank':qc['first_frame_blank'],'first_grid_edge_min':round(qc['first_frame']['grid_edge_min'],2)}))
