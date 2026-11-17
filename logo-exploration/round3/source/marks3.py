"""Round 3: 30 simple luxury marks on a 200x200 grid.
Classes: ln = fg stroke, lg = gold stroke, ff = fg fill, fg_ = gold fill, bk = bg fill."""
import math

SW = 4.6
_uid = [0]
def uid(p):
    _uid[0] += 1; return f"{p}{_uid[0]}"

def L(d, c="ln", w=SW, extra=""):
    return f'<path class="{c}" d="{d}" stroke-width="{w}" fill="none" stroke-linecap="butt" stroke-linejoin="miter"{extra}/>'
def F(d, c="fa"):
    return f'<path class="{c}" d="{d}"/>'
def Ci(cx, cy, r, c="ln", w=SW):
    if c in ("ln", "lg"): return f'<circle class="{c}" cx="{cx}" cy="{cy}" r="{r}" stroke-width="{w}" fill="none"/>'
    return f'<circle class="{c}" cx="{cx}" cy="{cy}" r="{r}"/>'

STAR = "M100,22 Q106,94 178,100 Q106,106 100,178 Q94,106 22,100 Q94,94 100,22 Z"
def star(cx, cy, s):
    return f'<path class="fa" transform="translate({cx} {cy}) scale({s}) translate(-100 -100)" d="{STAR}"/>'

# I. Single line
def arch():      return L("M64,166 V92 A36,36 0 0 1 136,92 V166") + L("M48,166 H152", "lg")
def keyhole():   return L("M89.4,104.8 A27,27 0 1 1 110.6,104.8 L121,164 H79 Z", "lg")
def horizon():   return Ci(100, 96, 54) + L("M22,118 H178", "lg")
def tower():     return L("M82,40 H118 V170 H82 Z") + F("M82,26 H118 V36 H82 Z")
def step():      return L("M36,158 H78 V118 H118 V78 H160") + Ci(160, 54, 8, "fa")
def fold():      return L("M44,40 H124 L160,76 V160 H44 Z") + F("M124,40 V76 H160 Z")
# II. One shape
def pearl():     return Ci(100, 100, 34, "fa") + Ci(100, 100, 58, "ln", 2.6)
def eclipse():
    m = uid("ec")
    return (f'<defs><mask id="{m}"><rect x="0" y="0" width="200" height="200" fill="#fff"/><circle cx="122" cy="88" r="50" fill="#000"/></mask></defs>'
            f'<circle class="fa" cx="96" cy="104" r="62" mask="url(#{m})"/>')
def stone():     return F("M80,44 H120 A36,36 0 0 1 156,80 V120 A36,36 0 0 1 120,156 H80 A36,36 0 0 1 44,120 V80 A36,36 0 0 1 80,44 Z") + L("M82,56 H118 A26,26 0 0 1 144,82 V118 A26,26 0 0 1 118,144 H82 A26,26 0 0 1 56,118 V82 A26,26 0 0 1 82,56 Z", "lb", 2)
def diamond():   return L("M100,28 L164,100 L100,172 L36,100 Z", "ln", 3.4) + F("M100,74 L124,100 L100,126 L76,100 Z")
def half():      return F("M100,42 A58,58 0 0 0 100,158 Z") + Ci(100, 100, 58)
def niche():     return F("M68,164 V98 A32,32 0 0 1 132,98 V164 Z") + L("M50,176 H150", "ln", 3)
# III. Quiet architecture
def window():    return L("M46,46 H154 V154 H46 Z M100,46 V154 M46,100 H154") + F("M104.6,50.6 H149.4 V95.4 H104.6 Z")
def court():     return L("M46,46 H154 V154 H46 Z") + Ci(100, 100, 42, "lg")
def corners():   return L("M40,84 V40 H84") + L("M160,116 V160 H116") + Ci(100, 100, 9, "fa")
def meridian():  return Ci(100, 100, 56) + L("M100,24 V176", "lg")
def levels():    return L("M62,78 H138", "lg") + L("M46,102 H154") + L("M30,126 H170")
def door():      return L("M70,32 H130 V168 H70 Z") + Ci(117, 104, 5.5, "fa")
# IV. Emblems
def sparkle():   return star(100, 100, 1)
def ring():      return Ci(100, 112, 50) + F("M100,40 L113,56 L100,72 L87,56 Z")
def seal():
    p = uid("sp")
    return (Ci(100, 100, 88, "ln", 1.8) + Ci(100, 100, 68, "ln", 1.0) +
            f'<defs><path id="{p}" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>'
            f'<text class="tf" style="font-family:\'Cormorant Garamond\';font-weight:600;font-size:13.6px;letter-spacing:3.5px"><textPath href="#{p}">ALMA GROUP · THE STANDARD YOU DESERVE ·</textPath></text>'
            + star(100, 100, 0.38))
