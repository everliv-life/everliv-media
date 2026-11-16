"""Four currently-available strips (Energy, Hydrate, Iron, D3+K2) as of Nov 16, 2026.
Sleep (sold out) and Collagen (paused, label verification) are excluded from purchase-driving creative.
Same method as compose_strips.py: authentic supplier cut-outs, uniform scale only."""
import os
here=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(here,'compose_strips.py')).read().split("five=['energy'")[0]
ns={};exec(src,ns);lineup=ns['lineup']
os.chdir(os.path.join(here,'cutouts'))
T=520;g=70;W,H=1400,1300;th=round(T*1362/1352)
xs=[W/2-(T+g)/2,W/2+(T+g)/2];ys=[H/2-(th+70)/2,H/2+(th+70)/2]
lineup(['energy','hydrate','iron','d3k2'],[(x,y) for y in ys for x in xs],W,H,T,'../strips-available-4--2x2')
T=440;g=60;W,H=2200,900
xs=[W/2-1.5*(T+g)+i*(T+g) for i in range(4)]
lineup(['energy','hydrate','iron','d3k2'],[(x,H/2) for x in xs],W,H,T,'../strips-available-4--row')
print('ok')
