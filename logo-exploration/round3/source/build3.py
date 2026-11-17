# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marks3 import svg, CSS as MCSS, WORDMARK
from content3 import C, FAMILIES, TOP5

NM = "node_modules/@fontsource/"
FONT_CSS = ["italiana/400.css", "cormorant-garamond/400.css", "cormorant-garamond/400-italic.css", "cormorant-garamond/500.css", "cormorant-garamond/600.css",
            "bodoni-moda/400.css", "josefin-sans/300.css", "gilda-display/400.css", "montserrat/400.css", "montserrat/500.css", "montserrat/600.css",
            "jost/400.css", "tenor-sans/400.css", "cinzel/400.css", "cinzel/700.css",
            "heebo/hebrew-300.css", "heebo/hebrew-400.css", "heebo/hebrew-500.css", "heebo/hebrew-700.css", "heebo/300.css", "heebo/400.css", "heebo/500.css", "heebo/700.css",
            "frank-ruhl-libre/hebrew-500.css", "frank-ruhl-libre/hebrew-700.css", "frank-ruhl-libre/500.css"]
CRIT = ["יוקרה", "פשטות", "אמינות", "גמישות בגדלים", "ייחודיות"]
BYN = {c["n"]: c for c in C}

_LAT = r"[A-Za-zΦ][A-Za-zΦ0-9'’\-\.&+: ]*[A-Za-zΦ0-9+]|[A-Za-zΦ]"
_NUM = r"[+€]*\d[\d,\.:]*(?:M\+|M|\+)?"
_BOTH = re.compile(_NUM + "|" + _LAT)
def bd(t):
    out = []
    for p in re.split(r"(<[^>]+>)", t):
        if p.startswith("<"): out.append(p); continue
        out.append(_BOTH.sub(lambda m: f'<bdi dir="ltr">{m.group(0)}</bdi>' if re.search(r"[A-Za-zΦ+€:]", m.group(0)) else m.group(0), p))
    return "".join(out)

