#!/usr/bin/env python3
"""Generate original comic-editorial SVG artwork for a GitHub profile.
No third-party packages required; assets render as GitHub README images.
Edit profile.config.json for profile copy, links, projects, social profiles.
"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'assets'
C = json.loads((ROOT / 'profile.config.json').read_text())
INK='#101017'; RED='#ef3d41'; CREAM='#f7f1e6'; LIME='#c8ff4f'; MUTED='#57575e'; WHITE='#ffffff'
FONT="'DejaVu Sans','Arial',sans-serif"
MONO="'DejaVu Sans Mono','Courier New',monospace"

def esc(s): return escape(str(s),quote=True)
def svg(body,w=1080,h=180,title='Harun Nur Rasyid profile art',defs='',css=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="svgtitle">'
            f'<title id="svgtitle">{esc(title)}</title><defs>{defs}</defs>'
            f'<style>{css}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>{body}</svg>\n')
def txt(x,y,t,size=20,fill=INK,weight=700,mono=False,extra=''):
    return f'<text x="{x}" y="{y}" fill="{fill}" font-family="{MONO if mono else FONT}" font-size="{size}" font-weight="{weight}" {extra}>{esc(t)}</text>'
def rect(x,y,w,h,fill,rx=0,stroke=None,sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'
def polygon(points,fill,stroke=None,sw=2):
    return f'<polygon points="{points}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'
def dots(pid='dots',c=INK,op='.15',step=14,r=2):
    return f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse"><circle cx="{step/2}" cy="{step/2}" r="{r}" fill="{c}" opacity="{op}"/></pattern>'
def paper_grid():
    return '<pattern id="grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M25 0H0V25" fill="none" stroke="#101017" stroke-opacity=".06" stroke-width="1"/></pattern>'
def write(file,body,w=1080,h=180,title='',defs='',css=''):
    p=A/file;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(svg(body,w,h,title or str(file),defs,css),encoding='utf-8')
def header(file,index,title,subtitle,accent=RED):
    b=rect(0,0,1080,96,INK)+polygon('0,0 54,0 80,96 0,96',accent)
    b+=rect(48,14,110,68,CREAM,3)+txt(65,59,index,36,INK,900,True)
    b+=txt(184,58,title,38,CREAM,900)+txt(185,81,subtitle,14,LIME,700,True)
    b+=polygon('951,0 1080,0 1080,96 979,96',accent)
    b+=txt(991,61,'✦',40,INK,900,False)
    b+=f'<path d="M940 10l18 20-18 20" fill="none" stroke="{CREAM}" stroke-width="5"/>'
    write(file,b,1080,96,f'{index} {title}')

# About: paper + black strip + original comic accent
b=rect(0,0,1080,206,CREAM)+rect(0,0,1080,206,'url(#grid)')
b+=rect(0,0,13,206,RED)+txt(43,38,'01 / ABOUT THE BUILDER',18,RED,900,True)
b+=txt(44,92,"I build backends that don't",38,INK,900)+txt(44,139,'fall apart when life gets messy.',36,INK,900)
b+=txt(45,181,'Reliability  /  systems thinking  /  thoughtful AI engineering',18,MUTED,700,True)
b+=f'<g transform="translate(910 93) rotate(11)">{polygon("-70,-54 70,-54 70,54 -70,54",RED,INK,5)}{txt(-52,-11,"BUILD.",22,CREAM,900)}{txt(-52,23,"LEARN.",22,CREAM,900)}</g>'
write('about.svg',b,1080,206,'About Harun — building reliable systems',paper_grid())

header('section-projects.svg','02','SELECT TARGETS','FEATURED ENGINEERING PROJECTS',RED)
header('section-focus.svg','03','WHAT I CARE ABOUT','PRINCIPLES & CURRENT FOCUS',LIME)
header('section-writing.svg','04','THE IDEA LOG','WRITING & TECH NOTES',RED)
header('section-stack.svg','05','MY TOOLBOX','PRACTICAL TOOLS, NOT A COLLECTIBLE BADGE WALL',LIME)
header('section-connect.svg','06','LET\'S CONNECT','COLLABORATE / READ / SAY HELLO',RED)

projects = C['projects']
for i,p in enumerate(projects):
    ptitle=p['title'].upper();slug=p['slug'];tag=p['tag'].upper();desc=p['description'];number=f'{i+1:02d}'
    bg=[CREAM,RED,LIME][i%3];fg=INK
    b=rect(0,0,1080,168,bg)+rect(0,0,1080,168,'url(#dotpat)')
    b+=rect(0,0,17,168,INK)+rect(31,24,78,76,INK)
    b+=txt(42,79,number,40,LIME,900,True)
    b+=txt(138,76,ptitle,57,INK,900)
    b+=txt(141,118,desc,19,INK,600)
    b+=rect(843,28,193,43,INK,5)+txt(865,57,tag,17,CREAM,900,True)
    b+=f'<path d="M972 111h45m-18-18 18 18-18 18" fill="none" stroke="{INK}" stroke-width="7"/>'
    b+=rect(139,139,210,5,INK)
    write(f'projects/{slug}.svg',b,1080,168,f'{ptitle}: {desc}',dots('dotpat',INK,'.12',17,2))

# Three-column focus canvas
focus=[('01','DESIGN FOR','FAILURE','Idempotency, retries, backoff and safer boundaries.'),
       ('02','MAKE IT','OBSERVABLE','Tracing, evidence and decisions you can explain.'),
       ('03','HUMANS +','AI','Faster delivery without surrendering judgment.')]
b=rect(0,0,1080,258,CREAM)+rect(0,0,1080,258,'url(#grid)')
for i,(n,a,c,d) in enumerate(focus):
    x=20+i*355; bg=[INK,RED,INK][i]
    b+=rect(x,20,332,217,bg,5)
    b+=rect(x+18,20,59,39,LIME)+txt(x+29,48,n,22,INK,900,True)
    b+=txt(x+20,100,a,28,CREAM,900)+txt(x+20,132,c,28,LIME if i!=1 else CREAM,900)
    # shortened, deliberately 2 lines with measured widths
    texts=[('Idempotency, retries,','and safer boundaries.'),('Tracing, evidence,','explainable decisions.'),('Move faster, keep','human judgment.')][i]
    b+=txt(x+21,175,texts[0],17,CREAM,500)+txt(x+21,198,texts[1],17,CREAM,500)
write('focus.svg',b,1080,258,'Engineering focus: reliable design, observability, human-AI collaboration',paper_grid())

# Writing cards: short labels keep guaranteed fit
for i,p in enumerate(C['articles']):
    bg=[CREAM,LIME,CREAM][i%3]
    b=rect(0,0,1080,93,bg)+rect(0,0,1080,93,'url(#dots)')
    b+=rect(0,0,10,93,RED)+txt(31,63,f'0{i+1}',34,INK,900,True)
    b+=rect(100,19,3,55,INK)+txt(124,55,p['label'],29,INK,900)
    b+=txt(125,78,p['topic'].upper(),13,MUTED,700,True)
    b+=txt(970,61,'↗',45,RED,900)
    write(f'writing/post-{i+1}.svg',b,1080,93,p['label'],dots('dots',INK,'.05',16,2))

# Stack: grouped tools, compact and understated
b=rect(0,0,1080,209,CREAM)+rect(0,0,1080,209,'url(#grid)')
cols=[('LANGUAGES',['GO','PYTHON','RUBY','RUST']),('DATA',['POSTGRESQL','REDIS','MYSQL','MONGODB']),('DELIVERY',['DOCKER','KUBERNETES','AWS','TERRAFORM'])]
for i,(label,tools) in enumerate(cols):
    x=24+i*353
    b+=rect(x,20,330,45,INK)+txt(x+17,50,label,23,LIME,900,True)
    for j,t in enumerate(tools):
        y=87+j*28
        b+=f'<circle cx="{x+22}" cy="{y-5}" r="5" fill="{RED if i%2==0 else INK}"/>'
        b+=txt(x+40,y,t,19,INK,800,True)
write('stack.svg',b,1080,209,'Tools and technologies',paper_grid())

# Custom SVG social buttons
socials=C['socials']
for i,s in enumerate(socials):
    bg=[INK,RED,LIME,INK][i%4]
    fg=CREAM if bg!=LIME else INK
    b=rect(0,0,255,84,bg,3)+rect(1,1,253,82,'none',3,INK,3)
    b+=txt(16,32,f'0{i+1}',14,LIME if bg!=LIME else RED,900,True)
    b+=txt(16,62,s['label'].upper(),24,fg,900,True)
    b+=f'<path d="M200 25h28m-12-12 12 12-12 12" fill="none" stroke="{fg}" stroke-width="4"/>'
    write(f'social/{s["slug"]}.svg',b,255,84,f'Visit {s["label"]}')

# Footer and animated ticker
b=rect(0,0,1080,91,INK)+rect(0,0,1080,9,RED)
b+=txt(30,62,'KEEP BUILDING.',45,CREAM,900)+txt(648,58,'THANKS FOR DROPPING BY',17,LIME,900,True)
b+=polygon('1020,15 1076,15 1076,85 1000,85',RED)+txt(1023,68,'!',53,INK,900)
write('footer.svg',b,1080,91,'Keep building — thanks for visiting')
b=rect(0,0,1080,46,RED)
b+=f'<clipPath id="cl"><rect width="1080" height="46"/></clipPath><g clip-path="url(#cl)"><g class="marq">'
phrase='  BUILD > THINK > SHIP    ✦    RELIABILITY IS A FEATURE    ✦    ENGINEERING IN PROGRESS    ✦   '
for i in range(4):b+=txt(i*770+9,32,phrase,17,INK,900,True)
b+='</g></g>'
css='@keyframes move{to{transform:translateX(-770px)}}.marq{animation:move 18s linear infinite}'
write('ticker.svg',b,1080,46,'Engineering in progress ticker',css=css)

# Generated README, all image references are local and validated below
r=[]
def add(v=''): r.append(v)
add('<!-- Generated by scripts/generate.py. Edit profile.config.json, then run python3 scripts/generate.py. -->')
add('<p align="center"><img src="assets/hero.svg" width="100%" alt="Harun Nur Rasyid — backend engineer and systems thinker" /></p>')
add('<p align="center"><img src="assets/about.svg" width="100%" alt="I build backends that do not fall apart when life gets messy" /></p>')
add('<p align="center"><img src="assets/section-projects.svg" width="100%" alt="Featured engineering projects" /></p>')
for p in projects:
    add(f'<p align="center"><a href="{esc(p["url"])}"><img src="assets/projects/{p["slug"]}.svg" width="100%" alt="{esc(p["title"])} — {esc(p["description"])}" /></a></p>')
add('<p align="center"><img src="assets/section-focus.svg" width="100%" alt="What I care about" /></p>')
add('<p align="center"><img src="assets/focus.svg" width="100%" alt="Design for failure, make systems observable, preserve human judgment when using AI" /></p>')
add('<p align="center"><img src="assets/section-writing.svg" width="100%" alt="Writing and tech notes" /></p>')
for i,p in enumerate(C['articles']):
    add(f'<p align="center"><a href="{esc(p["url"])}"><img src="assets/writing/post-{i+1}.svg" width="100%" alt="{esc(p["label"])}" /></a></p>')
add('<p align="center"><img src="assets/section-stack.svg" width="100%" alt="My toolbox" /></p>')
add('<p align="center"><img src="assets/stack.svg" width="100%" alt="Go, Python, Ruby, Rust, PostgreSQL, Redis, MySQL, MongoDB, Docker, Kubernetes, AWS and Terraform" /></p>')
add('<p align="center"><img src="assets/section-connect.svg" width="100%" alt="Connect with me" /></p>')
add('<p align="center">')
for s in socials:
    add(f'  <a href="{esc(s["url"])}"><img src="assets/social/{s["slug"]}.svg" width="24%" alt="{esc(s["label"])}" /></a>')
add('</p>')
add('<p align="center"><img src="assets/ticker.svg" width="100%" alt="Engineering in progress — build, think, ship" /></p>')
add('<p align="center"><img src="assets/footer.svg" width="100%" alt="Keep building. Thanks for dropping by" /></p>')
add('')
(ROOT/'README.md').write_text('\n'.join(r),encoding='utf-8')
import re
refs=re.findall(r'src="(assets/[^"]+)"','\n'.join(r))
missing=[q for q in refs if not (ROOT/q).is_file()]
if missing: raise SystemExit(f'Missing assets: {missing}')
print('Generated README and',len(refs),'SVG image references; all exist.')
