"""Export the master calendar, production manifest, January roadmap and scheduler import files."""
import csv, glob, os, json, pathlib
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
import plan
ROOT = pathlib.Path(__file__).parent; A = ROOT/'assets'; OUT = ROOT/'package'; OUT.mkdir(exist_ok=True)

def files_for(stem):
    if stem == 'SPEC': return []
    f = sorted(os.path.relpath(p, A) for p in glob.glob(str(A/f'{stem}*.png')))
    v = A/'video'/f'{stem}.mp4'
    if v.exists(): f = [os.path.relpath(v, A)] + [x for x in f if '_f' not in x]
    return f
def status(p):
    if p['asset'] == 'SPEC': return 'SPEC: storyboard/script ready; needs filming or editing'
    fs = files_for(p['asset'])
    if not fs: return 'TO PRODUCE'
    if p['fmt'] == 'email': return 'READY FOR REVIEW: header image + copy (build in Shopify Messaging)'
    if p['fmt'] == 'reel': return 'READY FOR REVIEW: MP4 rendered (no audio; add licensed music in-app)'
    return 'READY FOR REVIEW: rendered'

rows = plan.rows()
for r in rows:
    p = next((x for x in plan.P if x['id'] == r['ID']), None)
    if p:
        fs = files_for(p['asset']); r['Asset'] = '; '.join(fs) if fs else p['asset']; r['Production'] = status(p)
cols = ['Date', 'Day', 'Time', 'Platform', 'Format', 'Phase', 'ID', 'Title', 'Hook', 'Caption', 'Asset', 'CTA', 'URL', 'Objective',
        'Production', 'Approval', 'Dependencies', 'Alternates']