def key():       return Ci(58, 100, 22) + L("M80,100 H170 M150,100 V120 M166,100 V114") + Ci(58, 100, 6, "fa")
def orbit():     return Ci(100, 100, 60, "ln", 3) + Ci(142.4, 57.6, 10, "fa")
def infinity():
    pts = []
    for i in range(201):
        t = 2 * math.pi * i / 200
        d = 1 + math.sin(t) ** 2
        pts.append((100 + 74 * math.cos(t) / d, 100 + 74 * math.sin(t) * math.cos(t) / d))
    return L("M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z", "lg", 5)
# V. Wordmarks (symbol = the wordmark itself)
def T(txt, x, y, size, fam, wt=400, ls=0, c="tf", style="", anchor="middle"):
    return f'<text class="{c}" x="{x}" y="{y}" text-anchor="{anchor}" style="font-family:\'{fam}\';font-weight:{wt};font-size:{size}px;letter-spacing:{ls}px;{style}">{txt}</text>'
def wm_italiana(): return T('ALMA<tspan class="fa" dx="-4">.</tspan>', 106, 112, 50, "Italiana", 400, 12) + T("GROUP", 104.7, 140, 11, "Montserrat", 500, 9.5)
def wm_script():   return T("Alma", 100, 118, 92, "Cormorant Garamond", 400, 0, style="font-style:italic") + L("M58,140 H142", "lg", 2.2)
def wm_bodoni():   return L("M30,66 H170", "lg", 2.4) + T("ALMA", 106, 124, 50, "Bodoni Moda", 400, 11) + L("M30,140 H170", "lg", 2.4)
def wm_josefin():  return T("ALMA", 106.5, 104, 44, "Josefin Sans", 300, 13) + L("M90,120 H110", "lg", 2.6) + T("GROUP", 104.5, 146, 11, "Josefin Sans", 300, 9)
def wm_plaque():   return L("M30,64 H170 V136 H30 Z", "lg", 2.2) + T("ALMA", 104, 108, 33, "Gilda Display", 400, 8) + T("GROUP", 103, 124, 7.5, "Montserrat", 500, 6)
def wm_lower():    return T('alma<tspan class="fa">.</tspan>', 100, 116, 62, "Jost", 400, 1)

MARKS = {1: arch, 2: keyhole, 3: horizon, 4: tower, 5: step, 6: fold,
         7: pearl, 8: eclipse, 9: stone, 10: diamond, 11: half, 12: niche,
         13: window, 14: court, 15: corners, 16: meridian, 17: levels, 18: door,
         19: sparkle, 20: ring, 21: seal, 22: key, 23: orbit, 24: infinity,
         25: wm_italiana, 26: wm_script, 27: wm_bodoni, 28: wm_josefin, 29: wm_plaque, 30: wm_lower}
WORDMARK = set(range(25, 31))

def svg(n, size=None, cls=""):
    st = f' style="width:{size};height:{size}"' if size else ""
    return f'<svg class="mk {cls}" viewBox="0 0 200 200"{st} xmlns="http://www.w3.org/2000/svg">{MARKS[n]()}</svg>'

CSS = """
.mk .ln{stroke:var(--fg)} .mk .lg{stroke:var(--ac)} .mk .lb{stroke:var(--bg)}
.mk .fa{fill:var(--ac)} .mk .ff{fill:var(--fg)} .mk .tf{fill:var(--fg)}
.th-dark{--bg:#0d0c0b;--fg:#efe7d6;--ac:#c7a466}
.th-light{--bg:#f4efe7;--fg:#151311;--ac:#a7844b}
.th-mono{--bg:#151311;--fg:#efe7d6;--ac:#efe7d6}
.th-monol{--bg:#ffffff;--fg:#151311;--ac:#151311}
"""
