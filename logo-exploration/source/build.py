# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from symbols import svg
from content import C, FAMILIES, TOP5

NM = "node_modules/@fontsource/"
FONT_CSS = [
    "cinzel/600.css", "cinzel/700.css", "cormorant-garamond/600.css", "cormorant-garamond/700.css",
    "marcellus/400.css", "bodoni-moda/500.css", "tenor-sans/400.css", "jost/500.css", "jost/600.css",
    "montserrat/500.css", "montserrat/600.css", "montserrat/700.css",
    "heebo/hebrew-300.css", "heebo/hebrew-400.css", "heebo/hebrew-500.css", "heebo/hebrew-700.css",
    "heebo/300.css", "heebo/400.css", "heebo/500.css", "heebo/700.css",
    "frank-ruhl-libre/hebrew-500.css", "frank-ruhl-libre/hebrew-700.css", "frank-ruhl-libre/500.css", "frank-ruhl-libre/700.css",
]
TOTAL = 30
CRIT = ["עוצמה", "אמינות", "על-זמניות", "גמישות בגדלים", "ייחודיות"]

CSS = r"""
@page { size: 297mm 210mm; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
html, body { background: #F4F1EB }
body { font-family: Heebo, sans-serif; color: #1E1C19; direction: rtl; -webkit-print-color-adjust: exact; print-color-adjust: exact }
:root { --ink:#171614; --paper:#F4F1EB; --stone:#EBE5DA; --gold:#A88E5E; --gold2:#C2A774; --olive:#3F433C; --muted:#6F6A61; --line:#D8D0C2 }
.page { width: 297mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; background: var(--paper) }
.f{fill:var(--fg)} .a{fill:var(--ac)} .b{fill:var(--bg)} .sf{stroke:var(--fg);fill:none} .sa{stroke:var(--ac);fill:none} .sb{stroke:var(--bg);fill:none}
.dark { --bg:#171614; --fg:#F3EFE7; --ac:#B9A06F; background: var(--bg); color: var(--fg) }
.light { --bg:#ECE6DB; --fg:#171614; --ac:#9C8150; background: var(--bg); color: var(--fg) }
.olive { --bg:#3F433C; --fg:#F3EFE7; --ac:#F3EFE7; background: var(--bg); color: var(--fg) }
.paper { --bg:#F4F1EB; --fg:#171614; --ac:#9C8150 }
.ltr { direction: ltr }
bdi { white-space: nowrap }
.run { position:absolute; top: 9mm; left: 14mm; right: 14mm; display:flex; justify-content:space-between; font-size: 7.5pt; letter-spacing:.18em; color: var(--muted); font-family: Montserrat; font-weight:500 }
.run .r { font-family: Heebo; letter-spacing: .02em; font-size: 8.5pt }
.foot { position:absolute; bottom: 7mm; left: 14mm; right: 14mm; display:flex; justify-content:space-between; font-size: 7pt; color: var(--muted); letter-spacing:.16em; font-family: Montserrat }
h1,h2,h3 { font-family: 'Frank Ruhl Libre', serif; font-weight: 700 }
.eyebrow { font-family: Montserrat; font-weight:600; letter-spacing: .32em; font-size: 7.5pt; color: var(--gold); direction:ltr; display:inline-block }
.heb-eyebrow { font-weight:500; letter-spacing:.06em; font-size: 9pt; color: var(--gold) }
p { font-size: 9.6pt; line-height: 1.62 }

/* lockups */
.lk { display:flex; align-items:center; direction:ltr; color: var(--fg) }
.lk.stack { flex-direction:column; text-align:center }
.lk .wm { display:flex; flex-direction:column; line-height:1 }
.lk.row .wm { align-items:flex-start }
.lk.stack .wm { align-items:center }
.lk .w1 { white-space:nowrap }
.lk .w2 { white-space:nowrap; color: var(--fg); opacity:.82 }
.lk .tag { font-family: Montserrat; font-weight:500; color: var(--ac); white-space:nowrap }

/* concept page */
.cp-grid { position:absolute; top: 17mm; left: 14mm; right: 14mm; bottom: 13mm; display:grid; grid-template-columns: 108mm 1fr; gap: 9mm }
.txt { display:flex; flex-direction:column }
.numrow { display:flex; align-items:baseline; gap: 4mm }
.bignum { font-family: 'Cinzel'; font-weight:700; font-size: 40pt; color: var(--gold); line-height: .9; direction:ltr }
.ofn { font-family: Montserrat; font-size: 8pt; color: var(--muted); letter-spacing:.2em; direction:ltr }
.en { font-family: Cinzel; font-weight:700; font-size: 12pt; letter-spacing:.22em; color:#2A2723; direction:ltr; text-align:right; margin-top: 3mm }
.he { font-size: 21pt; margin-top: 1mm; line-height:1.15 }
.chip { display:inline-block; margin-top: 2.2mm; font-size: 8pt; color: var(--muted); border:1px solid var(--line); border-radius: 20px; padding: .6mm 3mm; align-self:flex-start }
.sec { margin-top: 3.2mm }
.sec h4 { font-size: 8.4pt; font-weight:700; color: var(--gold); letter-spacing:.04em; margin-bottom: .6mm }
.sec p { font-size: 9.1pt; line-height: 1.55 }
.debate { margin-top: 3.4mm; background: var(--stone); border-right: 2.5px solid var(--gold); padding: 2.6mm 3.2mm }
.debate h4 { font-size: 8.4pt; font-weight:700; color: #1E1C19; margin-bottom: 1mm }
.debate .con { font-size: 8.9pt; line-height:1.5; color:#5A554C; font-style: normal }
.debate .ver { font-size: 8.9pt; line-height:1.5; margin-top: 1.2mm }
.debate b { font-weight:700 }
.fit { margin-top: 3mm; font-size: 8.6pt; color:#3A3631 }
.fit b { color: var(--gold) }
.scores { margin-top:auto; padding-top: 2mm; display:grid; grid-template-columns: 1fr; gap: 1.1mm }
.sc { display:grid; grid-template-columns: 24mm 1fr 7mm; align-items:center; gap: 2mm; font-size: 7.8pt; color:#4A463F }
.bar { height: 3px; background: var(--line); position:relative }
.bar i { position:absolute; right:0; top:0; bottom:0; background: var(--ink) }
.sc .v { font-family: Montserrat; font-weight:600; font-size: 7.6pt; direction:ltr; text-align:left }
.total { display:flex; justify-content:space-between; border-top:1px solid var(--line); margin-top: 1mm; padding-top: 1.4mm; font-size: 8.2pt; font-weight:700 }
.total .v { font-family: Montserrat; color: var(--gold); direction:ltr }
.vis { display:grid; grid-template-rows: 1fr 44mm; gap: 4mm; min-height:0 }
.hero { position:relative; display:flex; align-items:center; justify-content:center }
.hero .tl { position:absolute; bottom: 5mm; left:0; right:0; text-align:center; font-family: Montserrat; font-size: 6.4pt; letter-spacing:.42em; color: var(--ac); direction:ltr }
.hero .lbl, .tile .lbl { position:absolute; top: 3.2mm; right: 4mm; font-size: 6.8pt; letter-spacing:.06em; opacity:.55 }
.tiles { display:grid; grid-template-columns: 1.45fr 1fr 1fr; gap: 4mm }
.tile { position:relative; display:flex; align-items:center; justify-content:center }
.sizes { display:flex; align-items:flex-end; gap: 6mm; direction:ltr }
.sizes div { display:flex; flex-direction:column; align-items:center; gap: 1.6mm; font-family: Montserrat; font-size: 5.6pt; color: var(--muted) }
.top-badge { position:absolute; top: 3.2mm; left: 4mm; font-family: Montserrat; font-weight:600; font-size: 6.6pt; letter-spacing:.24em; color: var(--ac); border: 1px solid var(--ac); padding: .8mm 2.2mm; direction:ltr }
"""

