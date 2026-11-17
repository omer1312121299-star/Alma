# -*- coding: utf-8 -*-
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from marks import svg
from theme import CSS as THEME
from content2 import C, FAMILIES, TOP5

NM = "node_modules/@fontsource/"
FONT_CSS = ["cinzel/700.css", "cormorant-garamond/600.css", "cormorant-garamond/700.css", "bodoni-moda/500.css",
            "tenor-sans/400.css", "jost/500.css", "jost/600.css", "montserrat/500.css", "montserrat/600.css", "montserrat/700.css",
            "heebo/hebrew-300.css", "heebo/hebrew-400.css", "heebo/hebrew-500.css", "heebo/hebrew-700.css",
            "heebo/300.css", "heebo/400.css", "heebo/500.css", "heebo/700.css",
            "frank-ruhl-libre/hebrew-500.css", "frank-ruhl-libre/hebrew-700.css", "frank-ruhl-libre/700.css"]
CRIT = ["אפקט וואו", "עוצמה", "יוקרה ואמינות", "גמישות בגדלים", "ייחודיות"]
BYN = {c["n"]: c for c in C}

_LAT = r"[A-Za-zͰ-ϿÖé][A-Za-zͰ-ϿÖé0-9'’\-\.&+: ]*[A-Za-zͰ-ϿÖé0-9+]|[A-Za-z]"
_NUM = r"[+€]*\d[\d,\.:]*(?:M\+|M|\+)?"
_BOTH = re.compile(_NUM + "|" + _LAT)
def bd(t):
    out = []
    for p in re.split(r"(<[^>]+>)", t):
        if p.startswith("<"): out.append(p); continue
        out.append(_BOTH.sub(lambda m: f'<bdi dir="ltr">{m.group(0)}</bdi>' if re.search(r"[A-Za-zͰ-Ͽ]|[+€:]", m.group(0)) else m.group(0), p))
    return "".join(out)

