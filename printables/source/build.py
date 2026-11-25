"""Builds every printable for the HCAI Faculty Kick Off.

Run from anywhere:  python3 build.py
Writes the HTML sources next to this file and the print-ready PDFs to ../
Edit the lists below (names, menu questions, hunt items, meeting options)
and re-run to regenerate.
"""
import html, pathlib, subprocess, zipfile

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ---------- content ----------
PEOPLE = [
    ("Justin Cary", "Program Director, HCAI"),
    ("Kiran Budhrani", "Director of Teaching & Learning Innovation, CTL"),
    ("Hailey Stroder", "Instructional Designer & Technologist, CTL"),
    ("Jordan Register", "Instructional Designer & Technologist II, CTL"),
    ("Yash Tadimalla", "Lecturer, Computer Science"),
    ("Aileen Benedict", "Teaching Assistant Professor, Computer Science"),
    ("Jim Damron", "Lecturer, Applied Physiology, Health & Clinical Science"),
    ("Daryl Lewis", "Academic Advising & Charlotte Engineering Early College, University College"),
    ("Mary McKenzie", "Senior Lecturer, Sociology"),
]
TEACHING = ["Yash Tadimalla", "Aileen Benedict", "Jim Damron", "Daryl Lewis", "Mary McKenzie"]
HOMES = [
    "Computer Science",
    "Applied Physiology, Health & Clinical Science",
    "Sociology",
    "University College & Academic Advising",
    "Center for Teaching & Learning",
    "Somewhere else? Write it in.",
]
MENU = {
    "Appetizers": ("Easy openers", [
        "What's a piece of tech you've had a love/hate relationship with?",
        "What's the best class you ever took, and what made it great?",
        "What did you think AI would look like when you were a kid?",
    ]),
    "Entrées": ("The meatier stuff", [
        "What do your students already know about AI that you don't?",
        "Where have you seen AI go wrong in your field? What would a human-centered fix have looked like?",
        "One thing you'd never let AI do in your classroom, and one thing you'd love it to do?",
        "Which pillar from this morning are you most excited to teach? Which one makes you a little nervous?",
        "What does “human-centered” mean to you, in one sentence?",
    ]),
    "Dessert": ("Looking ahead", [
        "If this program is wildly successful in five years, what are our graduates doing?",
        "Who in this room would you like to collaborate with, and on what?",
    ]),
}
HUNT = [
    "One place a pillar from this morning already shows up",
    "One locked item and one item you can edit",
    "The HCAI AI-use / syllabus statement",
    "Where to request a change to the blueprint",
    "The accessibility checker",
    "One resource you didn't know existed and would actually use",
]
MEETING_ROWS = 5  # blank rows on the meeting-time poster

# ---------- shared look ----------
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:'
         'opsz,wght@12..96,500;12..96,700;12..96,800&family=Hanken+Grotesk:wght@400;500;600&'
         'family=JetBrains+Mono:wght@400;600&display=swap">')
BASE = """
:root{--ink:#18202E;--muted:#586174;--line:#C9CFD9;--soft:#EEF0F4;
--d1:#E39A2D;--d2:#2E58D6;--d3:#D9573F;--d4:#13887D;--d5:#8B4FA6;--note:#FFE98A;--note-ink:#3B3210;
--fd:"Bricolage Grotesque","Avenir Next",system-ui,sans-serif;--fb:"Hanken Grotesk","Helvetica Neue",system-ui,sans-serif;
--fm:"JetBrains Mono",ui-monospace,Menlo,monospace}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact}
html,body{margin:0;padding:0;background:#fff;color:var(--ink);font-family:var(--fb)}
h1,h2,h3{font-family:var(--fd);margin:0;line-height:1.05;text-wrap:balance}
p{margin:0}
.sheet{position:relative;overflow:hidden;break-after:page;display:flex;flex-direction:column}
.sheet:last-child{break-after:auto}
.eyebrow{font-family:var(--fm);letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
.dots{display:inline-flex;gap:.35em}.dots i{display:block;width:.8em;height:.8em;border-radius:50%}
.foot{display:flex;justify-content:space-between;align-items:center;font-family:var(--fm);color:var(--muted);letter-spacing:.06em}
"""
DOTS = '<span class="dots"><i style="background:var(--d1)"></i><i style="background:var(--d4)"></i><i style="background:var(--d3)"></i><i style="background:var(--d2)"></i><i style="background:var(--d5)"></i></span>'
FOOT_TXT = "HCAI Faculty Kick Off · January 7, 2027"
e = html.escape

