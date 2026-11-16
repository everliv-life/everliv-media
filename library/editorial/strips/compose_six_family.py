"""Six-tin strip family (owner direction Nov 15 23:52): all six varieties incl. Sleep, no cropping.
Uses lineup() from compose_strips.py: authentic supplier cut-outs, uniform scale only, background-only contact shadow."""
import os
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'compose_strips.py')).read().split("five=['energy'")[0]
ns={};exec(src,ns);lineup=ns['lineup']
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cutouts'))
# Desktop 3x2, 1920x1280 (3:2). Order keeps the two purple tins (Sleep, Iron) apart; Energy (best seller) leads.
T=500;g=70;W,H=1920,1280;th=round(T*1362/1352)
xs=[W/2-(T+g),W/2,W/2+(T+g)];vy=(th+90)/2
top=['energy','sleep','hydrate'];bot=['collagen','d3k2','iron']
lineup(top+bot,[(x,H/2-vy) for x in xs]+[(x,H/2+vy) for x in xs],W,H,T,'../strips-family-6--desktop-3x2')
# Mobile 2x3, 1080x1620 (2:3).
T=420;g=60;W,H=1080,1620;th=round(T*1362/1352)
xs=[W/2-(T+g)/2,W/2+(T+g)/2];ys=[H/2-(th+70),H/2,H/2+(th+70)]
order=[['energy','sleep'],['hydrate','collagen'],['d3k2','iron']]
lineup(sum(order,[]),[(x,y) for y in ys for x in xs],W,H,T,'../strips-family-6--mobile-2x3')
print('ok')
