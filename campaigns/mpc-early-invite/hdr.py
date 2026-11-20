import sys, asyncio; sys.path.insert(0,'/home/claude/ov')
import build_assets as B
from playwright.async_api import async_playwright
W,H=1200,680
body=f"""
<div class='green' style='position:relative;width:{W}px;height:{H}px;overflow:hidden'>
 <div style='position:absolute;left:50%;top:205px;width:620px;height:620px;transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(201,178,124,.20) 0%,rgba(201,178,124,.06) 38%,rgba(0,0,0,0) 66%)'></div>
 <div style='position:absolute;left:56px;top:48px'>{B.logo(True,40)}</div>
 <div style='position:absolute;left:0;right:0;top:92px;display:flex;justify-content:center'>{B.emblem(220)}</div>
 <div class='eb' style='position:absolute;left:0;right:0;top:350px;text-align:center;font-size:26px;letter-spacing:.34em;color:#C9B27C'>Member Price Club</div>
 <div class='hd' style='position:absolute;left:0;right:0;top:404px;text-align:center;font-size:86px;color:#F1ECE3'>An <i>early</i> <em class='foil' style='font-style:italic'>invitation.</em></div>
 <div class='rule' style='position:absolute;left:50%;top:528px;width:150px;transform:translateX(-50%)'></div>
 <div style='position:absolute;left:0;right:0;top:562px;text-align:center;font-size:30px;font-weight:450;color:#E9E4DF;opacity:.92'>12 months of member pricing &middot; $49.99 &middot; no automatic renewal</div>
</div>"""
html=f"<!doctype html><html><head><style>{B.CSS}</style></head><body style='--w:{W}px;--h:{H}px'>{body}</body></html>"
open('/home/claude/ov/email/v4/hdr.html','w').write(html)
async def m():
    async with async_playwright() as p:
        b=await p.chromium.launch(channel='chrome'); pg=await b.new_page(viewport={'width':W,'height':H},device_scale_factor=1)
        await pg.goto('file:///home/claude/ov/email/v4/hdr.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(600)
        await pg.screenshot(path='/home/claude/ov/email/v4/MPC-invite-header-gold_1200x680.png'); await b.close()
asyncio.run(m())