CSS = MCSS + r"""
@page { size: 297mm 210mm; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
html, body { background: #f4efe7 }
body { font-family: Heebo, sans-serif; direction: rtl; -webkit-print-color-adjust: exact; print-color-adjust: exact; color:#151311 }
bdi { white-space: nowrap }
.ltr { direction: ltr }
:root { --gold:#c7a466; --goldd:#a7844b; --muted:#8b8274; --line:#ddd4c5 }
.page { width: 297mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; background:#f4efe7 }
.pd { background:#0d0c0b; color:#efe7d6 }
.run { position:absolute; top: 9mm; left: 14mm; right: 14mm; display:flex; justify-content:space-between; font-size: 6.6pt; letter-spacing:.3em; font-family: Montserrat; font-weight:500; opacity:.55 }
.run .r { font-family: Heebo; letter-spacing:.03em; font-size: 7.8pt }
.foot { position:absolute; bottom: 7mm; left: 14mm; right: 14mm; display:flex; justify-content:space-between; font-size: 6.4pt; letter-spacing:.26em; font-family: Montserrat; opacity:.45 }
h1, h2 { font-family: 'Frank Ruhl Libre', serif; font-weight:500 }
.heb { font-size: 8.6pt; font-weight:500; color: var(--goldd) }
.pd .heb { color: var(--gold) }
p { font-size: 9.6pt; line-height: 1.65 }
.lk { display:flex; flex-direction:column; align-items:center; direction:ltr; text-align:center }
.lk .w1, .lk .w2 { white-space:nowrap; color: var(--fg); line-height:1 }
.lk .w2 { opacity:.72 }
.lk .tg { font-family: Montserrat; font-weight:500; color: var(--ac); white-space:nowrap }
.cp { position:absolute; top: 17mm; left: 14mm; right: 14mm; bottom: 13mm; display:grid; grid-template-columns: 84mm 1fr; gap: 9mm }
.vis { display:grid; grid-template-rows: 1fr 38mm; gap: 4mm; min-height:0 }
.heros { display:grid; grid-template-columns: 1fr 1fr; gap: 4mm; min-height:0 }
.hero { position:relative; display:flex; align-items:center; justify-content:center; background: var(--bg) }
.hero .lbl, .tile .lbl { position:absolute; top: 3mm; right: 3.5mm; font-size: 6.2pt; opacity:.45 }
.tiles { display:grid; grid-template-columns: 1fr 1fr 1.15fr 1.5fr; gap: 4mm }
.tile { position:relative; display:flex; align-items:center; justify-content:center; background: var(--bg); color: var(--fg) }
.appic { width: 19mm; height: 19mm; border-radius: 4.4mm; background:#0d0c0b; display:flex; align-items:center; justify-content:center; box-shadow: 0 1mm 2.6mm rgba(0,0,0,.28) }
.sizes { display:flex; align-items:flex-end; gap: 4.5mm; direction:ltr }
.sizes div { display:flex; flex-direction:column; align-items:center; gap: 1.3mm; font-family: Montserrat; font-size: 5.2pt; opacity:.55 }
.bcard { width: 46mm; height: 27mm; background:#0d0c0b; box-shadow: 0 1.6mm 4mm rgba(0,0,0,.3); display:flex; align-items:center; justify-content:center; transform: rotate(-4deg) }
.txt { display:flex; flex-direction:column }
.num { font-family: 'Cormorant Garamond'; font-weight:400; font-size: 46pt; line-height:.8; color: var(--goldd); direction:ltr; text-align:right }
.num small { font-family: Montserrat; font-size: 7.4pt; letter-spacing:.2em; color: var(--muted); margin-right: 2mm }
.en { font-family: Montserrat; font-weight:500; font-size: 7.6pt; letter-spacing:.34em; direction:ltr; text-align:right; margin-top: 4mm; color:#4a443b }
.he { font-size: 21pt; line-height:1.15; margin-top: 1.2mm }
.chip { align-self:flex-start; margin-top: 2mm; font-size: 7.4pt; color: var(--muted); border:1px solid var(--line); border-radius: 20px; padding: .4mm 2.8mm }
.wow { margin-top: 4mm; font-family:'Frank Ruhl Libre'; font-weight:500; font-size: 11.4pt; line-height:1.45; border-right: 2px solid var(--gold); padding-right: 3mm }
.sec { margin-top: 3mm }
.sec h4 { font-size: 7.8pt; font-weight:700; color: var(--goldd); margin-bottom: .4mm }
.sec p { font-size: 8.9pt; line-height:1.55 }
.deb { margin-top: 3.2mm; background:#ebe4d8; padding: 2.4mm 3mm; font-size: 8.3pt; line-height:1.5 }
.deb .v { margin-top: 1mm }
.scores { margin-top:auto; display:grid; gap: 1mm }
.sc { display:grid; grid-template-columns: 22mm 1fr 8mm; align-items:center; gap: 2mm; font-size: 7.5pt; color:#4a443b }
.bar { height: 2px; background: var(--line); position:relative }
.bar i { position:absolute; right:0; top:0; bottom:0; background: #b8955a }
.sc .v { font-family: Montserrat; font-weight:500; font-size: 7.2pt; direction:ltr; text-align:left }
.tot { display:flex; justify-content:space-between; border-top:1px solid var(--line); margin-top: 1mm; padding-top: 1.3mm; font-size: 8.2pt; font-weight:700 }
.tot .v { font-family: Montserrat; color: var(--goldd); direction:ltr }
.badge { position:absolute; top: 3mm; left: 3.5mm; font-family: Montserrat; font-weight:500; font-size: 6pt; letter-spacing:.28em; color: var(--ac); border: 1px solid var(--ac); padding: .7mm 2.2mm; direction:ltr }
"""