with open(OUT/'master-calendar-2026.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

# Metricool-style bulk import (DRAFTS ONLY). Verify headers against Metricool's current template before importing.
with open(OUT/'metricool-import-DRAFTS.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['Text', 'Date', 'Time', 'Draft', 'Instagram', 'Facebook', 'TikTok', 'Youtube', 'Threads', 'Picture Url 1', 'Video Url', 'Notes'])
    for r in rows:
        if r['Platform'] not in ('IG', 'FB', 'TikTok', 'YT', 'Threads') or 'story' in r['Format']: continue
        w.writerow([r['Caption'], r['Date'], r['Time'][:5], 'TRUE', 'TRUE' if r['Platform'] == 'IG' else 'FALSE',
                    'TRUE' if r['Platform'] == 'FB' else 'FALSE', 'TRUE' if r['Platform'] == 'TikTok' else 'FALSE',
                    'TRUE' if r['Platform'] == 'YT' else 'FALSE', 'TRUE' if r['Platform'] == 'Threads' else 'FALSE',
                    'NEEDS PUBLIC URL: ' + r['Asset'] if r['Asset'] else '', '', r['ID'] + ' | ' + r['Production']])

# Manifest
man = []
for p in plan.P:
    fs = files_for(p['asset'])
    man.append(dict(ID=p['id'], Date=p['date'], Title=p['title'], Format=p['fmt'], Platforms=', '.join(p['platforms']),
                    Status=status(p), Files='; '.join(fs), Alternates=' | '.join(p['alt']), Dependencies=p['deps']))
alts = sorted(os.path.relpath(x, A) for x in glob.glob(str(A/'ALT-*.png')))
tmpl = sorted(os.path.relpath(x, A) for x in glob.glob(str(A/'stories/*.png')))

JAN = [
 ('2027-01-01', 'New Year: "A year of member pricing starts today"', 'Feed + Reel + Stories; email E07 "New year, member pricing"', 'Enrollments'),
 ('2027-01-02 to 01-04', 'Routine series ep.1-3: morning / midday / training day', 'Carousels + TikTok', 'Discovery'),
 ('2027-01-05', 'Member math refresher (calculator carousel, live prices)', 'Carousel + Threads/X', 'Qualified enrollments'),
 ('2027-01-07', 'Checkout walkthrough reel (filmed member account)', 'Reel/TikTok/Shorts', 'Trust'),
 ('2027-01-08', 'EMAIL E08: "Your routine, your member price"', 'Email', 'Enrollments'),
 ('2027-01-10', 'Member FAQ (objections: renewal, 20%/15%, Subscribe & Save)', 'Carousel', 'Objection handling'),
 ('2027-01-12', 'Discover What\'s Next ep.2 (only if Restructuring confirms a new product)', 'Feed', 'Retention'),
 ('2027-01-14', 'Strips spotlight (availability-checked; Sleep/Collagen only if restocked)', 'Reel', 'Product sales'),
 ('2027-01-17', '"Two orders and you\'re ahead" real-cart carousel (re-priced)', 'Carousel', 'Enrollments'),
 ('2027-01-20', 'Founder/team note: why membership instead of sales', 'Talking-head reel', 'Brand trust'),
 ('2027-01-21', 'FINAL WINDOW opens: "10 days left at $49.99"', 'Feed + Stories + email E09', 'Enrollments'),
 ('2027-01-24', '"One week left": founding vs $69.99 side-by-side', 'Feed + Reel + Stories', 'Enrollments'),
 ('2027-01-27', 'Member math: $20 more after Jan 31 means break-even rises to ~$350 at 20% ($69.99 / 0.20)', 'Carousel', 'Urgency (truthful)'),
 ('2027-01-29', '"3 days left" + EMAIL E10', 'Feed + Stories + email', 'Enrollments'),
 ('2027-01-30', '"Tomorrow is the last day at $49.99"', 'Stories + Threads/X', 'Enrollments'),
 ('2027-01-31', 'LAST DAY: "Founding price ends tonight, 11:59 PM ET" + EMAIL E11 (morning)', 'Feed + Reel + Stories x3 + email', 'Enrollments'),
 ('2027-02-01', 'Close-out: "Founding enrollment has closed. Membership is now $69.99. Thank you, Founding Members."', 'Feed + Stories', 'Brand; only after price change verified live'),
]
CADENCE = [
 ('Instagram feed/carousel', '5-7 per week (daily Nov 23-30)', '11:30 ET', 'Mix: 40% membership, 30% product/gifting, 30% brand/education'),
 ('Instagram Reels', '3 per week', '18:30 ET', 'Reuse to FB Reels, TikTok, YouTube Shorts'),
 ('Instagram + Facebook Stories', 'Daily, 2-4 frames', '09:00 and 19:30 ET', 'Polls/quizzes + link sticker to the day\'s destination'),
 ('Facebook feed', 'Mirror IG feed (5-7/week)', '12:00 ET', 'Direct UTM links in caption'),
 ('TikTok', '3-4 per week', '19:00 ET', 'Native hooks; photo carousels for education'),
 ('YouTube Shorts', '2-3 per week', '17:00 ET', 'Same vertical videos'),
 ('Threads', '3-4 per week', '09:30 ET', 'Text-led; conversational'),
 ('X', '3 per week', '10:00 ET', 'Short + link; post natively (Metricool X is a paid add-on)'),
 ('Pinterest', 'Only if an account exists (not among the six confirmed)', '20:00 ET', 'Gift guide + soap/coffee pins'),
 ('Email (opted-in only)', '6 sends Nov 27-Dec 28; 5 in January', '10:00 ET', 'Each send needs Jeff\'s explicit approval'),
]
DECISIONS = [
 'Approve the campaign spine: Teaser (Nov 20-22) -> Reveal Mon Nov 23 -> Black Friday Nov 27, or hold everything until Nov 27.',
 'Choose primary vs backup for the Reveal (A04 / ALT-A04-1 / ALT-A04-2), Black Friday (B01 / ALT-B01-2) and Cyber Monday (B04 / ALT-B04-1).',
 'Gift purchases: may members buy gifts at member price? Terms say "personal use by one account". Until you decide, gift content shows everyday prices only.',
 'Bundle push: the bundle app\'s free plan allows 50 bundle orders/month. OK to feature the $79.99 Build Your Own bundle in Dec 6 stocking-stuffer content?',
 'Holiday shipping: approve or decline an "order by" date (currently only the policy timing is stated, no guarantee).',
 'Filming: who records the checkout walkthrough and "first cart" reels (needs a real member account; Claude cannot sign in or buy).',
 'Testosterone & NAD+ Support: kept out of campaign creative until Quantus documentation and claims review clear. Confirm.',
 'Email: confirm the opted-in subscriber segment and approve each send (6 in Nov-Dec).',
 'Paid ads: remain on hold (purchase tracking + CA/NC geo-exclusion unverified). Revisit after Restructuring evidence.',
]

wb = Workbook(); hdr = Font(bold=True, color='FFFFFF'); fill = PatternFill('solid', fgColor='2A422A')
def sheet(ws, header, data, widths=None):
    ws.append(header)
    for c in ws[1]: c.font = hdr; c.fill = fill; c.alignment = Alignment(vertical='top', wrap_text=True)
    for d in data: ws.append(d)
    ws.freeze_panes = 'A2'; ws.auto_filter.ref = ws.dimensions
    for i, h in enumerate(header, 1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(h, 18)
    for row in ws.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(vertical='top', wrap_text=True)
ws = wb.active; ws.title = 'Calendar Nov-Dec 2026'
sheet(ws, cols, [[r[c] for c in cols] for r in rows], {'Caption': 70, 'Title': 34, 'Hook': 34, 'Asset': 40, 'URL': 40, 'Dependencies': 46, 'Alternates': 40, 'Production': 30, 'Phase': 22})
sheet(wb.create_sheet('Pieces & manifest'), list(man[0].keys()), [list(m.values()) for m in man], {'Title': 40, 'Status': 40, 'Files': 60, 'Dependencies': 50, 'Alternates': 50})
sheet(wb.create_sheet('Backup concepts'), ['File', 'For', 'Direction'], [[a, a.split('-')[1] if a.count('-') > 1 else '', a] for a in alts], {'File': 50, 'Direction': 50})
sheet(wb.create_sheet('January 2027 roadmap'), ['Date', 'Moment', 'Formats', 'Objective'], JAN, {'Moment': 70, 'Formats': 40})
sheet(wb.create_sheet('Platform cadence'), ['Channel', 'Frequency', 'Initial time (assumption)', 'Notes'], CADENCE, {'Channel': 28, 'Frequency': 34, 'Notes': 60})
sheet(wb.create_sheet('Decisions for Jeff & Esther'), ['#', 'Decision'], [[i + 1, d] for i, d in enumerate(DECISIONS)], {'Decision': 120})
wb.save(OUT/'EverLiv-Founding-Members-Master-Calendar.xlsx')
json.dump(dict(manifest=man, alternates=alts, templates=tmpl, jan=JAN, cadence=CADENCE, decisions=DECISIONS), open(OUT/'manifest.json', 'w'), indent=1)
c = {}
for m in man: k = m['Status'].split(':')[0]; c[k] = c.get(k, 0) + 1
print(len(rows), 'calendar rows;', len(man), 'pieces;', c, '; alts', len(alts), '; templates', len(tmpl))