CSS = THEME + r"""
@page { size: 297mm 210mm; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
html, body { background: #0c0b0a }
body { font-family: Heebo, sans-serif; direction: rtl; -webkit-print-color-adjust: exact; print-color-adjust: exact }
bdi { white-space: nowrap }
.ltr { direction: ltr }
:root { --gold:#c9a463; --goldd:#a8844a; --ink:#0c0b0a; --paper:#f1ece3; --muted:#8a8173; --line:#d9d0c1 }
.page { width: 297mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always }
.pdark { background: #0c0b0a; color: #efe7d6 }
.plight { background: #f1ece3; color: #171512 }
.glow { background: radial-gradient(ellipse 60% 55% at 50% 42%, #2b2316 0%, #15120d 45%, #0c0b0a 75%) }
.run { position:absolute; top: 8mm; left: 13mm; right: 13mm; display:flex; justify-content:space-between; font-size: 7pt; letter-spacing:.24em; font-family: Montserrat; font-weight:500; opacity:.6 }
.run .r { font-family: Heebo; letter-spacing:.03em; font-size: 8pt }
.foot { position:absolute; bottom: 6.5mm; left: 13mm; right: 13mm; display:flex; justify-content:space-between; font-size: 6.6pt; letter-spacing:.22em; font-family: Montserrat; opacity:.5 }
h1, h2 { font-family: 'Frank Ruhl Libre', serif; font-weight:700 }
.eb { font-family: Montserrat; font-weight:600; font-size: 7pt; letter-spacing:.36em; color: var(--gold); direction:ltr; display:inline-block }
.heb { font-size: 9pt; font-weight:500; color: var(--goldd) }
.pdark .heb { color: var(--gold) }
p { font-size: 9.6pt; line-height: 1.6 }

.lk { display:flex; flex-direction:column; align-items:center; direction:ltr; text-align:center }
.lk .w1 { white-space:nowrap; color: var(--fg) }
.lk .w2 { white-space:nowrap; color: var(--fg); opacity:.75 }
.lk .tg { font-family: Montserrat; font-weight:500; color: var(--g11); white-space:nowrap }
.lkr { display:flex; align-items:center; direction:ltr }
.lkr .wm { display:flex; flex-direction:column; align-items:flex-start; line-height:1 }

/* concept page */
.cp { position:absolute; top: 15mm; left: 13mm; right: 13mm; bottom: 12mm; display:grid; grid-template-columns: 88mm 1fr; gap: 8mm }
.vis { display:grid; grid-template-rows: 1fr 40mm; gap: 3.5mm; min-height:0 }
.hero { position:relative; display:flex; align-items:center; justify-content:center; border-radius: 1.5mm; overflow:hidden }
.hero .lbl, .tile .lbl { position:absolute; top: 3mm; right: 3.5mm; font-size: 6.4pt; opacity:.5; letter-spacing:.04em }
.tiles { display:grid; grid-template-columns: 1.5fr 1fr 1fr 1.1fr; gap: 3.5mm }
.tile { position:relative; display:flex; align-items:center; justify-content:center; border-radius: 1.5mm; background: var(--bg); color: var(--fg) }
.appic { width: 21mm; height: 21mm; border-radius: 5mm; background: radial-gradient(circle at 50% 35%, #2a2217, #0c0b0a 70%); display:flex; align-items:center; justify-content:center; box-shadow: 0 1.2mm 3mm rgba(0,0,0,.35) }
.sizes { display:flex; align-items:flex-end; gap: 5mm; direction:ltr }
.sizes div { display:flex; flex-direction:column; align-items:center; gap: 1.4mm; font-family: Montserrat; font-size: 5.4pt; opacity:.6 }
.txt { display:flex; flex-direction:column; color:#171512 }
.num { font-family: Cinzel; font-weight:700; font-size: 44pt; line-height:.85; color: var(--goldd); direction:ltr; text-align:right }
.num small { font-family: Montserrat; font-size: 8pt; letter-spacing:.2em; color: var(--muted); margin-right: 2mm }
.en { font-family: Montserrat; font-weight:600; font-size: 8.4pt; letter-spacing:.3em; direction:ltr; text-align:right; margin-top: 3mm; color:#3a342b }
.he { font-size: 20pt; line-height:1.15; margin-top: 1mm }
.chip { align-self:flex-start; margin-top: 2mm; font-size: 7.6pt; color: var(--muted); border:1px solid var(--line); border-radius: 20px; padding: .5mm 2.8mm }
.wow { margin-top: 3.2mm; font-family:'Frank Ruhl Libre'; font-weight:500; font-size: 11.2pt; line-height:1.45; color:#171512; border-right: 2.5px solid var(--gold); padding-right: 3mm }
.sec { margin-top: 2.8mm }
.sec h4 { font-size: 8pt; font-weight:700; color: var(--goldd); margin-bottom: .5mm }
.sec p { font-size: 8.8pt; line-height:1.5 }
.deb { margin-top: 3mm; background:#e6dfd2; padding: 2.4mm 3mm; font-size: 8.4pt; line-height:1.48 }
.deb b { font-weight:700 }
.deb .v { margin-top: 1mm }
.fit { margin-top: 2.6mm; font-size: 8.3pt }
.fit b { color: var(--goldd) }
.scores { margin-top:auto; display:grid; gap: 1mm }
.sc { display:grid; grid-template-columns: 23mm 1fr 8mm; align-items:center; gap: 2mm; font-size: 7.6pt; color:#4a443b }
.bar { height: 3px; background: var(--line); position:relative }
.bar i { position:absolute; right:0; top:0; bottom:0; background: linear-gradient(to left, #8a6a3a, #d8b778) }
.sc .v { font-family: Montserrat; font-weight:600; font-size: 7.4pt; direction:ltr; text-align:left }
.tot { display:flex; justify-content:space-between; border-top:1px solid var(--line); margin-top: 1mm; padding-top: 1.3mm; font-size: 8.2pt; font-weight:700 }
.tot .v { font-family: Montserrat; color: var(--goldd); direction:ltr }
.badge { position:absolute; top: 3mm; left: 3.5mm; font-family: Montserrat; font-weight:600; font-size: 6.4pt; letter-spacing:.26em; color: #d9b878; border: 1px solid #b8955c; padding: .8mm 2.4mm; direction:ltr }
"""

def lockup(c, s=1.0, tag=True):
    fam, wt, tr, tr2 = c["font"]
    t = (f'<div class="tg" style="font-size:{1.9*s}mm;letter-spacing:.46em;margin-top:{4.2*s}mm;margin-right:-.46em">THE STANDARD YOU DESERVE</div>' if tag else "")
    return (f'<div class="lk">{svg(c["n"], f"{74*s}mm")}'
            f'<div class="w1" style="margin-top:{6*s}mm;font-family:\'{fam}\';font-weight:{wt};font-size:{11.5*s}mm;letter-spacing:{tr}em;margin-right:-{tr}em;line-height:1">ALMA</div>'
            f'<div class="w2" style="font-family:\'{fam}\';font-weight:{min(wt,600)};font-size:{4.1*s}mm;letter-spacing:{tr2}em;margin-right:-{tr2}em;margin-top:{2.4*s}mm">GROUP</div>{t}</div>')