def lockup(c, s=1.0, tag=True):
    fam, wt, tr, tr2 = c["font"]
    t = (f'<div class="tg" style="font-size:{1.7*s}mm;letter-spacing:.5em;margin-top:{5*s}mm;margin-right:-.5em">THE STANDARD YOU DESERVE</div>' if tag else "")
    if c["n"] in WORDMARK:
        return f'<div class="lk">{svg(c["n"], f"{68*s}mm")}{t}</div>'
    style = "font-style:italic;" if False else ""
    return (f'<div class="lk">{svg(c["n"], f"{30*s}mm")}'
            f'<div class="w1" style="margin-top:{7*s}mm;font-family:\'{fam}\';font-weight:{wt};font-size:{9.6*s}mm;letter-spacing:{tr}em;margin-right:-{tr}em">ALMA</div>'
            f'<div class="w2" style="font-family:\'{fam}\';font-weight:{wt};font-size:{3.1*s}mm;letter-spacing:{tr2}em;margin-right:-{tr2}em;margin-top:{2.6*s}mm">GROUP</div>{t}</div>')

def run(txt):
    return f'<div class="run"><span class="ltr">ALMA GROUP · ROUND 3 · SIMPLE LUXURY</span><span class="r">{txt}</span></div>'
def foot(pg):
    return f'<div class="foot"><span class="ltr">CONFIDENTIAL · NOVEMBER 2026</span><span class="ltr">{pg:02d}</span></div>'

def concept(c, pg):
    n = c["n"]; fam = FAMILIES[c["fam"]]; tot = sum(c["scores"])
    rank = TOP5.index(n) + 1 if n in TOP5 else None
    sc = "".join(f'<div class="sc"><span>{CRIT[i]}</span><div class="bar"><i style="width:{v*10}%"></i></div><span class="v">{v}/10</span></div>' for i, v in enumerate(c["scores"]))
    badge = f'<div class="badge">TOP {rank}</div>' if rank else ""
    return f"""
<section class="page">{run(f"משפחה {fam[0]} · {fam[1]}")}
<div class="cp">
 <div class="txt">
  <div class="num">{n:02d}<small>/ 30</small></div>
  <div class="en">{c["en"]}</div>
  <h2 class="he">{c["he"]}</h2>
  <span class="chip">משפחה {fam[0]}: {fam[1]}</span>
  <div class="wow">{bd(c["wow"])}</div>
  <div class="sec"><h4>הרעיון</h4><p>{bd(c["idea"])}</p></div>
  <div class="sec"><h4>המשמעות</h4><p>{bd(c["meaning"])}</p></div>
  <div class="deb"><b>פרקליט השטן:</b> {bd(c["con"])}<div class="v"><b>הכרעת הצוות:</b> {bd(c["verdict"])}</div></div>
  <div class="scores">{sc}<div class="tot"><span>ציון כולל</span><span class="v">{tot}/50</span></div></div>
 </div>
 <div class="vis">
  <div class="heros">
   <div class="hero th-light" style="background:#ebe4d8"><span class="lbl">רקע בהיר</span>{lockup(c, 0.8)}</div>
   <div class="hero th-dark"><span class="lbl">רקע כהה</span>{badge}{lockup(c, 0.8)}</div>
  </div>
  <div class="tiles">
   <div class="tile th-monol" style="background:#e9e2d6"><span class="lbl">אייקון</span><div class="appic th-dark">{svg(n, "13mm")}</div></div>
   <div class="tile th-mono"><span class="lbl">צבע אחד</span>{svg(n, "22mm")}</div>
   <div class="tile th-light"><span class="lbl">מבחן גודל</span><div class="sizes"><div>{svg(n,"48px")}48px</div><div>{svg(n,"32px")}32px</div><div>{svg(n,"16px")}16px</div></div></div>
   <div class="tile th-light" style="background:#cfc6b8"><span class="lbl">כרטיס ביקור</span><div class="bcard th-dark">{lockup(c, 0.36, tag=False)}</div></div>
  </div>
 </div>
</div>{foot(pg)}</section>"""