def lockup(c, scale=1.0, layout=None, tag=False, cls=""):
    fam, wt, tr, tr2, lay = c["font"]
    lay = layout or lay
    if lay == "stack":
        sym = 40 * scale; s1 = 20 * scale; s2 = 7.6 * scale; gap = 5 * scale
    else:
        sym = 28 * scale; s1 = 18.5 * scale; s2 = 6.6 * scale; gap = 4.6 * scale
    w1 = f'<div class="w1" style="font-family:\'{fam}\';font-weight:{wt};font-size:{s1}mm;letter-spacing:{tr}em;margin-right:-{tr}em">ALMA</div>'
    w2 = (f'<div class="w2" style="font-family:\'{fam}\';font-weight:{min(wt,600)};font-size:{s2}mm;letter-spacing:{tr2}em;'
          f'margin-top:{2.2*scale}mm;margin-right:-{tr2}em">GROUP</div>')
    t = (f'<div class="tag" style="font-size:{2.1*scale}mm;letter-spacing:.4em;margin-top:{4*scale}mm;margin-right:-.4em">THE STANDARD YOU DESERVE</div>'
         if tag else "")
    if lay == "stack":
        return (f'<div class="lk stack {cls}">{svg(c["n"], f"{sym}mm")}'
                f'<div class="wm" style="margin-top:{gap}mm">{w1}{w2}{t}</div></div>')
    return (f'<div class="lk row {cls}">{svg(c["n"], f"{sym}mm")}'
            f'<div class="wm" style="margin-left:{gap}mm">{w1}{w2}{t}</div></div>')

def run(left_extra=""):
    return (f'<div class="run"><span class="ltr">ALMA GROUP · LOGO EXPLORATION 2026</span>'
            f'<span class="r">{left_extra}</span></div>')

def foot(pg):
    return f'<div class="foot"><span class="ltr">CONFIDENTIAL · FOR INTERNAL REVIEW</span><span class="ltr">{pg:02d}</span></div>'

import re
_LAT = re.compile(r"[A-Za-zͰ-Ͽ][A-Za-zͰ-Ͽ0-9'’\-\.&+ ]*[A-Za-zͰ-Ͽ0-9+]|[A-Za-zͰ-Ͽ]")
_NUM = re.compile(r"[+€]*\d[\d,\.]*(?:M\+|M|\+)")
_BOTH = re.compile(_NUM.pattern + "|" + _LAT.pattern)
def bd(t):
    parts = re.split(r"(<[^>]+>)", t)
    out = []
    for p in parts:
        if p.startswith("<"):
            out.append(p); continue
        p = _BOTH.sub(lambda m: f'\x00{m.group(0)}\x01', p)
        out.append(p.replace("\x00", '<bdi dir="ltr">').replace("\x01", "</bdi>"))
    return "".join(out)

