from pathlib import Path
from html import escape
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = Path.cwd()
WORK = ROOT / '.copilot-tracking/ppt/2026-10-13/zava-forward-agent-process'
DEST = ROOT / 'docs/capstone/deck'
CREAM, FOREST, MOSS, GOLD = '#F7F2E7', '#183A31', '#D5E2D4', '#E5B96A'
WIDTH, HEIGHT, SCALE = 1600, 900, 2
font_paths = {
    False: subprocess.check_output(['fc-match', '-f', '%{file}', 'Liberation Sans'], text=True),
    True: subprocess.check_output(['fc-match', '-f', '%{file}', 'Liberation Sans:style=Bold'], text=True),
}
image = Image.new('RGB', (WIDTH*SCALE, HEIGHT*SCALE), CREAM)
draw = ImageDraw.Draw(image)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">',
       '<title id="title">Five bounded assists in the retrofit process</title>',
       '<desc id="desc">Proposed design. Five capability cards show staff-requested help, event or scheduled review triggers, and the human decision owner. Workflow rules control progression; assistance only proposes or raises flags. Funding continues through claims and cash; hazards go directly to the human service. Intended benefits remain unmeasured.</desc>',
       f'<rect width="1600" height="900" fill="{CREAM}"/>']
checks = []

def rect(x,y,w,h,fill,r=0,stroke=None):
    box=(round(x*SCALE),round(y*SCALE),round((x+w)*SCALE),round((y+h)*SCALE))
    draw.rounded_rectangle(box, radius=round(r*SCALE), fill=fill, outline=stroke, width=SCALE)
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')

def text(x,y,lines,size=26,color=FOREST,bold=False,center=False,max_width=None):
    if isinstance(lines,str): lines=lines.split('\n')
    font=ImageFont.truetype(font_paths[bold], size*SCALE)
    for i,line in enumerate(lines):
        width=draw.textlength(line,font=font)/SCALE
        if max_width is not None:
            assert width <= max_width, (line,width,max_width)
        left=x-width/2 if center else x
        top=y+i*size*1.17
        assert 0 <= left and left+width <= WIDTH and top+size*1.2 <= HEIGHT, line
        draw.text((round(left*SCALE),round(top*SCALE)),line,font=font,fill=color,anchor='lt')
        svg.append(f'<text x="{x}" y="{top}" fill="{color}" font-family="Liberation Sans, Arial, sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" dominant-baseline="text-before-edge" text-anchor="{"middle" if center else "start"}">{escape(line)}</text>')
        checks.append({'text':line,'left':left,'top':top,'width':width,'font_px':size})

