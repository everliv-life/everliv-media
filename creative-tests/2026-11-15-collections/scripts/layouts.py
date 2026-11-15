import json
K='/home/claude/kit/cutouts/'
SO={'omh':'everliv-milk-honey-soap','coco':'coconut-beach-soap','sand':'everliv-sandalwood-soap','slum':'everliv-clean-forrest-soap','aloe':'everliv-aloe-cool-cucumber-soap','char':'everliv-charcoal-soap'}
CO={'haz':'everliv-hazelnut-coffee-medium-roast','coc':'everliv-cocoa-coffee-medium-roast','mus':'everliv-mushroom-coffee-medium-roast','car':'everliv-caramel-coffee-dark-roast'}
def soap(k,x,y,w): return {'cutout':K+SO[k]+'--front-cutout-v2.png','x':x,'y':y,'w':w}
def cof(k,x,y,w): return {'cutout':K+CO[k]+'--front-cutout-v2.png','x':x,'y':y,'w':w,'choke':1}
def grid(keys,cx,cy,w,gx,gy,cols):
    import math
    rows=math.ceil(len(keys)/cols); h=w*0.89
    out=[]
    for i,k in enumerate(keys):
        r,c=divmod(i,cols)
        x=cx+(c-(cols-1)/2)*(w+gx); y=cy+(r-(rows-1)/2)*(h+gy); out.append(soap(k,round(x),round(y),w))
    return out
L={}
six=['aloe','slum','char','omh','sand','coco']
TD={'dx':38,'dy':48,'sigma':30,'strength':0.2,'contact':0.32}
L['soapcoll_stone_wide']=dict(plate='plates/soap_stone_wide.jpg',out='out/soapcoll_stone_wide',scene_wb=0.5,expo='auto',expo_region=[1000,200,2100,1300],mode='topdown',shadow=TD,grain_sd=2.4,
  items=grid(six,1560,760,365,90,90,3),exports=[[2560,1429,'desktop'],[1920,1072,'desktop']])
L['soapcoll_stone_vert']=dict(plate='plates/soap_stone_vert.jpg',out='out/soapcoll_stone_vert',scene_wb=0.5,expo='auto',expo_region=[200,800,1400,2100],mode='topdown',shadow={**TD,'dx':52,'dy':64,'sigma':52},grain_sd=2.4,
  items=grid(six,790,1380,450,70,70,2),exports=[[1080,1350,'mobile-social']])
def cascade(keys,cx,cy,w,g,shift):
    h=w*0.89; out=[]
    for i,k in enumerate(keys):
        r,c=divmod(i,3); x=cx+(c-1)*(w+g)+(shift*(w+g) if r==1 else -shift*(w+g)/2); y=cy+(r-0.5)*(h+g); out.append(soap(k,round(x),round(y),w))
    return out
gift=['omh','sand','coco','slum','aloe','char']
L['soapcoll_gift_wide']=dict(plate='plates/soap_gift_wide.jpg',out='out/soapcoll_gift_wide',scene_wb=0.5,expo='auto',expo_region=[1000,300,2100,1300],mode='topdown',shadow=TD,grain_sd=2.4,
  items=cascade(gift,1560,790,310,80,0.3),exports=[[2560,1429,'desktop'],[1920,1072,'desktop']])
L['soapcoll_gift_vert']=dict(plate='plates/soap_gift_vert.jpg',out='out/soapcoll_gift_vert',scene_wb=0.5,expo='auto',expo_region=[200,800,1400,2100],mode='topdown',shadow={**TD,'dx':52,'dy':64,'sigma':52},grain_sd=2.4,
  items=grid(gift,780,1470,380,70,70,2),exports=[[1080,1350,'mobile-social']])
json.dump(L,open('layouts.json','w'),indent=1)
UP=lambda h:{'contact':0.25,'glen':0.2,'gdx':h*0.2,'gsigma':max(8,h*0.016),'gstrength':0.27,'front_fade':max(20,int(h*0.028))}
def row(keys,cx,base,w,gap):
    n=len(keys); return [cof(k,round(cx+(i-(n-1)/2)*(w+gap)),base,w) for i,k in enumerate(keys)]