def lockup_row(c, s=1.0):
    fam, wt, tr, tr2 = c["font"]
    return (f'<div class="lkr">{svg(c["n"], f"{20*s}mm")}<div class="wm" style="margin-left:{4.5*s}mm">'
            f'<div style="font-family:\'{fam}\';font-weight:{wt};font-size:{9.5*s}mm;letter-spacing:{tr}em;color:var(--fg);white-space:nowrap">ALMA</div>'
            f'<div style="font-family:\'{fam}\';font-weight:{min(wt,600)};font-size:{3.4*s}mm;letter-spacing:{tr2}em;color:var(--fg);opacity:.75;margin-top:{1.8*s}mm;white-space:nowrap">GROUP</div></div></div>')

def run(txt, dark=True):
    return f'<div class="run"><span class="ltr">ALMA GROUP · LOGO EXPLORATION · ROUND 2</span><span class="r">{txt}</span></div>'
def foot(pg):
    return f'<div class="foot"><span class="ltr">CONFIDENTIAL · NOVEMBER 2026</span><span class="ltr">{pg:02d}</span></div>'

def concept(c, pg):
    n = c["n"]; fam = FAMILIES[c["fam"]]; tot = sum(c["scores"])
    rank = TOP5.index(n) + 1 if n in TOP5 else None
    sc = "".join(f'<div class="sc"><span>{CRIT[i]}</span><div class="bar"><i style="width:{v*10}%"></i></div><span class="v">{v}/10</span></div>' for i, v in enumerate(c["scores"]))
    badge = f'<div class="badge">TOP {rank} · RECOMMENDED</div>' if rank else ""
    return f"""
<section class="page plight">{run(f"משפחה {fam[0]} · {fam[1]}")}
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
  <div class="fit"><b>מתאים במיוחד ל:</b> {bd(c["fit"])}</div>
  <div class="scores">{sc}<div class="tot"><span>ציון כולל</span><span class="v">{tot}/50</span></div></div>
 </div>
 <div class="vis">
  <div class="hero th-dark glow" style="color:var(--fg)"><span class="lbl">גרסה ראשית</span>{badge}{lockup(c, 0.92)}</div>
  <div class="tiles">
   <div class="tile th-light"><span class="lbl">רקע בהיר</span>{lockup_row(c, 0.62)}</div>
   <div class="tile th-mono"><span class="lbl">צבע אחד</span>{svg(n, "25mm")}</div>
   <div class="tile th-light" style="background:#ddd5c8"><span class="lbl">אייקון אפליקציה</span><div class="appic th-dark">{svg(n, "15mm")}</div></div>
   <div class="tile th-light"><span class="lbl">מבחן גודל</span><div class="sizes"><div>{svg(n,"48px")}48px</div><div>{svg(n,"32px")}32px</div><div>{svg(n,"16px")}16px</div></div></div>
  </div>
 </div>
</div>{foot(pg)}</section>"""

def cover():
    order = [3, 9, 1, 19, 13, 17, 6, 26, 14, 8, 11, 5, 27, 25, 7, 2, 4, 12, 28, 21, 10, 30, 16, 15, 20, 24, 23, 29, 22, 18]
    grid = "".join(f'<div class="cv">{svg(n, "21mm")}</div>' for n in order)
    return f"""
<section class="page pdark th-dark">
 <div style="position:absolute;inset:0;display:grid;grid-template-columns:118mm 1fr">
  <div style="padding:22mm 16mm;display:flex;flex-direction:column;justify-content:space-between;border-left:1px solid #2a251e">
   <div style="text-align:right"><span class="eb">ROUND 2 · BRAND MARK EXPLORATION</span></div>
   <div>
    <div class="ltr" style="font-family:Montserrat;font-weight:600;font-size:22pt;letter-spacing:.42em;text-align:right;white-space:nowrap">ALMA GROUP</div>
    <div style="height:1px;width:36mm;background:linear-gradient(to left,#c9a463,transparent);margin:7mm 0 7mm auto"></div>
    <h1 style="font-size:31pt;line-height:1.12;color:#f4ecdb">30 סמלים<br>שעוצרים את העין</h1>
    <p style="margin-top:5mm;color:#a99f8d;font-size:10.5pt;max-width:92mm">סבב שני. בלי אתונה, בלי עמודים ובלי אותיות. צורות בלתי אפשריות, אשליות אופטיות, פיסול בזהב ומתמטיקה של יוקרה.</p>
   </div>
   <div class="ltr" style="font-family:Montserrat;font-size:6.6pt;letter-spacing:.32em;color:#6f675a;text-align:right">CONFIDENTIAL · NOVEMBER 2026</div>
  </div>
  <div style="padding:13mm 12mm;display:grid;grid-template-columns:repeat(6,1fr);gap:2.4mm;align-content:center;direction:ltr">{grid}</div>
 </div>
 <style>.cv{{aspect-ratio:1;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 40%,#1c1812,#0e0d0b 70%);border:1px solid #1f1b15}}</style>
</section>"""

