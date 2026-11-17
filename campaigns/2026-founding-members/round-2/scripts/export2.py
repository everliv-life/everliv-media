import csv, json, datetime as dt, pathlib
import plan2, plan
from plan import url, MEM, TIMES, TZ
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
OUT = pathlib.Path(__file__).parent/'package-r2'; OUT.mkdir(exist_ok=True)
MUSIC_NOTE = ("Instagram catalog track via Instagram Audio API (Metricool). Organic Instagram Reels only; not for boosting/ads, "
              "not for embedding in exported files or other platforms. Re-confirm availability 48 h before publishing.")
def fmt_for(p, plat):
    if plat == 'Email': return 'Email', TIMES['Email']
    if plat in ('IG', 'FB'):
        f = {'feed': 'feed', 'carousel': 'carousel', 'reel': 'reel'}[p['fmt']]
        if p['status'] == 'MOTION' and f == 'feed': f = 'reel (motion version)'
        return f'{plat} {f}', TIMES.get(f'{plat} {f.split()[0]}', TIMES['IG feed'] if plat == 'IG' else TIMES['FB feed'])
    return {'TikTok': 'TikTok video' if p['fmt'] == 'reel' or p['status'] == 'MOTION' else 'TikTok photo carousel', 'YT': 'YouTube Short', 'Threads': 'Threads post',
            'X': 'X post', 'Pinterest*': 'Pinterest pin'}[plat], TIMES[plat]
rows = []
for p in plan2.P:
    if p['rev'] == 'REMOVED':
        continue
    for plat in p['platforms']:
        f, t = fmt_for(p, plat)
        src = {'IG': 'instagram', 'FB': 'facebook', 'Email': 'email', 'TikTok': 'tiktok', 'YT': 'youtube', 'Threads': 'threads', 'X': 'x', 'Pinterest*': 'pinterest'}[plat]
        music = p['music'] if (plat in ('IG',) and (p['fmt'] == 'reel' or p['status'] == 'MOTION')) else ''
        cap = plan.adapt(p, plat) if plat not in ('Email',) else p['caption']
        rows.append(dict(Date=p['date'], Day=dt.date.fromisoformat(p['date']).strftime('%a'), Time=f'{t} {TZ}', Platform=plat, Format=f, Phase=p['phase'],
                         ID=p['id'], Title=p['title'], Hook=p['hook'], Caption=cap, Kind={'member': 'Membership', 'product': 'Product & gifting', 'brand': 'Brand & lifestyle'}[p['kind']],
                         Asset=p['asset'], Motion=' | '.join(p['motion']), Revision=p['rev'], Status=p['status'],
                         Music=music, MusicStatus=(('Metricool draft #' + plan2.DRAFTED[p['id']] + ' · ' if p['id'] in plan2.DRAFTED else 'Proposed · ') + MUSIC_NOTE) if music else '',
                         CTA=p['cta'], URL=url(p['path'], src, 'email' if plat == 'Email' else 'social', p['id'].lower()), Notes=p.get('note', ''), Dependencies=p['deps']))
d = dt.date(2026, 11, 18)
while d <= dt.date(2027, 1, 31):
    s = plan2.story_for(d)
    if s:
        for plat in ('IG', 'FB'):
            rows.append(dict(Date=d.isoformat(), Day=d.strftime('%a'), Time=f"{TIMES['IG story']} {TZ}", Platform=plat, Format=f'{plat} story', Phase='Stories',
                             ID=f"S{d.strftime('%m%d')}", Title=f"Stories: {s.replace('story-', '')}", Hook='', Caption='Story frame from the round-2 set + same-day feed post.',
                             Kind='Membership' if s in ('story-offer', 'story-founding', 'story-quiz', 'story-ten', 'story-week', 'story-tomorrow', 'story-last') else 'Product & gifting' if s in ('story-strips', 'story-coffee') else 'Brand & lifestyle',
                             Asset=f'stories-r2/{s}', Motion='', Revision='NEW', Status='READY', Music='', MusicStatus='', CTA='Link sticker',
                             URL=url(MEM, 'instagram' if plat == 'IG' else 'facebook', 'story', f"s{d.strftime('%m%d')}"), Notes='', Dependencies=''))
    d += dt.timedelta(days=1)
rows.sort(key=lambda r: (r['Date'], r['Time'], r['Platform']))
cols = list(rows[0].keys())
with open(OUT/'master-calendar-r2.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rows)
wb = Workbook(); ws = wb.active; ws.title = 'Calendar'
ws.append(cols)
for r in rows: ws.append([r[c] for c in cols])
for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='2A422A')
widths = dict(Date=11, Day=5, Time=14, Platform=8, Format=20, Phase=26, ID=7, Title=36, Hook=34, Caption=60, Kind=16, Asset=32, Motion=36, Revision=10, Status=12, Music=44, MusicStatus=50, CTA=14, URL=40, Notes=44, Dependencies=40)
for i, c in enumerate(cols, 1): ws.column_dimensions[ws.cell(1, i).column_letter].width = widths.get(c, 14)
ws.freeze_panes = 'A2'; ws.auto_filter.ref = ws.dimensions
ws2 = wb.create_sheet('Pieces')
pc = ['date', 'id', 'title', 'kind', 'fmt', 'asset', 'motion', 'rev', 'status', 'music', 'note']
ws2.append(pc)
for p in plan2.P: ws2.append([', '.join(p[k]) if isinstance(p[k], list) else str(p[k]) for k in pc])
ws3 = wb.create_sheet('Mix')
ws3.append(['Window', 'Feed pieces', 'Membership', 'Product & gifting', 'Brand & lifestyle'])
for a, b in [('2026-11-18', '2026-11-30'), ('2026-12-01', '2026-12-20'), ('2026-12-21', '2026-12-31'), ('2027-01-01', '2027-01-31'), ('2026-11-18', '2027-01-31')]:
    n, c = plan2.mix(a, b); ws3.append([f'{a} to {b}', n, f"{c['member']} ({round(100*c['member']/n)}%)", f"{c['product']} ({round(100*c['product']/n)}%)", f"{c['brand']} ({round(100*c['brand']/n)}%)"])
wb.save(OUT/'EverLiv-Campaign-Calendar-R2-Nov18-Jan31.xlsx')
json.dump(rows, open(OUT/'calendar-r2.json', 'w'))
print(len(rows), 'rows;', len([p for p in plan2.P if p['rev'] != 'REMOVED']), 'pieces')