def concept_page(c, pg):
    c = dict(c, **{k: bd(c[k]) for k in ("idea", "sym", "con", "verdict", "fit")})
    n = c["n"]; fam = FAMILIES[c["fam"]]
    total = sum(c["scores"])
    rank = TOP5.index(n) + 1 if n in TOP5 else None
    scores = "".join(
        f'<div class="sc"><span>{CRIT[i]}</span><div class="bar"><i style="width:{v*10}%"></i></div><span class="v">{v}/10</span></div>'
        for i, v in enumerate(c["scores"]))
    badge = f'<div class="top-badge">TOP {rank} · RECOMMENDED</div>' if rank else ""
    s = f"""
<section class="page paper">{run(f"משפחה {fam[0]} · {fam[1]}")}
<div class="cp-grid">
  <div class="txt">
    <div class="numrow"><span class="bignum">{n:02d}</span><span class="ofn">/ {TOTAL}</span></div>
    <div class="en">{c["en"]}</div>
    <h2 class="he">{c["he"]}</h2>
    <span class="chip">משפחה {fam[0]}: {fam[1]} · {fam[2]}</span>
    <div class="sec"><h4>הרעיון</h4><p>{c["idea"]}</p></div>
    <div class="sec"><h4>הסמליות והסיפור</h4><p>{c["sym"]}</p></div>
    <div class="debate"><h4>מחדר הדיונים</h4>
      <div class="con"><b>פרקליט השטן:</b> {c["con"]}</div>
      <div class="ver"><b>הכרעת הצוות:</b> {c["verdict"]}</div></div>
    <div class="fit"><b>מתאים במיוחד ל:</b> {c["fit"]}</div>
    <div class="scores">{scores}<div class="total"><span>ציון כולל</span><span class="v">{total}/50</span></div></div>
  </div>
  <div class="vis">
    <div class="hero dark"><span class="lbl">גרסה ראשית · רקע כהה</span>{badge}{lockup(c, 1.0, tag=True)}</div>
    <div class="tiles">
      <div class="tile light"><span class="lbl">רקע בהיר · גרסה אופקית</span>{lockup(c, 0.5, layout="row")}</div>
      <div class="tile olive"><span class="lbl">צבע אחד</span>{svg(n, "22mm")}</div>
      <div class="tile light"><span class="lbl">מבחן גודל</span>
        <div class="sizes"><div>{svg(n, "48px")}48px</div><div>{svg(n, "32px")}32px</div><div>{svg(n, "16px")}16px</div></div></div>
    </div>
  </div>
</div>{foot(pg)}</section>"""
    return s

# ---------------- front matter ----------------
def cover():
    top = [c for c in C if c["n"] == 7][0]
    marks = "".join(f'<div class="cm">{svg(c["n"], "15mm")}</div>' for c in C)
    return f"""
<section class="page dark" style="display:grid;grid-template-columns:1fr 1fr">
  <div style="padding:20mm 18mm;display:flex;flex-direction:column;justify-content:space-between;border-left:1px solid #2E2B27">
    <div style="text-align:right"><span class="eyebrow" style="white-space:nowrap">BRAND IDENTITY · LOGO EXPLORATION</span></div>
    <div>
      <div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:26pt;letter-spacing:.24em;text-align:right;white-space:nowrap">ALMA GROUP</div>
      <div style="height:1px;background:#B9A06F;width:40mm;margin:7mm 0 7mm auto"></div>
      <h1 style="font-size:30pt;line-height:1.15;color:#F3EFE7">30 כיווני לוגו<br>לזהות חדשה</h1>
      <p style="margin-top:5mm;color:#BDB6A8;font-size:11pt;max-width:110mm">אמינות · עוצמה · היקף · ניסיון. הצעה מלאה מחדר העיצוב: מחקר, אסטרטגיה, 30 כיוונים, דיון ביקורתי על כל אחד, והמלצה.</p>
    </div>
    <div class="ltr" style="font-family:Montserrat;font-size:7pt;letter-spacing:.3em;color:#8C857A;text-align:right">ATHENS · NOVEMBER 2026 · CONFIDENTIAL</div>
  </div>
  <div style="padding:16mm 16mm;display:grid;grid-template-columns:repeat(5,1fr);grid-auto-rows:1fr;gap:3mm;align-content:center">
    {marks}
  </div>
  <style>.cm{{display:flex;align-items:center;justify-content:center;aspect-ratio:1;border:1px solid #2A2724}}</style>
</section>"""