def brief(pg):
    pr = [("בלתי אפשרי", "צורה שהעין מנסה לפתור שוב ושוב. מה שלא מובן מיד, נחרט בזיכרון."),
          ("עומק ונפח", "סמל שנראה כאילו יצקו אותו ממתכת: אור, צל וחומר, ולא רק קו."),
          ("דיוק מתמטי", "גאומטריה מדויקת עד העשירית. שפה של מוסדות פיננסיים ושל אדריכלים."),
          ("מחווה אחת", "כל סמל עושה דבר אחד, חזק. אפשר לזהות אותו ב-16 פיקסלים ועל קיר של 6 מטר.")]
    return f"""
<section class="page plight">{run("הבריף החדש")}
<div style="position:absolute;top:18mm;left:13mm;right:13mm;bottom:14mm;display:grid;grid-template-columns:1fr 1fr;gap:12mm">
 <div>
  <span class="heb">מה שמענו ממך</span>
  <h2 style="font-size:25pt;line-height:1.15;margin-top:1.5mm">לא סמל שמסביר.<br>סמל שעוצר.</h2>
  <p style="margin-top:4mm">הכיוון הקודם היה נכון אסטרטגית אבל צפוי: עמודים, מקדשים ואתונה. הבריף החדש ברור: צורה מיוחדת שמי שרואה אותה אומר "וואו". צורה שאין לאף חברה אחרת, ושמשדרת עוצמה, היקף וביטחון בלי מילה אחת.</p>
  <p style="margin-top:3mm">לכן הצוות התחיל מאפס: בלי סמלים יווניים, בלי קווי רקיע ובלי אותיות. מה שנשאר מהסבב הקודם הוא רק הפלטה: שחור עמוק וזהב, שהם נכס של המותג.</p>
  <div style="margin-top:6mm;display:grid;grid-template-columns:repeat(3,1fr);gap:3mm">
   {"".join(f'<div class="th-dark" style="background:#0c0b0a;aspect-ratio:1;display:flex;align-items:center;justify-content:center">{svg(n,"24mm")}</div>' for n in (3,9,17))}
  </div>
  <div style="font-size:7.6pt;color:var(--muted);margin-top:1.5mm">שלוש דוגמאות מהסבב: הקובייה הדו-משמעית, כוח המשיכה והקשר.</div>
 </div>
 <div>
  <span class="heb">ארבעת העקרונות של "וואו"</span>
  <div style="margin-top:3mm;display:grid;gap:3mm">
   {"".join(f'<div style="display:grid;grid-template-columns:12mm 1fr;gap:3mm;border-top:1px solid var(--line);padding-top:3mm"><div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:17pt;color:var(--goldd)">0{i}</div><div><div style="font-weight:700;font-size:11pt">{a}</div><div style="font-size:9pt;color:#4a443b;line-height:1.5;margin-top:.5mm">{b}</div></div></div>' for i,(a,b) in enumerate(pr,1))}
  </div>
  <div style="margin-top:6mm;background:#171512;color:#e9e0cf;padding:4.5mm 5mm">
   <div class="heb" style="color:#c9a463">חמשת מבחני הציון</div>
   <div style="font-size:9pt;line-height:1.6;margin-top:1.5mm">אפקט וואו · עוצמה · יוקרה ואמינות · גמישות בגדלים · ייחודיות. כל אחד מ-1 עד 10. בכל עמוד מוצגים גרסה ראשית, רקע בהיר, צבע אחד, אייקון ומבחן גודל.</div>
  </div>
 </div>
</div>{foot(pg)}</section>"""