cards = [
 {'phase':'Choose homes','name':['Stock','Prioritisation'], 'request':['Explain sourced','candidate evidence'], 'proactive':['New conflicts or','missing stock facts'], 'owner':['Assets owns policy;','data owners verify'], 'full_name':'Stock Prioritisation Agent'},
 {'phase':'Assess & design','name':['Assessment','Preparation'], 'request':['Prepare a sourced','survey / design pack'], 'proactive':['Changed or stale','assessment evidence'], 'owner':['Assessor + coordinator','sign off independently'], 'full_name':'Assessment Agent'},
 {'phase':'Prepare funding','name':['Grant & Funding','Evidence'], 'request':['Draft a source-linked','application / pack'], 'proactive':['Changed terms or','missing pack inputs'], 'owner':['Finance validates,','approves and submits'], 'full_name':'Grant & Funding Agent'},
 {'phase':'Coordinate works','name':['Works & Resident','Coordination'], 'request':['Draft updates; offer','capacity-backed slots'], 'proactive':['Unaccepted handoffs;','missed update duties'], 'owner':['Resident chooses;','Programme releases'], 'full_name':'Contractor & Resident Coordination Agent'},
 {'phase':'Verify & handover','name':['Quality','Evidence Review'], 'request':['Assemble evidence','for human review'], 'proactive':['Missing or conflicting','quality evidence'], 'owner':['Independent quality','authority accepts'], 'full_name':'Quality Verification Agent'},
]
text(60,47,'PROPOSED DESIGN | BOUNDED ASSISTANCE, NOT FIVE AUTONOMOUS MANAGERS',19,bold=True,max_width=1480)
text(60,85,'Five assists. One controlled journey.',55,bold=True,max_width=1480)
text(60,155,'The workflow owns progression. People own decisions.',27,max_width=1480)
for i,card in enumerate(cards):
    x=60+i*303
    rect(x,218,267,60,FOREST,12)
    text(x+133.5,234,card['phase'],27,CREAM,True,True,max_width=245)
    if i<4:
        points=[(x+274,245),(x+293,245),(x+293,239),(x+302,248),(x+293,257),(x+293,251),(x+274,251)]
        draw.polygon([(int(a*SCALE),int(b*SCALE)) for a,b in points],fill=FOREST)
        svg.append('<polygon points="'+' '.join(f'{a},{b}' for a,b in points)+f'" fill="{FOREST}"/>')
    text(x+133.5,298,card['owner'],22,bold=True,center=True,max_width=257)
    rect(x,372,267,296,MOSS,14)
    text(x+18,392,card['name'],25,bold=True,max_width=231)
    rect(x+18,465,20,20,FOREST,10)
    text(x+28,466,'?',17,CREAM,True,True,max_width=20)
    text(x+49,465,'ON REQUEST',18,bold=True,max_width=200)
    text(x+18,494,card['request'],24,max_width=231)
    rect(x+18,566,20,20,GOLD,10)
    text(x+28,567,'!',17,FOREST,True,True,max_width=20)
    text(x+49,566,'PROACTIVE REVIEW',18,bold=True,max_width=200)
    text(x+18,595,card['proactive'],23,max_width=231)
rect(60,697,1479,56,FOREST,12)
text(799.5,712,'WORKFLOW CORE | Rights + versions + gates + approvals + audit + manual recovery',26,CREAM,True,True,max_width=1440)
text(60,772,'Proactive = permitted event / scheduled check -> draft or raise-only flag to a named human queue.',23,max_width=1480)
text(60,805,'Funding spans planning through claim / cash. A new hazard goes straight to the human safety service.',23,max_width=1480)
text(60,842,'Intended value: fewer evidence gaps, less rework, clearer handoffs. Not measured gains or deployment proof.',21,bold=True,max_width=1480)
svg.append('</svg>')
for suffix,content in [('svg','\n'.join(svg)+'\n')]:
    path=DEST/f'agents-in-retrofit-process.{suffix}'
    assert not path.exists(), path
    path.write_text(content)
path=DEST/'agents-in-retrofit-process.png'
assert not path.exists(),path
image.save(path,optimize=True)
(WORK/'research/diagram-contract.json').write_text(json.dumps({'cards':cards,'colors':{'cream':CREAM,'forest':FOREST,'moss':MOSS,'gold':GOLD},'evidence':['docs/case_study_48_addendum.md#where-agents-fit-and-where-they-do-not','docs/case_study_48_addendum.md#agentic-architecture-brief','docs/prds/zava-forward-retrofit-programme-demonstrator.md#bounded-agent-orchestration-pattern','docs/reference/research/company/agent-request-challenge.md#summary'],'status':'proposed target design; benefits unmeasured; proactive watchers not claimed deployed','trigger_boundary':'Deterministic eligibility and routing; registered permitted AI task only; invalid or failed proposals preserve state and owned manual recovery. No automatic contact, approval, work release, claim or payment.','funding_boundary':'Grant/funding evidence work spans preparation through claim and cash; reviewed funding and budget are prerequisites before work release, award is not cash.','text_geometry':checks},indent=2)+'\n')
print('Created SVG and 3200x1800 PNG; all text widths checked.')