def research(pg):
    return f"""
<section class="page paper">{run("שלב 1 · מחקר")}
<div style="position:absolute;top:18mm;left:14mm;right:14mm;bottom:14mm;display:grid;grid-template-columns:1.05fr 1fr;gap:12mm">
 <div>
  <span class="heb-eyebrow">מה למדנו מהאתר ומ-16 מסמכי השיווק</span>
  <h2 style="font-size:24pt;margin-top:1.5mm;line-height:1.15">החברה שהלוגו צריך לייצג</h2>
  <p style="margin-top:3mm">Alma Group היא קבוצת יזמות בינלאומית שבונה מאפס, בלב המשולש ההיסטורי של אתונה, בניינים עם חניון תת-קרקעי, דירות Turnkey מאובזרות במלואן, ומתחמי גג עם בריכה, ספא, סאונה, ג'קוזי, חדר כושר ונוף פתוח לאקרופוליס. החברה פועלת על הון עצמי ללא חוב חיצוני, ומוכרת למשקיעים מישראל, ארה"ב, בריטניה ואירופה.</p>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:6mm">
   {"".join(f'<div style="border-top:2px solid var(--ink);padding-top:2mm"><div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:17pt;text-align:right">{a}</div><div style="font-size:8pt;color:var(--muted);margin-top:.5mm">{b}</div></div>' for a,b in [("13+","שנים בשוק היווני"),("200+","דירות"),("13,000+","מ\"ר שנבנו"),("€70M+","היקף מכירות")])}
  </div>
  <div style="margin-top:7mm;display:grid;grid-template-columns:1fr 1fr;gap:6mm">
   <div><h4 style="font-size:9pt;color:var(--gold)">פרויקטים</h4><p style="font-size:8.8pt"><span dir="ltr" style="display:block;text-align:right">Gazi Boulevard · Specter · Utopia · Apollo · Euphoria · Playa · Gazi Vibes · Alma · Mavro · Kallergi · Galatsi</span>בשכונות גאזי, אקזרכיה-נאפולי, מטקסורגיו וגלאצי.</p></div>
   <div><h4 style="font-size:9pt;color:var(--gold)">קהל היעד</h4><p style="font-size:8.8pt">משקיעים בינלאומיים בגילאי 35–65, רובם בעלי עסקים ואנשי הייטק, שקונים נכס שני ומעלה. הם מחפשים ביטחון, שקיפות ותשואה.</p></div>
   <div><h4 style="font-size:9pt;color:var(--gold)">קול המותג</h4><p style="font-size:8.8pt"><span dir="ltr" style="display:block;text-align:right">The Standard You Deserve<br>The Details Are Everything<br>Where Soul Meets Pulse</span>הטון רשמי, פרימיום ומכוון משקיעים.</p></div>
   <div><h4 style="font-size:9pt;color:var(--gold)">ערכי ליבה</h4><p style="font-size:8.8pt">שקיפות מלאה, מקצועיות ללא פשרות, ראייה ארוכת טווח: "פרויקט שיהיה מקור לגאווה גם בעוד עשרות שנים".</p></div>
  </div>
 </div>
 <div style="display:flex;flex-direction:column">
  <span class="heb-eyebrow">אבחון הזהות הנוכחית</span>
  <div class="dark" style="margin-top:2mm;height:52mm;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:3mm">
    <svg viewBox="0 0 120 70" style="width:24mm"><path d="M8,66 L40,4 L56,36" stroke="#F3EFE7" stroke-width="4" fill="none"/><path d="M30,38 H70" stroke="#F3EFE7" stroke-width="4"/><path d="M92,22 A26,22 0 1,0 96,46 V38 H72" stroke="#F3EFE7" stroke-width="4" fill="none"/></svg>
    <div class="ltr" style="font-family:'Cormorant Garamond';font-weight:600;font-size:15pt;letter-spacing:.2em">ALMA GROUP</div>
    <div style="font-size:7pt;color:#8C857A">שחזור סכמטי של הסמל הקיים</div>
  </div>
  <div style="margin-top:4mm;display:grid;gap:2.4mm">
   {"".join(f'<div style="display:grid;grid-template-columns:5mm 1fr;gap:2mm;font-size:8.8pt;line-height:1.5"><b style="color:var(--gold);font-family:Montserrat">{i}</b><span>{t}</span></div>' for i,t in enumerate([
    "<b>מה עובד:</b> פלטת שחור, זהב-חאקי וירוק-זית עקבית מאוד בכל המסמכים, והיא נכס שכדאי לשמור. גם הסריף הקלאסי מתאים.",
    "<b>קווים דקים מדי:</b> מונוגרם ה-AG בנוי מקו דק. הוא נעלם בפאביקון, בשלט רחוק ובהטבעה, ולא משדר מסה או כוח.",
    "<b>חתימה ולא סמל:</b> שילוב אותיות A ו-G הוא פתרון נפוץ מאוד בענף, ולכן קשה להפוך אותו לנכס מזוהה ובלעדי.",
    "<b>אין סיפור:</b> הסמל לא מספר דבר על אתונה, על בנייה או על הבטחה. הזהות החדשה צריכה לעשות את כל השלושה.",
   ],1))}
  </div>
 </div>
</div>{foot(pg)}</section>"""