def page(title, size, css, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{e(title)}</title>{FONTS}
<style>@page{{size:{size};margin:0}}{BASE}{css}</style></head><body>{body}</body></html>"""

def foot(size="9pt"):
    return f'<div class="foot" style="font-size:{size}"><span>{FOOT_TXT}</span>{DOTS}</div>'

docs = {}

# 1. Still Wondering poster (tabloid portrait)
docs["01-still-wondering-poster"] = page("Still Wondering", "11in 17in", """
.sheet{width:11in;height:17in;padding:.7in}
.top{display:flex;justify-content:space-between;align-items:flex-start}
h1{font-size:132pt;font-weight:800;letter-spacing:-.035em;line-height:.88;margin-top:.35in}
h1 span{color:var(--d2)}
.sub{font-size:20pt;max-width:8.2in;margin-top:.3in;line-height:1.35}
.board{flex:1;margin:.45in 0 .35in;border:3px dashed var(--line);border-radius:.25in;
background-image:radial-gradient(var(--line) 1.6px,transparent 1.8px);background-size:.5in .5in;background-position:.25in .25in;
display:flex;align-items:flex-end;justify-content:flex-end;padding:.3in}
.board p{font-family:var(--fm);font-size:12pt;color:var(--muted);letter-spacing:.08em}
""", f"""<section class="sheet">
<div class="top"><span class="eyebrow" style="font-size:12pt">Parking lot · open all day</span>{DOTS.replace('class="dots"','class="dots" style="font-size:22pt"')}</div>
<h1>Still<br>wondering<span>?</span></h1>
<p class="sub">Stick a question here anytime. CTL answers the Canvas questions near the end of their hour, and everything else gets an owner before we leave.</p>
<div class="board"><p>ONE QUESTION PER STICKY NOTE</p></div>
{foot("11pt")}
</section>""")

# 2. Where are you coming from? (tabloid portrait)
tiles = "".join(
    f'<div class="tile" style="--c:var(--d{i % 5 + 1})"><i></i><h3>{e(h)}</h3></div>'
    for i, h in enumerate(HOMES))
docs["02-where-are-you-coming-from-poster"] = page("Where Are You Coming From", "11in 17in", """
.sheet{width:11in;height:17in;padding:.7in}
h1{font-size:92pt;font-weight:800;letter-spacing:-.03em;line-height:.92;margin-top:.25in}
.sub{font-size:20pt;margin-top:.25in;color:var(--muted)}
.grid{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:.3in;margin:.5in 0 .35in}
.tile{border:3px solid var(--c);border-radius:.25in;padding:.3in;display:flex;flex-direction:column;gap:.18in;
background:color-mix(in srgb,var(--c) 6%,#fff)}
.tile i{display:block;width:.42in;height:.42in;border-radius:50%;background:var(--c)}
.tile h3{font-size:24pt;font-weight:700;line-height:1.1}
.tile:last-child{border-style:dashed;background:#fff}
""", f"""<section class="sheet">
<span class="eyebrow" style="font-size:12pt">Say hello · 11:20</span>
<h1>Where are you coming from?</h1>
<p class="sub">Put a sticker on your home base. Then go find someone from a different box.</p>
<div class="grid">{tiles}</div>
{foot("11pt")}
</section>""")

# 3. Pillars brainstorm prompt (tabloid portrait)
docs["03-pillars-brainstorm-prompt-poster"] = page("Pillars Prompt", "11in 17in", """
.sheet{width:11in;height:17in;padding:.7in;background:#fff}
.note{flex:1;margin:.5in .2in .5in;background:var(--note);color:var(--note-ink);padding:.8in .75in;transform:rotate(-1.2deg);
box-shadow:0 .08in .25in rgba(0,0,0,.18);display:flex;flex-direction:column;justify-content:center;gap:.4in}
.note p{font-family:var(--fd);font-weight:700;font-size:58pt;line-height:1.08;letter-spacing:-.015em}
.note p em{font-style:normal;display:block;padding-left:.6in;color:#6b5a12}
.rules{display:grid;grid-template-columns:repeat(3,1fr);gap:.25in;margin-bottom:.35in}
.rules div{border-top:4px solid var(--d4);padding-top:.12in}
.rules b{font-family:var(--fd);font-size:30pt;display:block}
.rules span{font-size:14pt;color:var(--muted)}
""", f"""<section class="sheet">
<span class="eyebrow" style="font-size:12pt">Shared vision · silent brainstorm</span>
<div class="note"><p>By the time a student finishes the HCAI program, they should be able to…<em>care about…</em><em>have experienced…</em></p></div>
<div class="rules"><div><b>1 idea</b><span>per sticky note</span></div><div><b>5–7</b><span>notes each</span></div><div><b>8 min</b><span>no talking yet</span></div></div>
{foot("11pt")}
</section>""")

# 4. Tight / Loose headers (3 x letter landscape)
TL = [
    ("Tight", "Every HCAI course does this", "d4", 0.0),
    ("In between", "Every course touches this, its own way", "d4", 0.5),
    ("Loose", "Your course, your call", "d4", 1.0),
]
tl_pages = ""
for label, head, c, pos in TL:
    tl_pages += f"""<section class="sheet" style="--fill:{[.9,.45,.08][int(pos*2)]}">
<div class="row"><span class="eyebrow" style="font-size:13pt">{e(label)}</span>
<div class="spec"><span>TIGHT</span><div class="bar"><i style="left:{pos*100}%"></i></div><span>LOOSE</span></div></div>
<h1>{e(head)}</h1>
{foot("10pt")}
</section>"""
docs["04-tight-loose-wall-headers"] = page("Tight Loose Headers", "11in 8.5in", """
.sheet{width:11in;height:8.5in;padding:.6in .7in;justify-content:space-between;
background:color-mix(in srgb,var(--d4) calc(var(--fill)*22%),#fff)}
.row{display:flex;justify-content:space-between;align-items:center}
h1{font-size:76pt;font-weight:800;letter-spacing:-.03em;line-height:.98;max-width:9.4in}
.spec{display:flex;align-items:center;gap:.15in;font-family:var(--fm);font-size:10pt;color:var(--muted);letter-spacing:.1em}
.bar{position:relative;margin:0 .2in;width:2.6in;height:.08in;border-radius:1in;background:linear-gradient(90deg,var(--d4),#d9dee6)}
.bar i{position:absolute;top:50%;width:.32in;height:.32in;border-radius:50%;background:var(--ink);border:.05in solid #fff;transform:translate(-50%,-50%)}
""", tl_pages)

# 5. Course map (tabloid landscape)
rows = "".join(f'<tr><th><b>{e(n)}</b><span class="line"></span></th>' + "<td></td>" * 6 + "</tr>" for n in TEACHING)
rows += "".join('<tr><th><span class="line"></span><span class="line"></span></th>' + "<td></td>" * 6 + "</tr>" for _ in range(2))
heads = "".join(f'<th class="ph"><span>Pillar {i}</span><span class="line"></span></th>' for i in range(1, 7))
docs["05-course-map-poster"] = page("Course Map", "17in 11in", """
.sheet{width:17in;height:11in;padding:.6in .7in}
.top{display:flex;justify-content:space-between;align-items:flex-end;gap:.5in}
h1{font-size:60pt;font-weight:800;letter-spacing:-.03em}
.sub{font-size:16pt;color:var(--muted);max-width:5.2in;text-align:right}
table{flex:1;width:100%;border-collapse:separate;border-spacing:0;margin:.4in 0 .3in;table-layout:fixed}
th,td{border-right:2px solid var(--line);border-bottom:2px solid var(--line)}
tr>*:last-child{border-right:0}
thead th{border-bottom:4px solid var(--ink)}
tbody tr:last-child>*{border-bottom:0}
th.corner{width:3.4in;text-align:left;vertical-align:bottom;padding:.12in;font-family:var(--fm);font-size:10pt;color:var(--muted);letter-spacing:.1em;font-weight:400}
th.ph{padding:.12in .15in;text-align:left;vertical-align:bottom;height:1.2in;background:color-mix(in srgb,var(--d4) 9%,#fff)}
th.ph span:first-child{font-family:var(--fm);font-size:10pt;color:var(--d4);letter-spacing:.08em;text-transform:uppercase;display:block}
tbody th{text-align:left;padding:.12in;font-weight:400;vertical-align:middle}
tbody th b{font-family:var(--fd);font-size:17pt;display:block}
.line{display:block;border-bottom:1.5px solid var(--line);height:.34in}
th.ph .line{border-color:var(--d4)}
""", f"""<section class="sheet">
<div class="top"><div><span class="eyebrow" style="font-size:11pt">Shared vision · course map</span><h1>Where does your course meet each pillar?</h1></div>
<p class="sub">Write your course on your row. Put a spirit-color dot in every box where your course hits that pillar.</p></div>
<table><thead><tr><th class="corner">FACULTY + COURSE</th>{heads}</tr></thead><tbody>{rows}</tbody></table>
{foot("10pt")}
</section>""")

# 6. Conversation menu (letter portrait)
courses = ""
for k, (tag, qs) in MENU.items():
    items = "".join(f"<li>{e(q)}</li>" for q in qs)
    courses += f'<div class="course"><div class="ch"><h2>{e(k)}</h2><span class="eyebrow">{e(tag)}</span></div><ul>{items}</ul></div>'
docs["06-conversation-menu"] = page("Conversation Menu", "8.5in 11in", """
.sheet{width:8.5in;height:11in;padding:.55in .7in;border:0}
.frame{flex:1;border:2px solid var(--ink);outline:1px solid var(--ink);outline-offset:-.09in;padding:.5in .55in;display:flex;flex-direction:column;gap:.34in}
.mast{text-align:center;display:grid;gap:.06in;justify-items:center}
.mast h1{font-size:52pt;font-weight:800;letter-spacing:-.025em}
.mast p{font-size:11pt;color:var(--muted)}
.course{display:grid;gap:.12in}
.ch{display:flex;align-items:baseline;gap:.15in;border-bottom:1.5px solid var(--ink);padding-bottom:.05in}
.ch h2{font-size:22pt;font-weight:700}
.ch .eyebrow{font-size:8pt}
ul{list-style:none;margin:0;padding:0;display:grid;gap:.11in}
li{font-size:13pt;line-height:1.35;display:flex;gap:.14in}
li::before{content:"";flex:none;width:.1in;height:.1in;border-radius:50%;background:var(--d3);margin-top:.08in}
.swap{margin-top:auto;background:color-mix(in srgb,var(--d3) 10%,#fff);border-radius:.08in;padding:.13in .2in;font-size:11pt;line-height:1.4}
.swap b{font-family:var(--fd)}
""", f"""<section class="sheet"><div class="frame">
<div class="mast">{DOTS}<h1>Food for Thought</h1><p>Today's conversation menu. Order anything. Seconds encouraged.</p></div>
{courses}
<p class="swap"><b>Around 1:10</b> · Grab a cookie, refill your coffee, and come back to a seat next to someone new.</p>
</div></section>""")

# 7. Scavenger hunt (letter portrait, 2-up)
hunt_items = "".join(f'<li><span class="box"></span><span class="t">{e(h)}</span><span class="star">☆</span></li>' for h in HUNT)
half = f"""<div class="half">
<div class="hd"><div><span class="eyebrow">Canvas Hub · in pairs · 20 min</span><h1>Blueprint scavenger hunt</h1></div>{DOTS}</div>
<div class="names"><span>Pair</span><i></i><span>&amp;</span><i></i></div>
<div class="colhd"><span>Find it</span><span>Confusing? Star it</span></div>
<ol>{hunt_items}</ol>
</div>"""
docs["07-blueprint-scavenger-hunt"] = page("Blueprint Scavenger Hunt", "8.5in 11in", """
.sheet{width:8.5in;height:11in;padding:0}
.half{height:5.5in;padding:.45in .6in;display:flex;flex-direction:column;gap:.14in}
.half:first-child{border-bottom:1.5px dashed var(--muted)}
.hd{display:flex;justify-content:space-between;align-items:flex-start}
.hd .eyebrow{font-size:8pt}
h1{font-size:25pt;font-weight:800;letter-spacing:-.02em;margin-top:.05in}
.names{display:flex;align-items:flex-end;gap:.12in;font-size:10.5pt;color:var(--muted)}
.names i{flex:1;border-bottom:1.5px solid var(--line);height:.25in}
.colhd{display:flex;justify-content:space-between;font-family:var(--fm);font-size:7.5pt;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);border-bottom:1.5px solid var(--ink);padding-bottom:.04in}
ol{list-style:none;margin:0;padding:0;display:grid;gap:0}
li{display:flex;align-items:center;gap:.16in;padding:.085in 0;border-bottom:1px solid var(--line);font-size:11.5pt}
.box{width:.2in;height:.2in;border:2px solid var(--d2);border-radius:.04in;flex:none}
.t{flex:1}
.star{font-size:15pt;color:var(--muted)}
""", f'<section class="sheet">{half}{half}</section>')

# 8. Meeting times (tabloid portrait)
mrows = "".join('<div class="mrow"><div class="cell"></div><div class="cell"></div><div class="cell"></div><div class="cell"></div><div class="dotzone"></div></div>' for _ in range(MEETING_ROWS))
docs["08-meeting-times-poster"] = page("Meeting Times", "11in 17in", """
.sheet{width:11in;height:17in;padding:.7in}
h1{font-size:96pt;font-weight:800;letter-spacing:-.03em;line-height:.92;margin-top:.25in}
.sub{font-size:20pt;color:var(--muted);margin-top:.25in}
.tbl{flex:1;display:flex;flex-direction:column;margin:.45in 0 .35in}
.mrow,.hrow{display:grid;grid-template-columns:1.3fr 1.3fr 1.3fr 1.3fr 2.2fr;gap:.18in}
.hrow{font-family:var(--fm);font-size:11pt;letter-spacing:.1em;color:var(--muted);border-bottom:4px solid var(--ink);padding-bottom:.08in}
.mrow{flex:1;border-bottom:2px solid var(--line);padding:.15in 0}
.cell{border-bottom:1.5px dashed var(--line)}
.dotzone{border-radius:.15in;background:color-mix(in srgb,var(--d5) 9%,#fff)}
""", f"""<section class="sheet">
<span class="eyebrow" style="font-size:12pt">Wrap-up · semester check-ins</span>
<h1>When should we check in?</h1>
<p class="sub">Dot every option that works for you. Most dots wins.</p>
<div class="tbl"><div class="hrow"><span>DAY</span><span>TIME</span><span>HOW OFTEN</span><span>WHERE</span><span>DOTS</span></div>{mrows}</div>
{foot("11pt")}
</section>""")

# 9. Name tents (letter landscape, fold in half)
def tent_face(name, role):
    nm = f"<h1>{e(name)}</h1>" if name else '<span class="blank"></span>'
    rl = f"<p>{e(role)}</p>" if role else '<span class="blank sm"></span>'
    return f'<div class="face"><div class="txt">{nm}{rl}</div><div class="ring"><span>spirit<br>color</span></div></div>'
tents = "".join(
    f'<section class="sheet"><div class="flip">{tent_face(n, r)}</div><div class="fold"><span>FOLD</span></div>{tent_face(n, r)}</section>'
    for n, r in PEOPLE + [("", ""), ("", "")])
docs["09-name-tents"] = page("Name Tents", "11in 8.5in", """
.sheet{width:11in;height:8.5in;padding:0}
.flip{transform:rotate(180deg);height:4.25in}
.face{height:4.25in;padding:.55in .75in;display:flex;align-items:center;justify-content:space-between;gap:.5in}
.txt{display:grid;gap:.12in;flex:1}
.face h1{font-size:50pt;font-weight:800;letter-spacing:-.025em}
.face p{font-size:15pt;color:var(--muted);max-width:6.4in;line-height:1.3}
.blank{display:block;border-bottom:2px solid var(--line);height:.9in;width:6.5in}
.blank.sm{height:.4in;width:5in}
.ring{flex:none;width:1.25in;height:1.25in;border-radius:50%;border:2.5px dashed var(--muted);display:grid;place-items:center;text-align:center}
.ring span{font-family:var(--fm);font-size:8pt;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);line-height:1.3}
.fold{height:0;border-top:1px dashed var(--line);position:relative}
.fold span{position:absolute;right:.3in;top:-.07in;background:#fff;padding:0 .08in;font-family:var(--fm);font-size:7pt;color:var(--muted);letter-spacing:.15em}
""", tents)

# 10. Exit cards (letter portrait, 4-up)
card = f"""<div class="card"><div class="hd"><span class="eyebrow">Before you go</span>{DOTS}</div>
<p class="q">One word for how you're feeling about the semester</p><i class="ln"></i>
<p class="q">One thing you'll try in your course</p><i class="ln"></i><i class="ln"></i><i class="ln"></i></div>"""
docs["10-exit-cards"] = page("Exit Cards", "8.5in 11in", """
.sheet{width:8.5in;height:11in;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}
.card{padding:.5in .45in;display:flex;flex-direction:column;gap:.12in}
.card:nth-child(odd){border-right:1.5px dashed var(--muted)}
.card:nth-child(-n+2){border-bottom:1.5px dashed var(--muted)}
.hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:.1in}
.hd .eyebrow{font-size:8pt}
.q{font-family:var(--fd);font-weight:700;font-size:15pt;line-height:1.15;margin-top:.12in}
.ln{display:block;border-bottom:1.5px solid var(--line);height:.38in}
""", f'<section class="sheet">{card*4}</section>')

# ---------- build ----------
pdfs = []
for name, doc in docs.items():
    src = HERE / f"{name}.html"
    src.write_text(doc, encoding="utf-8")
    pdf = OUT / f"{name}.pdf"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", src.as_uri()],
                   check=True, capture_output=True)
    pdfs.append(pdf)
    print("built", pdf.name)

with zipfile.ZipFile(OUT / "hcai-kickoff-printables.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in pdfs:
        z.write(p, p.name)
print("zipped", len(pdfs), "files")