def index(pg):
    rows = ""
    for f in range(1, 6):
        fam = FAMILIES[f]
        cells = "".join(f'<div class="ix"><div class="ixs">{svg(c["n"], "19mm")}</div><div class="ixt"><span class="ltr" style="font-family:Montserrat;font-weight:600;color:#c9a463">{c["n"]:02d}</span> {c["he"]}{" ★" if c["n"] in TOP5 else ""}</div></div>' for c in C if c["fam"] == f)
        rows += f'<div class="ixr"><div><div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:14pt;color:#c9a463;text-align:right">{fam[0]}</div><div style="font-weight:700;font-size:9.6pt">{fam[1]}</div><div style="font-size:7.2pt;opacity:.6;line-height:1.35">{fam[2]}</div></div>{cells}</div>'
    return f"""
<section class="page pdark th-dark">{run("מפת הכיוונים")}
<style>.ixr{{display:grid;grid-template-columns:32mm repeat(6,1fr);gap:3mm;align-items:center;margin-top:2.4mm}}
.ixs{{height:24.5mm;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 40%,#1e1912,#100e0c 75%);border:1px solid #1f1b15}}
.ixt{{font-size:7.4pt;margin-top:1mm;white-space:nowrap;overflow:hidden}}</style>
<div style="position:absolute;top:15mm;left:13mm;right:13mm;bottom:11mm">
 <div style="display:flex;justify-content:space-between;align-items:baseline"><h2 style="font-size:18pt">30 כיוונים בחמש משפחות</h2><span style="font-size:8pt;opacity:.6">★ = חמשת המומלצים</span></div>
 {rows}
</div>{foot(pg)}</section>"""

def divider(f, pg):
    fam = FAMILIES[f]
    cs = [c for c in C if c["fam"] == f]
    marks = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:3mm">{svg(c["n"], "38mm")}<span class="ltr" style="font-family:Montserrat;font-size:6.6pt;letter-spacing:.24em;opacity:.5">{c["n"]:02d} · {c["en"]}</span></div>' for c in cs)
    return f"""
<section class="page pdark th-dark glow">
 <div style="position:absolute;top:0;bottom:0;right:0;width:96mm;padding:22mm 14mm;display:flex;flex-direction:column;justify-content:center;border-left:1px solid #2a251e">
  <div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:56pt;color:#c9a463;text-align:right;line-height:1">{fam[0]}</div>
  <div class="ltr" style="font-family:Montserrat;font-weight:600;font-size:7.4pt;letter-spacing:.38em;opacity:.55;text-align:right;margin-top:4mm">{fam[3]}</div>
  <h1 style="font-size:27pt;margin-top:4mm;color:#f4ecdb;line-height:1.15">{fam[1]}</h1>
  <p style="margin-top:4mm;color:#b3a993;font-size:10pt">{fam[4]}</p>
  <div style="margin-top:6mm;font-size:8.4pt;opacity:.55">כיוונים {cs[0]["n"]:02d}–{cs[-1]["n"]:02d}</div>
 </div>
 <div style="position:absolute;top:0;bottom:0;left:0;width:201mm;display:grid;grid-template-columns:repeat(3,1fr);align-content:center;row-gap:12mm;padding:16mm 10mm;direction:ltr">{marks}</div>
</section>"""

def ranking(pg):
    srt = sorted(C, key=lambda c: (-sum(c["scores"]), c["n"]))
    def row(c):
        return (f'<tr{" class=top" if c["n"] in TOP5 else ""}><td class="ltr n">{c["n"]:02d}</td><td class="s th-light">{svg(c["n"], "7.5mm")}</td><td>{c["he"]}</td>'
                + "".join(f'<td class="ltr v">{v}</td>' for v in c["scores"]) + f'<td class="ltr t">{sum(c["scores"])}</td></tr>')
    def table(rs):
        return '<table><thead><tr><th>#</th><th></th><th>כיוון</th>' + "".join(f"<th>{k}</th>" for k in CRIT) + '<th>סה"כ</th></tr></thead><tbody>' + "".join(row(c) for c in rs) + "</tbody></table>"
    return f"""
<section class="page plight">{run("טבלת הערכה")}
<style>table{{width:100%;border-collapse:collapse;font-size:7.6pt}} th{{font-weight:500;color:var(--muted);font-size:6.4pt;padding:1mm .5mm;border-bottom:1px solid #171512;text-align:center}}
td{{padding:.45mm .8mm;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}} td:nth-child(3){{text-align:right}}
td.n{{font-family:Montserrat;font-weight:600;color:var(--goldd)}} td.v{{font-family:Montserrat}} td.t{{font-family:Montserrat;font-weight:700}}
td.s{{background:transparent;padding:.2mm}} tr.top td{{background:#e3d9c6}} tr.top td.t{{color:var(--goldd)}}</style>
<div style="position:absolute;top:15mm;left:13mm;right:13mm;bottom:12mm">
 <h2 style="font-size:18pt">כל 30 הכיוונים, מדורגים</h2>
 <p style="font-size:8.4pt;color:var(--muted);margin-top:.5mm">השורות המודגשות הן חמשת הכיוונים המומלצים.</p>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:3mm">{table(srt[:15])}{table(srt[15:])}</div>
</div>{foot(pg)}</section>"""