def cover():
    grid = "".join(f'<div class="cv">{svg(n, "15mm")}</div>' for n in range(1, 31))
    return f"""
<section class="page pd th-dark">
 <div style="position:absolute;inset:0;display:grid;grid-template-columns:1fr 1fr">
  <div style="display:flex;flex-direction:column;justify-content:center;align-items:center;border-left:1px solid #24201b">
   <div class="ltr" style="font-family:Montserrat;font-weight:500;font-size:6.6pt;letter-spacing:.5em;color:#c7a466;margin-right:-.5em">ROUND 3 · SIMPLE LUXURY</div>
   <div class="ltr" style="font-family:Italiana;font-size:36pt;letter-spacing:.3em;margin:10mm -.3em 0 0">ALMA</div>
   <div class="ltr" style="font-family:Montserrat;font-weight:500;font-size:7.4pt;letter-spacing:.8em;opacity:.7;margin:3mm -.8em 0 0">GROUP</div>
   <div style="width:14mm;height:1px;background:#c7a466;margin:11mm 0"></div>
   <h1 style="font-size:24pt;color:#f3ebdb;text-align:center;line-height:1.25">30 סמלים פשוטים<br>שמשדרים יוקרה</h1>
   <p style="margin-top:4mm;color:#9f9583;font-size:9.6pt;text-align:center;max-width:100mm">קו אחד, צורה אחת, ומרווח לנשום. זו השפה של מותגי היוקרה הגדולים בעולם.</p>
  </div>
  <div style="padding:22mm 20mm;display:grid;grid-template-columns:repeat(5,1fr);gap:5mm;align-content:center;direction:ltr">{grid}</div>
 </div>
 <style>.cv{{aspect-ratio:1;display:flex;align-items:center;justify-content:center}}</style>
</section>"""

def brief(pg):
    pr = [("פחות זה יותר", "כל אלמנט מיותר מוריד יוקרה. כל סמל כאן בנוי משניים-שלושה רכיבים לכל היותר."),
          ("קו דק, זהב אחד", "קווים עדינים בצבע אחד וזהב רק בנקודה אחת: הסף, הידית, הגג."),
          ("מרווח לנשום", "המקום הריק סביב הסמל הוא חלק מהיוקרה. לא ממלאים, לא מקשטים."),
          ("טיפוגרפיה מושלמת", "ברוב מותגי היוקרה השם עצמו הוא הלוגו. לכן משפחה שלמה כאן היא לוגוטייפ בלבד.")]
    return f"""
<section class="page">{run("הבריף")}
<div style="position:absolute;top:22mm;left:14mm;right:14mm;bottom:16mm;display:grid;grid-template-columns:1fr 1fr;gap:16mm">
 <div>
  <span class="heb">מה שמענו ממך</span>
  <h2 style="font-size:27pt;line-height:1.2;margin-top:2mm">פשוט. קל.<br>ויוקרתי.</h2>
  <p style="margin-top:5mm">הסבב הקודם היה מורכב מדי: אשליות, תלת-ממד ופרטים רבים. הבריף עכשיו ברור: סמל פשוט וקליל, שמשדר יוקרה במבט אחד, כמו המותגים הגדולים של עולם האופנה, התכשיטים והמלונאות.</p>
  <p style="margin-top:3mm">כל 30 הכיוונים כאן בנויים מקו אחד או מצורה אחת, בשחור, שנהב וזהב. בלי אתונה ובלי האותיות AG.</p>
  <div style="margin-top:8mm;display:grid;grid-template-columns:repeat(3,1fr);gap:4mm">
   {"".join(f'<div class="th-dark" style="background:#0d0c0b;aspect-ratio:1;display:flex;align-items:center;justify-content:center">{svg(n,"20mm")}</div>' for n in (1,18,8))}
  </div>
 </div>
 <div>
  <span class="heb">ארבעה עקרונות</span>
  <div style="margin-top:3mm;display:grid;gap:3.6mm">
   {"".join(f'<div style="display:grid;grid-template-columns:13mm 1fr;gap:3mm;border-top:1px solid var(--line);padding-top:3.4mm"><div class="ltr" style="font-family:Cormorant Garamond;font-size:20pt;color:var(--goldd);line-height:1">0{i}</div><div><div style="font-weight:700;font-size:10.6pt">{a}</div><div style="font-size:9pt;color:#4a443b;line-height:1.55;margin-top:.6mm">{b}</div></div></div>' for i,(a,b) in enumerate(pr,1))}
  </div>
  <div style="margin-top:6mm;font-size:8.6pt;color:#6a6255;line-height:1.6">בכל עמוד: גרסה על רקע בהיר ועל רקע כהה, אייקון, צבע אחד, מבחן גודל וכרטיס ביקור. הציון מבוסס על חמישה מבחנים: יוקרה, פשטות, אמינות, גמישות בגדלים וייחודיות.</div>
 </div>
</div>{foot(pg)}</section>"""