four=['haz','coc','mus','car']
L['coffeecoll_counter_wide']=dict(plate='plates/coffee_counter_wide.jpg',out='out/coffeecoll_counter_wide',scene_wb=0.4,expo='auto',expo_region=[900,1150,2000,1300],expo_bias=0.97,mode='upright',shadow={**UP(595),'gstrength':0.45,'glen':0.45,'gsigma':5},grain_sd=2.4,
  items=row(four,1450,1285,270,60),exports=[[2560,1429,'desktop'],[1920,1072,'desktop']])
L['coffeecoll_counter_vert']=dict(plate='plates/coffee_counter_vert.jpg',out='out/coffeecoll_counter_vert',scene_wb=0.4,expo='auto',expo_region=[100,1780,1300,1950],expo_bias=0.97,mode='upright',shadow={**UP(605),'gstrength':0.45,'glen':0.45,'gsigma':5},grain_sd=2.4,
  items=row(four,678,1905,275,30),exports=[[1080,1350,'mobile-social']])
L['coffeecoll_gift_wide']=dict(plate='plates/coffee_gift_wide.jpg',out='out/coffeecoll_gift_wide',scene_wb=0.3,expo=0.8,mode='upright',shadow=UP(530),grain_sd=2.4,
  items=[dict(i,choke=2) for i in row(four,1500,1215,240,60)],exports=[[2560,1429,'desktop'],[1920,1072,'desktop']])
L['coffeecoll_gift_vert']=dict(plate='plates/coffee_gift_vert.jpg',out='out/coffeecoll_gift_vert',scene_wb=0.3,expo=0.8,mode='upright',shadow=UP(430),grain_sd=2.4,
  items=[dict(i,choke=2) for i in row(four,700,1830,250,35)],exports=[[1080,1350,'mobile-social']])
def soapup(k,x,base,w): d=soap(k,x,base,w); return d
L['mixed_holiday_wide_old']=dict(plate='plates/holiday_table_wide.jpg',out='out/mixed_holiday_wide',scene_wb=0.3,expo='auto',expo_region=[1000,950,1900,1150],expo_bias=0.95,mode='upright',shadow=UP(600),grain_sd=2.4,
  items=[cof('car',1610,1075,258),cof('coc',1270,1100,272),soapup('sand',1080,1190,214),soapup('omh',1345,1196,218),soapup('char',1620,1192,216)],
  exports=[[2560,1429,'desktop'],[1920,1072,'desktop']])
L['mixed_holiday_vert_old']=dict(plate='plates/holiday_table_vert.jpg',out='out/mixed_holiday_vert',scene_wb=0.3,expo='auto',expo_region=[150,1700,1250,1850],expo_bias=0.95,mode='upright',shadow=UP(620),grain_sd=2.4,
  items=[cof('car',905,1790,312),cof('coc',530,1815,330),soapup('sand',330,1935,262),soapup('omh',640,1942,266),soapup('char',950,1938,264)],
  exports=[[1080,1350,'mobile-social']])
def alt(seq,x0,base,gap):
    out=[]; x=x0
    for kind,k,w in seq:
        out.append((cof if kind=='c' else soapup)(k,round(x+w/2),base,w)); x+=w+gap
    return out
L['mixed_holiday_wide']=dict(plate='plates/holiday_low_wide.jpg',out='out/mixed_holiday_wide',scene_wb=0.55,expo='auto',expo_region=[800,1180,2050,1300],expo_bias=0.95,mode='upright',shadow={**UP(552),'gstrength':0.3},grain_sd=2.4,
  items=alt([('s','sand',204),('c','coc',250),('s','omh',204),('c','car',250),('s','char',204)],825,1268,35),exports=[[2560,1429,'desktop'],[1920,1072,'desktop']])
L['mixed_holiday_vert']=dict(plate='plates/holiday_low_vert.jpg',out='out/mixed_holiday_vert',scene_wb=0.55,expo='auto',expo_region=[100,1900,1200,2000],expo_bias=0.95,mode='upright',shadow={**UP(610),'gstrength':0.3},grain_sd=2.4,
  items=alt([('c','coc',276),('s','omh',224),('c','car',276),('s','sand',224)],95,1968,40),exports=[[1080,1350,'mobile-social']])
L.pop('mixed_holiday_wide_old',None); L.pop('mixed_holiday_vert_old',None)
json.dump(L,open('layouts.json','w'),indent=1)