WHY = {
    3: "הסמל היחיד שקיבל 9 ומעלה בכל המבחנים. צורה מוסדית ופשוטה, כמעט קלאסית, שמסתירה אשליה שהמוח לא מפסיק לפתור. עובד מצוין ב-16 פיקסלים, ובולט על קיר של 6 מטר. מתחבר ישירות לסלוגן: The Details Are Everything.",
    9: "הכי ייחודי במסמך. אף חברת נדל\"ן בעולם לא נראית כך. מסר של מסה, כוח ומרכז: השוק נמשך אלינו.",
    1: "האשליה החזקה ביותר. עוצר כל מי שעובר מול שלט אתר. \"אנחנו בונים את מה שאחרים חושבים שאי אפשר\".",
    19: "סיפור מתמטי בלתי נשכח שמתאים בדיוק לשלושה מייסדים: כל אחד עצמאי, ויחד אי אפשר להפריד ביניהם.",
    13: "מגדל איקוני שמסתובב על צירו: שאפתנות, אדריכלות וגובה. מושלם לשלטים אנכיים ולחזיתות.",
}

def recommend(pg):
    top = [BYN[n] for n in TOP5]; first = top[0]
    cards = "".join(
        f'<div><div class="th-dark glow" style="height:33mm;display:flex;align-items:center;justify-content:center;position:relative;border-radius:1.5mm">'
        f'<span class="ltr" style="position:absolute;top:2mm;right:2.5mm;font-family:Montserrat;font-weight:600;font-size:6.2pt;letter-spacing:.2em;color:#c9a463">#{i+2}</span>{svg(c["n"], "25mm")}</div>'
        f'<div style="font-weight:700;font-size:9.4pt;margin-top:1.8mm"><span class="ltr" style="font-family:Montserrat;color:var(--goldd)">{c["n"]:02d}</span> {c["he"]}</div>'
        f'<div style="font-size:7.9pt;line-height:1.45;color:#3a342b;margin-top:.5mm">{bd(WHY[c["n"]])}</div></div>' for i, c in enumerate(top[1:]))
    return f"""
<section class="page plight">{run("ההמלצה")}
<div style="position:absolute;top:15mm;left:13mm;right:13mm;bottom:12mm;display:grid;grid-template-columns:1fr 1.1fr;gap:9mm">
 <div class="th-dark glow" style="display:flex;align-items:center;justify-content:center;position:relative;border-radius:1.5mm;color:var(--fg)"><div class="badge" style="left:auto;right:3.5mm">#1 · RECOMMENDED</div>{lockup(first, 1.08)}</div>
 <div style="display:flex;flex-direction:column">
  <span class="heb">ההמלצה של הצוות</span>
  <h2 style="font-size:23pt;line-height:1.15;margin-top:1mm">כיוון 03: הקובייה הדו-משמעית</h2>
  <p style="margin-top:2.5mm;font-size:10pt;line-height:1.65">{bd(WHY[3])}</p>
  <p style="margin-top:2.5mm;font-size:10pt;line-height:1.65"><b>החלופות המובילות</b> מכסות ארבעה כיוונים שונים: אופטי (09), בלתי אפשרי (01), שזור (19) ופיסולי (13). כל אחד מהם יכול להפוך ללוגו ראשי.</p>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:auto">{cards}</div>
 </div>
</div>{foot(pg)}</section>"""