def index(pg):
    rows = ""
    for f in range(1, 6):
        fam = FAMILIES[f]
        cells = "".join(f'<div><div class="ixs">{svg(c["n"], "17mm")}</div><div class="ixt"><span class="ltr" style="font-family:Montserrat;color:#a7844b">{c["n"]:02d}</span> {c["he"]}{" ★" if c["n"] in TOP5 else ""}</div></div>' for c in C if c["fam"] == f)
        rows += f'<div class="ixr"><div><div style="font-weight:700;font-size:9.6pt">{fam[1]}</div><div class="ltr" style="font-family:Montserrat;font-size:6pt;letter-spacing:.24em;color:#8b8274;text-align:right;margin-top:.6mm">{fam[2]}</div></div>{cells}</div>'
    return f"""
<section class="page">{run("מפת הכיוונים")}
<style>.ixr{{display:grid;grid-template-columns:30mm repeat(6,1fr);gap:3.4mm;align-items:center;margin-top:2.4mm}}
.ixs{{height:23.5mm;display:flex;align-items:center;justify-content:center;background:#0d0c0b;--bg:#0d0c0b;--fg:#efe7d6;--ac:#c7a466}}
.ixt{{font-size:7.3pt;margin-top:1mm;white-space:nowrap;overflow:hidden}}</style>
<div style="position:absolute;top:16mm;left:14mm;right:14mm;bottom:12mm">
 <div style="display:flex;justify-content:space-between;align-items:baseline"><h2 style="font-size:18pt">30 כיוונים בחמש משפחות</h2><span style="font-size:8pt;color:#8b8274">★ = חמשת המומלצים</span></div>
 {rows}
</div>{foot(pg)}</section>"""

def divider(f, pg):
    fam = FAMILIES[f]; cs = [c for c in C if c["fam"] == f]
    marks = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:4mm">{svg(c["n"], "30mm")}<span class="ltr" style="font-family:Montserrat;font-size:6pt;letter-spacing:.3em;opacity:.45">{c["n"]:02d}</span></div>' for c in cs)
    return f"""
<section class="page pd th-dark">
 <div style="position:absolute;top:0;bottom:0;right:0;width:100mm;padding:24mm 16mm;display:flex;flex-direction:column;justify-content:center;border-left:1px solid #24201b">
  <div class="ltr" style="font-family:'Cormorant Garamond';font-size:50pt;color:#c7a466;text-align:right;line-height:1">{fam[0]}</div>
  <div class="ltr" style="font-family:Montserrat;font-weight:500;font-size:6.6pt;letter-spacing:.44em;opacity:.5;text-align:right;margin-top:4mm">{fam[2]}</div>
  <h1 style="font-size:28pt;margin-top:4mm;color:#f3ebdb">{fam[1]}</h1>
  <p style="margin-top:4mm;color:#a59b88;font-size:10pt">{fam[3]}</p>
 </div>
 <div style="position:absolute;top:0;bottom:0;left:0;width:197mm;display:grid;grid-template-columns:repeat(3,1fr);align-content:center;row-gap:16mm;padding:16mm 12mm;direction:ltr">{marks}</div>
</section>"""