def strategy(pg):
    crit = [("עוצמה", "הסמל צריך לשאת משקל ויזואלי, לעמוד לבד על שלט של 6 מטר ולהיראות כמו חברה של מיליארדים."),
            ("אמינות", "שפה מוסדית ויציבה, שמשקיע שמעביר €150,000 מרגיש מולה בטוח."),
            ("על-זמניות", "רלוונטי גם בעוד 25 שנה. בלי טרנדים, בלי גרדיאנטים ובלי אפקטים."),
            ("גמישות בגדלים", "עובד ב-16 פיקסלים, בצבע אחד, בהטבעה על פליז ובחריטה על אבן."),
            ("ייחודיות", "שייך רק ל-Alma. לא עוד קו רקיע ולא עוד מונוגרם של אותיות.")]
    return f"""
<section class="page paper">{run("שלב 2 · אסטרטגיה ותהליך")}
<div style="position:absolute;top:18mm;left:14mm;right:14mm;bottom:14mm;display:grid;grid-template-columns:1fr 1fr;gap:12mm">
 <div>
  <span class="heb-eyebrow">התובנה המרכזית</span>
  <h2 style="font-size:23pt;margin-top:1.5mm;line-height:1.2">לבנות מותג שנראה כמו<br>מוסד, לא כמו סטארט-אפ</h2>
  <p style="margin-top:3mm">החברות הגדולות בעולם מזוהות לפי צורה אחת, פשוטה וכבדה, שאפשר לזהות במבט חטוף ולצייר מהזיכרון. לכן כל הכיוונים כאן נבנו מגאומטריה מלאה וכבדה, ולא מקווים דקים. הזהב משמש רק לנקודת מוקד אחת בכל סמל.</p>
  <div style="margin-top:5mm;background:var(--ink);color:#F3EFE7;padding:5mm 6mm">
   <span class="heb-eyebrow" style="color:#B9A06F">שלוש משמעויות לשם, שלוש נקודות פתיחה</span>
   <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:3mm">
    <div><div class="ltr" style="font-family:Cinzel;font-size:15pt;text-align:right">Alma</div><div style="font-size:8.4pt;color:#BDB6A8;line-height:1.5;margin-top:1mm">"נשמה" בלטינית ובספרדית: ה-<span dir="ltr">Soul</span> שבסלוגן של גאזי בולבארד.</div></div>
    <div><div class="ltr" style="font-family:Cinzel;font-size:15pt;text-align:right">Άλμα</div><div style="font-size:8.4pt;color:#BDB6A8;line-height:1.5;margin-top:1mm">"זינוק" או "קפיצה" ביוונית. השם עצמו מבטא צמיחה.</div></div>
    <div><div class="ltr" style="font-family:Cinzel;font-size:15pt;text-align:right">Alma Mater</div><div style="font-size:8.4pt;color:#BDB6A8;line-height:1.5;margin-top:1mm">"האם המזינה". מוסד שמגדל, מלווה ומחזיק.</div></div>
   </div>
  </div>
  <div style="margin-top:5mm">
   <span class="heb-eyebrow">כללי העבודה של הצוות</span>
   <p style="margin-top:1.5mm;font-size:9pt">ללא האותיות AG כמונוגרם · כל סמל חייב לעבוד בצבע אחד · כל סמל נבחן בגדלים של 48, 32 ו-16 פיקסלים · כל כיוון עבר "פרקליט שטן" שתפקידו להפיל אותו · שמירה על פלטת הצבעים הקיימת כדי שהמעבר יהיה טבעי.</p>
  </div>
 </div>
 <div>
  <span class="heb-eyebrow">חמשת מבחני ההערכה (כל אחד 1–10)</span>
  <div style="margin-top:3mm;display:grid;gap:3mm">
   {"".join(f'<div style="display:grid;grid-template-columns:10mm 1fr;gap:3mm;border-top:1px solid var(--line);padding-top:2.6mm"><div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:15pt;color:var(--gold)">0{i}</div><div><div style="font-weight:700;font-size:10.5pt">{a}</div><div style="font-size:8.8pt;color:#4A463F;line-height:1.5">{b}</div></div></div>' for i,(a,b) in enumerate(crit,1))}
  </div>
  <div style="margin-top:6mm">
   <span class="heb-eyebrow">איך לקרוא כל עמוד</span>
   <p style="margin-top:1.5mm;font-size:8.8pt">מצד שמאל: הלוגו בגרסה הראשית על רקע כהה, גרסה אופקית על רקע בהיר, גרסה בצבע אחד, ומבחן גודל. מצד ימין: הרעיון, הסמליות, הוויכוח שהתנהל עליו, השימוש המומלץ והציון.</p>
  </div>
 </div>
</div>{foot(pg)}</section>"""

def palette(pg):
    sw = [("#171614", "Athens Night", "שחור-פחם", "צבע הבסיס, הכוח"), ("#A88E5E", "Attic Gold", "זהב אטי", "נקודת המוקד, הערך"),
          ("#3F433C", "Olive Stone", "ירוק-זית", "צבע משני, שורשים"), ("#ECE6DB", "Pentelic Marble", "שיש פנטלי", "רקע, אוויר ושקט")]
    fonts = [("Cinzel", 700, "ALMA GROUP", "כתובת רומית חצובה: מוסדי, מונומנטלי"),
             ("Cormorant Garamond", 700, "ALMA GROUP", "גרמונד קלאסי: יוקרה ועידון"),
             ("Montserrat", 600, "ALMA GROUP", "גאומטרי רחב: עכשווי, תאגידי"),
             ("Marcellus", 400, "ALMA GROUP", "סריף מגולף: יווני ושקט")]
    return f"""
<section class="page paper">{run("שלב 3 · צבע וטיפוגרפיה")}
<div style="position:absolute;top:18mm;left:14mm;right:14mm;bottom:14mm">
  <span class="heb-eyebrow">פלטה: לחזק את מה שכבר קיים</span>
  <h2 style="font-size:22pt;margin-top:1.5mm">אותם צבעים, יותר החלטיות</h2>
  <p style="margin-top:2mm;max-width:200mm">הפלטה הקיימת במסמכים היא נכס. הצוות ממליץ לשמור עליה ולחדד אותה לארבעה צבעים קבועים עם שמות. הזהב מתחמם מעט כדי להיראות "זהב" ולא "חאקי" בהדפסה ובמסך.</p>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:5mm">
   {"".join(f'<div><div style="height:30mm;background:{h};border:1px solid var(--line)"></div><div class="ltr" style="font-family:Montserrat;font-weight:600;font-size:8pt;letter-spacing:.14em;margin-top:2mm;text-align:right">{e.upper()} · {h}</div><div style="font-size:9pt;font-weight:700;margin-top:.6mm">{he}</div><div style="font-size:8pt;color:var(--muted)">{d}</div></div>' for h,e,he,d in sw)}
  </div>
  <span class="heb-eyebrow" style="margin-top:8mm;display:block">משפחות טיפוגרפיות שנבדקו בכיוונים</span>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:3mm">
   {"".join(f'<div style="border-top:2px solid var(--ink);padding-top:3mm"><div class="ltr" style="font-family:\'{f}\';font-weight:{w};font-size:15pt;letter-spacing:.16em;text-align:right;white-space:nowrap">{s}</div><div class="ltr" style="font-family:Montserrat;font-size:7pt;color:var(--muted);letter-spacing:.14em;margin-top:2mm;text-align:right">{f.upper()}</div><div style="font-size:8.4pt;margin-top:1mm">{d}</div></div>' for f,w,s,d in fonts)}
  </div>
  <p style="margin-top:6mm;font-size:8.6pt;color:var(--muted)">הערה: הגופנים כאן הם גופנים פתוחים (Google Fonts) לצורך ההדגמה. בשלב הגמר, הצוות ממליץ על לוגוטייפ מצויר בהתאמה אישית (Custom Wordmark) על בסיס הכיוון שייבחר, כדי שהשם יהיה בלעדי לחלוטין.</p>
</div>{foot(pg)}</section>"""