MOCK_CSS = """
.wall { position:relative; overflow:hidden; border-radius:1.5mm;
  background: radial-gradient(ellipse 70% 60% at 50% 30%, rgba(255,240,210,.10), transparent 60%),
              repeating-linear-gradient(90deg, rgba(0,0,0,.35) 0 .5mm, transparent .5mm 46mm),
              repeating-linear-gradient(0deg, rgba(0,0,0,.35) 0 .5mm, transparent .5mm 30mm),
              linear-gradient(160deg, #3b3833, #26241f 55%, #1a1916) }
.wall .grain { position:absolute; inset:0; opacity:.35; background-image: radial-gradient(rgba(255,255,255,.05) 1px, transparent 1px); background-size: 2.4px 2.4px }
.sign svg { filter: drop-shadow(1.2mm 1.6mm 1.4mm rgba(0,0,0,.65)) }
.sign .ltxt { font-family: Montserrat; font-weight:600; color:#d8bb84; text-shadow: .5mm .8mm 1mm rgba(0,0,0,.7); direction:ltr; white-space:nowrap }
.card { position:absolute; width: 70mm; height: 42mm; border-radius: 1.2mm; box-shadow: 0 3mm 7mm rgba(0,0,0,.45), 0 .6mm 1.2mm rgba(0,0,0,.3) }
.desk { position:relative; overflow:hidden; border-radius:1.5mm; background: radial-gradient(ellipse at 30% 20%, #6b6256, #3f3a33 60%, #2c2925) }
.phone { position:absolute; width: 56mm; height: 112mm; border-radius: 8mm; background:#0b0b0b; padding: 2.2mm; box-shadow: 0 4mm 10mm rgba(0,0,0,.5) }
.phone .scr { width:100%; height:100%; border-radius: 6.2mm; background: linear-gradient(170deg, #3b3226, #17130e 60%, #0b0a08); display:grid; grid-template-columns: repeat(4,1fr); align-content:start; gap: 3.4mm; padding: 14mm 4mm }
.phone .ap { aspect-ratio:1; border-radius: 2.6mm; background: rgba(255,255,255,.08) }
.hoard { position:relative; overflow:hidden; border-radius:1.5mm; background:#0c0b0a }
"""

def mock_main(pg):
    c = BYN[TOP5[0]]
    fam, wt, tr, tr2 = c["font"]
    return f"""
<section class="page pdark th-dark">{run("בעולם האמיתי · כיוון 03")}
<style>{MOCK_CSS}</style>
<div style="position:absolute;top:15mm;left:13mm;right:13mm;bottom:12mm;display:grid;grid-template-columns:1.55fr 1fr;grid-template-rows:1fr 1fr;gap:4mm">
 <div class="wall sign" style="grid-row:1/3;display:flex;flex-direction:column;align-items:center;justify-content:center">
  <div class="grain"></div>
  {svg(c["n"], "62mm")}
  <div class="ltxt" style="font-size:10mm;letter-spacing:.42em;margin-top:7mm;margin-right:-.42em">ALMA</div>
  <div class="ltxt" style="font-size:3.6mm;letter-spacing:.7em;margin-top:2.4mm;margin-right:-.7em;opacity:.85">GROUP</div>
  <div style="position:absolute;bottom:3mm;right:4mm;font-size:6.6pt;opacity:.55">שלט מתכת על קיר בטון בכניסה לבניין</div>
 </div>
 <div class="desk">
  <div class="card th-dark" style="background:#0e0d0b;top:7mm;left:8mm;transform:rotate(-7deg);display:flex;align-items:center;justify-content:center">{svg(c["n"], "22mm")}</div>
  <div class="card" style="background:#efe9de;top:38mm;left:28mm;transform:rotate(5deg);padding:5mm 6mm;direction:ltr;color:#171512">
    <div class="th-light" style="display:flex;align-items:center;gap:3mm">{svg(c["n"], "10mm")}<div style="font-family:Montserrat;font-weight:600;font-size:3.3mm;letter-spacing:.38em;white-space:nowrap">ALMA GROUP</div></div>
    <div style="margin-top:7mm;font-family:Montserrat;font-size:2.1mm;letter-spacing:.12em;line-height:1.7;color:#4a443b">ALMAGREECE.COM<br>THE STANDARD YOU DESERVE</div>
  </div>
  <div style="position:absolute;bottom:3mm;right:4mm;font-size:6.6pt;opacity:.6">כרטיס ביקור: הטבעת זהב על נייר שחור</div>
 </div>
 <div class="desk" style="background:radial-gradient(ellipse at 70% 30%, #4a4238, #221f1b 70%)">
  <div class="phone" style="top:7mm;left:50%;transform:translateX(-50%) rotate(-4deg)"><div class="scr">
   {"".join('<div class="ap"></div>' for _ in range(5))}<div class="ap th-dark" style="background:radial-gradient(circle at 50% 35%,#2a2217,#0c0b0a 70%);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 .3mm #3a3226">{svg(c["n"], "8mm")}</div>{"".join('<div class="ap"></div>' for _ in range(10))}
  </div></div>
  <div style="position:absolute;bottom:3mm;right:4mm;font-size:6.6pt;opacity:.6">אייקון אפליקציה</div>
 </div>
</div>{foot(pg)}</section>"""