def ranking(pg):
    srt = sorted(C, key=lambda c: (-sum(c["scores"]), c["n"]))
    def row(c):
        return (f'<tr{" class=top" if c["n"] in TOP5 else ""}><td class="ltr n">{c["n"]:02d}</td><td class="s th-light">{svg(c["n"], "7.5mm")}</td><td>{c["he"]}</td>'
                + "".join(f'<td class="ltr v">{v}</td>' for v in c["scores"]) + f'<td class="ltr t">{sum(c["scores"])}</td></tr>')
    def table(rs):
        return '<table><thead><tr><th>#</th><th></th><th>כיוון</th>' + "".join(f"<th>{k}</th>" for k in CRIT) + '<th>סה"כ</th></tr></thead><tbody>' + "".join(row(c) for c in rs) + "</tbody></table>"
    return f"""
<section class="page">{run("טבלת הערכה")}
<style>table{{width:100%;border-collapse:collapse;font-size:7.6pt}} th{{font-weight:500;color:#8b8274;font-size:6.4pt;padding:1mm .5mm;border-bottom:1px solid #151311;text-align:center}}
td{{padding:.45mm .8mm;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}} td:nth-child(3){{text-align:right}}
td.n{{font-family:Montserrat;color:#a7844b}} td.v{{font-family:Montserrat}} td.t{{font-family:Montserrat;font-weight:600}}
td.s{{background:transparent;padding:.2mm}} tr.top td{{background:#e8dfcf}} tr.top td.t{{color:#a7844b}}</style>
<div style="position:absolute;top:16mm;left:14mm;right:14mm;bottom:12mm">
 <h2 style="font-size:18pt">כל 30 הכיוונים, מדורגים</h2>
 <p style="font-size:8.4pt;color:#8b8274;margin-top:.5mm">השורות המודגשות הן חמשת הכיוונים המומלצים.</p>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:9mm;margin-top:3mm">{table(srt[:15])}{table(srt[15:])}</div>
</div>{foot(pg)}</section>"""

WHY = {
    1: "הסמל הכי מאוזן בסבב: יוקרתי, פשוט, אדריכלי ושייך לעולם הבית. קו אחד וסף זהב מספרים את כל הסיפור: הכניסה לבית החדש. עובד בכל גודל, בהטבעה, בחריטה ובשלט.",
    18: "מלבן ונקודה, ושום דבר מעבר. כל אחד מבין מיד: דלת לבית. ידית הזהב היא הסטנדרט.",
    2: "חור מנעול בקו זהב: פרטיות, בלעדיות ומפתח לבית. נראה כמו תכשיט.",
    25: "בלי סמל בכלל: השם בגופן מעודן ונקודת זהב. הכיוון הבטוח והיוקרתי ביותר, כמו בתי האופנה.",
    8: "סהר זהב אחד: רך, אלגנטי ומעורר רגש, כמו מלון בוטיק.",
}

def recommend(pg):
    top = [BYN[n] for n in TOP5]; first = top[0]
    cards = "".join(
        f'<div><div class="th-dark" style="background:#0d0c0b;height:30mm;display:flex;align-items:center;justify-content:center;position:relative">'
        f'<span class="ltr" style="position:absolute;top:2mm;right:2.5mm;font-family:Montserrat;font-size:5.8pt;letter-spacing:.24em;color:#c7a466">#{i+2}</span>{svg(c["n"], "21mm")}</div>'
        f'<div style="font-weight:700;font-size:9.2pt;margin-top:1.8mm"><span class="ltr" style="font-family:Montserrat;font-weight:500;color:#a7844b">{c["n"]:02d}</span> {c["he"]}</div>'
        f'<div style="font-size:7.9pt;line-height:1.45;color:#3a342b;margin-top:.5mm">{bd(WHY[c["n"]])}</div></div>' for i, c in enumerate(top[1:]))
    return f"""
<section class="page">{run("ההמלצה")}
<div style="position:absolute;top:17mm;left:14mm;right:14mm;bottom:13mm;display:grid;grid-template-columns:1fr 1.1fr;gap:10mm">
 <div class="th-dark" style="background:#0d0c0b;display:flex;align-items:center;justify-content:center;position:relative"><div class="badge" style="left:auto;right:3.5mm">#1 · RECOMMENDED</div>{lockup(first, 1.15)}</div>
 <div style="display:flex;flex-direction:column">
  <span class="heb">ההמלצה של הצוות</span>
  <h2 style="font-size:24pt;line-height:1.15;margin-top:1mm">כיוון 01: הקשת</h2>
  <p style="margin-top:3mm;font-size:10pt;line-height:1.7">{bd(WHY[1])}</p>
  <p style="margin-top:2.5mm;font-size:10pt;line-height:1.7">כדאי לבחון אותה יחד עם הגומחה (12), הגרסה המלאה שלה: <b>הקשת בקו</b> לדפוס, לשילוט ולמסמכים, <b>והגומחה המלאה</b> לאייקון ולגדלים קטנים.</p>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3.4mm;margin-top:auto">{cards}</div>
 </div>
</div>{foot(pg)}</section>"""