def index_page(pg):
    rows = ""
    for f in range(1, 6):
        fam = FAMILIES[f]
        cs = [c for c in C if c["fam"] == f]
        cells = "".join(
            f'<div class="ix"><div class="ixs dark">{svg(c["n"], "15mm")}</div>'
            f'<div class="ixt"><span class="ltr ixn">{c["n"]:02d}</span> {c["he"]}{" ★" if c["n"] in TOP5 else ""}</div></div>' for c in cs)
        rows += (f'<div class="ixr"><div class="ixf"><div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:13pt;color:var(--gold);text-align:right">{fam[0]}</div>'
                 f'<div style="font-weight:700;font-size:10pt">{fam[1]}</div><div style="font-size:7.6pt;color:var(--muted);line-height:1.35">{fam[2]}</div></div>{cells}</div>')
    return f"""
<section class="page paper">{run("מפת הכיוונים")}
<style>.ixr{{display:grid;grid-template-columns:34mm repeat(6,1fr);gap:3mm;align-items:center;margin-top:2.6mm}}
.ix{{display:flex;flex-direction:column;align-items:stretch}} .ixs{{height:23mm;display:flex;align-items:center;justify-content:center}}
.ixt{{font-size:7.6pt;margin-top:1mm;white-space:nowrap;overflow:hidden}} .ixn{{font-family:Montserrat;font-weight:600;color:var(--gold)}}</style>
<div style="position:absolute;top:16mm;left:14mm;right:14mm;bottom:12mm">
  <div style="display:flex;justify-content:space-between;align-items:baseline">
   <h2 style="font-size:19pt">30 כיוונים בחמש משפחות</h2><span style="font-size:8.4pt;color:var(--muted)">★ = חמשת הכיוונים המומלצים</span></div>
  {rows}
</div>{foot(pg)}</section>"""

def divider(f, pg):
    fam = FAMILIES[f]
    cs = [c for c in C if c["fam"] == f]
    marks = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:3mm">{svg(c["n"], "22mm")}<span class="ltr" style="font-family:Montserrat;font-size:7pt;letter-spacing:.2em;color:#8C857A">{c["n"]:02d}</span></div>' for c in cs)
    intro = {
        1: "צורות מלאות וכבדות שמבטאות מסה, יציבות והון. זו השפה של מוסדות פיננסיים ותאגידי ענק: מעט פרטים והרבה נוכחות.",
        2: "הסדר האדריכלי היווני (כותרות, עמודים, מדרגות ומגנים) בפרשנות מודרנית ועבה. השפה שבה אמינות נבנתה במשך 2,500 שנה.",
        3: "סמלים שאתונה עצמה השתמשה בהם: המאנדר, הינשוף, מטבע הכסף, הדפנה, הזית והאומפלוס. שורשים שאי אפשר להעתיק.",
        4: "המיקום הוא המוצר: המשולש ההיסטורי, הגג, החזית, החצר והנוף לאקרופוליס, מתורגמים לצורה.",
        5: "ערך שעולה, השם ומשמעותו ביוונית (άλμα, זינוק) והאות M שבלב השם, כחלופה מכובדת למונוגרם AG.",
    }[f]
    return f"""
<section class="page dark">
 <div style="position:absolute;top:0;bottom:0;right:0;width:118mm;padding:24mm 16mm;border-left:1px solid #2E2B27;display:flex;flex-direction:column;justify-content:center">
  <div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:54pt;color:#B9A06F;text-align:right;line-height:1">{fam[0]}</div>
  <div class="ltr" style="font-family:Montserrat;font-weight:600;font-size:8pt;letter-spacing:.34em;color:#8C857A;text-align:right;margin-top:4mm">{fam[3].upper()}</div>
  <h1 style="font-size:28pt;margin-top:4mm;color:#F3EFE7">{fam[1]}</h1>
  <p style="margin-top:4mm;color:#BDB6A8;font-size:10.5pt">{intro}</p>
  <div style="margin-top:6mm;font-size:8.6pt;color:#8C857A">כיוונים {cs[0]["n"]:02d}–{cs[-1]["n"]:02d}</div>
 </div>
 <div style="position:absolute;top:0;bottom:0;left:0;width:179mm;display:grid;grid-template-columns:repeat(3,1fr);align-content:center;row-gap:14mm;padding:20mm 14mm">{marks}</div>
</section>"""