def mock_others(pg):
    cells = ""
    for n in TOP5[1:]:
        c = BYN[n]
        fam, wt, tr, tr2 = c["font"]
        cells += f"""
 <div style="display:grid;grid-template-rows:1fr 30mm;gap:2.5mm">
  <div class="hoard th-dark" style="display:flex;flex-direction:column;align-items:center;justify-content:center;background:radial-gradient(ellipse 80% 60% at 50% 40%,#2b2316,#0c0b0a 70%)">
   {svg(n, "34mm")}
   <div style="font-family:'{fam}';font-weight:{wt};font-size:5.4mm;letter-spacing:{tr}em;margin-right:-{tr}em;margin-top:4mm;color:#efe7d6;direction:ltr">ALMA</div>
   <div style="font-family:'{fam}';font-weight:{min(wt,600)};font-size:2mm;letter-spacing:{tr2}em;margin-right:-{tr2}em;margin-top:1.4mm;color:#efe7d6;opacity:.75;direction:ltr">GROUP</div>
   <div style="font-family:Montserrat;font-size:1.6mm;letter-spacing:.42em;color:#c9a463;margin-top:4mm;direction:ltr">THE STANDARD YOU DESERVE</div>
  </div>
  <div class="wall sign" style="display:flex;align-items:center;justify-content:center;gap:4mm;direction:ltr"><div class="grain"></div>{svg(n, "14mm")}<div class="ltxt" style="font-size:3.2mm;letter-spacing:.34em">ALMA GROUP</div></div>
  <div style="font-size:8.4pt;font-weight:700"><span class="ltr" style="font-family:Montserrat;color:#c9a463">{n:02d}</span> {c["he"]}</div>
 </div>"""
    return f"""
<section class="page pdark th-dark">{run("בעולם האמיתי · החלופות המובילות · שלט אתר בנייה ושלט מתכת על קיר")}
<style>{MOCK_CSS}</style>
<div style="position:absolute;top:15mm;left:13mm;right:13mm;bottom:12mm;display:grid;grid-template-columns:repeat(4,1fr);gap:4mm">{cells}</div>
{foot(pg)}</section>"""

def next_steps(pg):
    st = [("בחירה", "בחירת 2–3 כיוונים מתוך ה-30 לפיתוח מעמיק. מומלץ מתוך חמשת המובילים."),
          ("ליטוש", "גאומטריה סופית, בניית גרסה שטוחה לכל סמל תלת-ממדי, ולוגוטייפ מצויר בהתאמה אישית."),
          ("תנועה", "אנימציית לוגו של 3 שניות לאתר, לרשתות ולסרטונים: הקובייה מתהפכת, הרשת נמשכת, המגדל מסתובב."),
          ("מבחן שטח", "הדמיות על שלט אתר, חזית בניין, מצגת משקיעים, אתר, אינסטגרם ומתנות ללקוחות."),
          ("ספר מותג", "מדריך שימוש מלא, תבניות לכל המסמכים, והטמעה בכל חומרי השיווק.")]
    return f"""
<section class="page pdark th-dark glow">{run("השלבים הבאים")}
<div style="position:absolute;top:18mm;left:13mm;right:13mm;bottom:14mm;display:grid;grid-template-columns:1fr 1fr;gap:12mm">
 <div>
  <span class="heb">מכאן ממשיכים</span>
  <h2 style="font-size:24pt;margin-top:1.5mm;color:#f4ecdb">מ-30 סמלים ללוגו אחד</h2>
  <div style="margin-top:5mm;display:grid;gap:3.2mm">
   {"".join(f'<div style="display:grid;grid-template-columns:12mm 1fr;gap:3mm;border-top:1px solid #2e2820;padding-top:3mm"><div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:16pt;color:#c9a463">0{i}</div><div><div style="font-weight:700;font-size:10.6pt">{a}</div><div style="font-size:9pt;opacity:.72;line-height:1.5;margin-top:.5mm">{b}</div></div></div>' for i,(a,b) in enumerate(st,1))}
  </div>
 </div>
 <div style="display:flex;flex-direction:column;align-items:center;justify-content:center">
  {lockup(BYN[TOP5[0]], 1.0)}
 </div>
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
    html = f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>Alma Group Logo Exploration Round 2</title>{links}<style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    open("doc2.html", "w", encoding="utf-8").write(html)
    print("pages", len(pages), "bytes", len(html))

if __name__ == "__main__":
    build()