MOCK = """
.wall{position:relative;overflow:hidden;background: radial-gradient(ellipse 70% 60% at 50% 30%, rgba(255,245,225,.55), transparent 65%), linear-gradient(170deg,#d9d2c6,#c4bbad 60%,#b2a999)}
.wall .joint{position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(0,0,0,.06) 0 .4mm, transparent .4mm 34mm)}
.brass svg{filter: drop-shadow(.8mm 1.2mm 1mm rgba(0,0,0,.35))}
.brass .t{font-family:'Cormorant Garamond';font-weight:500;color:#9b7a43;text-shadow:.4mm .6mm .8mm rgba(0,0,0,.3);direction:ltr;white-space:nowrap}
.desk{position:relative;overflow:hidden;background: radial-gradient(ellipse at 30% 20%, #ece6dc, #d6cdbf 60%, #c2b8a8)}
.card{position:absolute;width:62mm;height:37mm;box-shadow:0 2.4mm 6mm rgba(0,0,0,.25),0 .5mm 1mm rgba(0,0,0,.2)}
.night{position:relative;overflow:hidden;background: radial-gradient(ellipse at 50% 30%, #2a241c, #0d0c0b 70%)}
"""

def mock_main(pg):
    c = BYN[TOP5[0]]; fam, wt, tr, tr2 = c["font"]
    return f"""
<section class="page">{run("בעולם האמיתי · כיוון 01")}
<style>{MOCK}</style>
<div style="position:absolute;top:17mm;left:14mm;right:14mm;bottom:13mm;display:grid;grid-template-columns:1.5fr 1fr;grid-template-rows:1fr 1fr;gap:4mm">
 <div class="wall brass th-light" style="grid-row:1/3;display:flex;flex-direction:column;align-items:center;justify-content:center;--fg:#9b7a43;--ac:#9b7a43">
  <div class="joint"></div>
  {svg(c["n"], "46mm")}
  <div class="t" style="font-size:11mm;letter-spacing:.34em;margin:8mm -.34em 0 0">ALMA</div>
  <div class="t" style="font-size:3.4mm;letter-spacing:.62em;margin:2.6mm -.62em 0 0">GROUP</div>
  <div style="position:absolute;bottom:3mm;right:4mm;font-size:6.4pt;color:#5a5246">אותיות פליז על קיר אבן בלובי</div>
 </div>
 <div class="desk">
  <div class="card th-dark" style="background:#0d0c0b;top:6mm;left:6mm;transform:rotate(-6deg);display:flex;align-items:flex-start;justify-content:flex-start;padding:5mm 6mm">{svg(c["n"], "15mm")}</div>
  <div class="card th-light" style="background:#f6f1e9;top:38mm;left:38mm;transform:rotate(4deg);display:flex;align-items:center;justify-content:center">{lockup(c, 0.42, tag=False)}</div>
  <div style="position:absolute;bottom:3mm;right:4mm;font-size:6.4pt;color:#5a5246">כרטיס ביקור: הטבעת זהב</div>
 </div>
 <div class="night th-dark" style="display:flex;flex-direction:column;align-items:center;justify-content:center">
  {lockup(c, 0.62)}
  <div style="position:absolute;bottom:3mm;right:4mm;font-size:6.4pt;opacity:.5">שלט אתר בנייה</div>
 </div>
</div>{foot(pg)}</section>"""