def ranking(pg):
    srt = sorted(C, key=lambda c: (-sum(c["scores"]), c["n"]))
    rows = "".join(
        f'<tr{" class=top" if c["n"] in TOP5 else ""}><td class="ltr n">{c["n"]:02d}</td><td class="s">{svg(c["n"], "7mm")}</td><td>{c["he"]}</td>'
        + "".join(f'<td class="ltr v">{v}</td>' for v in c["scores"]) + f'<td class="ltr t">{sum(c["scores"])}</td></tr>'
        for c in srt)
    half = len(srt) // 2
    def table(rs):
        return (f'<table><thead><tr><th>#</th><th></th><th>כיוון</th>' + "".join(f"<th>{k}</th>" for k in CRIT) + '<th>סה"כ</th></tr></thead><tbody>' + rs + "</tbody></table>")
    rl = rows.split("</tr>")[:-1]
    t1 = table("</tr>".join(rl[:half]) + "</tr>"); t2 = table("</tr>".join(rl[half:]) + "</tr>")
    return f"""
<section class="page paper">{run("טבלת הערכה מסכמת")}
<style>table{{width:100%;border-collapse:collapse;font-size:7.6pt}} th{{font-weight:500;color:var(--muted);font-size:6.6pt;text-align:center;padding:1mm .5mm;border-bottom:1px solid var(--ink)}}
td{{padding:.55mm .8mm;border-bottom:1px solid var(--line);text-align:center;white-space:nowrap}} td:nth-child(3){{text-align:right}}
td.n{{font-family:Montserrat;font-weight:600;color:var(--gold)}} td.v{{font-family:Montserrat}} td.t{{font-family:Montserrat;font-weight:700}}
td.s{{--bg:#F4F1EB;--fg:#171614;--ac:#9C8150;padding:.3mm}} tr.top td{{background:#E6DECF}} tr.top td.t{{color:var(--gold)}}</style>
<div style="position:absolute;top:16mm;left:14mm;right:14mm;bottom:13mm">
 <h2 style="font-size:19pt">כל 30 הכיוונים, מדורגים</h2>
 <p style="font-size:8.6pt;color:var(--muted);margin-top:1mm">ציון הצוות בחמשת המבחנים. השורות המודגשות הן חמשת הכיוונים המומלצים.</p>
 <div style="display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:3mm">{t1}{t2}</div>
</div>{foot(pg)}</section>"""

def recommendation(pg):
    top = [next(c for c in C if c["n"] == n) for n in TOP5]
    why = {
        7: "השילוב הנדיר בין צורה מונומנטלית למשחק המילים Capital (כותרת עמוד והון). הוא מספר את סיפור ההון העצמי בלי מילה אחת.",
        1: "הצורה הכי חזקה ופשוטה בחוברת. היא מזוהה מ-100 מטר ובגודל 16 פיקסלים, והיא מודרנית ומוסדית בו-זמנית.",
        10: "הבסיס של הפרתנון: שלושה שותפים, שלושה שלבים וגג מוזהב. סיפור שמשקיעים זוכרים ומספרים הלאה.",
        11: "שלושת המייסדים כשלושה עמודים בתוך מגן. מבטא 'Old Money', ביסוס והגנה על ההון. מושלם ל-Golden Visa.",
        13: "הסימן היווני הוותיק ביותר, בביצוע עבה וסגור. נצחי, לא ניתן להעתקה, ונראה מצוין בפליז ובאבן.",
    }
    first = top[0]
    cards = "".join(
        f'<div style="display:grid;grid-template-rows:30mm auto;gap:2mm"><div class="dark" style="display:flex;align-items:center;justify-content:center;position:relative">'
        f'<span class="ltr" style="position:absolute;top:2mm;right:3mm;font-family:Montserrat;font-weight:600;font-size:6.5pt;letter-spacing:.2em;color:#B9A06F">#{i+2}</span>{svg(c["n"], "19mm")}</div>'
        f'<div><div style="font-weight:700;font-size:9.6pt"><span class="ltr" style="font-family:Montserrat;color:var(--gold)">{c["n"]:02d}</span> {c["he"]}</div>'
        f'<div style="font-size:8pt;line-height:1.45;color:#3A3631;margin-top:.6mm">{bd(why[c["n"]])}</div></div></div>'
        for i, c in enumerate(top[1:]))
    return f"""
<section class="page paper">{run("ההמלצה")}
<div style="position:absolute;top:17mm;left:14mm;right:14mm;bottom:13mm;display:grid;grid-template-columns:1fr 1.15fr;gap:9mm">
 <div class="dark" style="display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative">
   <div class="top-badge" style="left:auto;right:4mm">#1 · RECOMMENDED</div>
   {lockup(first, 1.05, tag=True)}
 </div>
 <div style="display:flex;flex-direction:column">
   <span class="heb-eyebrow">ההמלצה של הצוות</span>
   <h2 style="font-size:22pt;margin-top:1mm;line-height:1.15">כיוון 07: הכותרת (The Capital)</h2>
   <p style="margin-top:2.4mm;font-size:10pt;line-height:1.65">{bd(why[7])} זהו הכיוון היחיד שקיבל ציון גבוה בכל חמשת המבחנים. הוא נראה יווני בלי להיות תיירותי, ומוסדי בלי להיות קר. הלוח המוזהב העליון מתחבר ישירות לרעיון הגג, לב המוצר של החברה.</p>
   <p style="margin-top:2.4mm;font-size:10pt;line-height:1.65"><b>איך זה ייראה בפועל:</b> הכותרת המוזהבת מוטבעת בפליז ליד כניסת כל בניין, נחרטת באבן בלובי, ומופיעה כסמל לבד בפינת כל מסמך, מצגת ושלט אתר. בגודל של פאביקון היא נשארת עמוד יווני ברור, ובשלט של 6 מטר היא נראית כמו מונומנט.</p>
   <p style="margin-top:2.4mm;font-size:10pt;line-height:1.65"><b>החלופות המובילות</b> מכסות טווח של אפשרויות: מהמודרני והמופשט ביותר (01) ועד הקלאסי והמסורתי ביותר (11).</p>
   <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:auto">{cards}</div>
 </div>
</div>{foot(pg)}</section>"""