def mock_others(pg):
    cells = ""
    for n in TOP5[1:]:
        c = BYN[n]
        cells += f"""
 <div style="display:grid;grid-template-rows:1fr 46mm auto;gap:3mm">
  <div class="night th-dark" style="display:flex;align-items:center;justify-content:center">{lockup(c, 0.6)}</div>
  <div class="desk"><div class="card th-dark" style="background:#0d0c0b;width:52mm;height:31mm;top:7mm;left:50%;margin-left:-26mm;transform:rotate(-4deg);display:flex;align-items:center;justify-content:center">{lockup(c, 0.3, tag=False)}</div></div>
  <div style="font-size:8.6pt;font-weight:700"><span class="ltr" style="font-family:Montserrat;font-weight:500;color:#a7844b">{n:02d}</span> {c["he"]}</div>
 </div>"""
    return f"""
<section class="page">{run("בעולם האמיתי · החלופות המובילות · שלט אתר וכרטיס ביקור")}
<style>{MOCK}</style>
<div style="position:absolute;top:17mm;left:14mm;right:14mm;bottom:13mm;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm">{cells}</div>
{foot(pg)}</section>"""

def next_steps(pg):
    st = [("בחירה", "בחירת 2–3 כיוונים, מומלץ מתוך חמשת המובילים."),
          ("ליטוש", "פרופורציות סופיות, עובי קו מדויק לכל גודל, ולוגוטייפ בהתאמה אישית."),
          ("מבחן שטח", "הדמיות על שלטי אתר, לובי, כרטיסים, אתר ורשתות."),
          ("ספר מותג", "מדריך שימוש, צבעים, גופנים ותבניות לכל המסמכים.")]
    return f"""
<section class="page pd th-dark">{run("השלבים הבאים")}
<div style="position:absolute;top:20mm;left:14mm;right:14mm;bottom:16mm;display:grid;grid-template-columns:1fr 1fr;gap:16mm">
 <div>
  <span class="heb">מכאן ממשיכים</span>
  <h2 style="font-size:24pt;margin-top:2mm;color:#f3ebdb">מ-30 כיוונים ללוגו אחד</h2>
  <div style="margin-top:6mm;display:grid;gap:3.6mm">
   {"".join(f'<div style="display:grid;grid-template-columns:13mm 1fr;gap:3mm;border-top:1px solid #2a251f;padding-top:3.4mm"><div class="ltr" style="font-family:Cormorant Garamond;font-size:20pt;color:#c7a466;line-height:1">0{i}</div><div><div style="font-weight:700;font-size:10.6pt">{a}</div><div style="font-size:9pt;opacity:.7;line-height:1.55;margin-top:.6mm">{b}</div></div></div>' for i,(a,b) in enumerate(st,1))}
  </div>
 </div>
 <div style="display:flex;align-items:center;justify-content:center">{lockup(BYN[TOP5[0]], 1.1)}</div>
</div>{foot(pg)}</section>"""

def build():
    pages = [cover()]; pg = 2
    for fn in (brief, index):
        pages.append(fn(pg)); pg += 1
    for f in range(1, 6):
        pages.append(divider(f, pg)); pg += 1
        for c in [c for c in C if c["fam"] == f]:
            pages.append(concept(c, pg)); pg += 1
    for fn in (ranking, recommend, mock_main, mock_others, next_steps):
        pages.append(fn(pg)); pg += 1
    links = "".join(f'<link rel="stylesheet" href="{NM}{f}">' for f in FONT_CSS)
    html = f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>Alma Group Logo Round 3</title>{links}<style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    open("doc3.html", "w", encoding="utf-8").write(html)
    print("pages", len(pages))

if __name__ == "__main__":
    build()