def next_steps(pg):
    steps = [("בחירה", "בחירת 2–3 כיוונים מתוך ה-30 (מומלץ: מתוך חמשת המובילים) לפיתוח מעמיק."),
             ("פיתוח", "ליטוש גאומטרי מלא, לוגוטייפ מצויר בהתאמה אישית, וגרסאות אופקית, אנכית וסמל בלבד."),
             ("מבחן שטח", "הדמיות על שלט אתר, חזית בניין, מצגת משקיעים, אתר, כרטיס ביקור ואינסטגרם."),
             ("ספר מותג", "מדריך שימוש: מרווחי ביטחון, צבעים, גופנים, שימושים אסורים, ותבניות מסמכים."),
             ("השקה", "הטמעה באתר, ברשתות, בשילוט הפרויקטים ובכל מסמכי השיווק, והחלפה הדרגתית של הישן.")]
    notes = [
        "נתוני החברה אינם אחידים בין המסמכים. בחוברת גאזי בולבארד: <b>13,000+ מ\"ר, 200+ דירות ו-€70M+ מכירות</b>. במדריך המשקיעים: <b>11,800+ מ\"ר, 168 דירות ו-€58.4M+</b>. גם מספר הפרויקטים משתנה בין 8, 10 ו-16, ובמקום אחר 'מעל 23'. מומלץ לקבוע סט מספרים רשמי אחד לזהות החדשה.",
        "במסמך ה-Design Concept מופיע המשפט <b>\"in the vibrant heart of Berlin\"</b>. ככל הנראה שארית מתבנית, ומומלץ לתקן לפני ההפצה הבאה.",
        "שגיאות כתיב קטנות: <b>DEVELOPEMENT</b> בחוברת Utopia, <b>APARTAMENTS</b> באתר, <b>PROFESIONAL</b> בחוברת החברה.",
        "מוני הנתונים באתר (\"+0\") נטענים באנימציה. אם מנועי חיפוש או לקוחות עם חיבור איטי רואים אפס, זו פגיעה באמינות. כדאי להציג את המספר האמיתי כברירת מחדל.",
    ]
    return f"""
<section class="page paper">{run("השלבים הבאים")}
<div style="position:absolute;top:18mm;left:14mm;right:14mm;bottom:14mm;display:grid;grid-template-columns:1fr 1fr;gap:12mm">
 <div>
  <span class="heb-eyebrow">מכאן ממשיכים</span>
  <h2 style="font-size:22pt;margin-top:1.5mm">מ-30 כיוונים ללוגו אחד</h2>
  <div style="margin-top:4mm;display:grid;gap:3mm">
   {"".join(f'<div style="display:grid;grid-template-columns:10mm 1fr;gap:3mm;border-top:1px solid var(--line);padding-top:2.4mm"><div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:15pt;color:var(--gold)">0{i}</div><div><div style="font-weight:700;font-size:10.5pt">{a}</div><div style="font-size:8.8pt;color:#4A463F;line-height:1.5">{b}</div></div></div>' for i,(a,b) in enumerate(steps,1))}
  </div>
 </div>
 <div>
  <span class="heb-eyebrow">הערות אגב מהסקירה (מעבר ללוגו)</span>
  <h2 style="font-size:16pt;margin-top:1.5mm">דברים שעלו בקריאת החומרים</h2>
  <div style="margin-top:4mm;display:grid;gap:3mm">
   {"".join(f'<div style="background:var(--stone);padding:3mm 3.5mm;font-size:8.7pt;line-height:1.55;border-right:2.5px solid var(--gold)">{bd(t)}</div>' for t in notes)}
  </div>
  <div class="dark" style="margin-top:6mm;padding:5mm;text-align:center">
   <div class="ltr" style="font-family:Cinzel;font-weight:700;font-size:14pt;letter-spacing:.3em;margin-right:-.3em">ALMA GROUP</div>
   <div class="ltr" style="font-family:Montserrat;font-size:6.5pt;letter-spacing:.42em;color:#B9A06F;margin-top:2mm;margin-right:-.42em">THE STANDARD YOU DESERVE</div>
  </div>
 </div>
</div>{foot(pg)}</section>"""

def build():
    pages = [cover()]
    pg = 2
    for fn in (research, strategy, palette, index_page):
        pages.append(fn(pg)); pg += 1
    for f in range(1, 6):
        pages.append(divider(f, pg)); pg += 1
        for c in [c for c in C if c["fam"] == f]:
            pages.append(concept_page(c, pg)); pg += 1
    pages.append(ranking(pg)); pg += 1
    pages.append(recommendation(pg)); pg += 1
    pages.append(next_steps(pg)); pg += 1
    links = "".join(f'<link rel="stylesheet" href="{NM}{f}">' for f in FONT_CSS)
    html = f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>Alma Group Logo Exploration</title>{links}<style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
    open("doc.html", "w", encoding="utf-8").write(html)
    print("pages", len(pages))

if __name__ == "__main__":
    build()
