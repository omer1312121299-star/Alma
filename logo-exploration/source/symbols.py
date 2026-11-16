"""30 logo symbols for Alma Group, each drawn on a 200x200 grid.
Classes: f = foreground fill, a = accent fill, b = background fill,
sf / sa / sb = stroke versions (fill none)."""
import math

_uid = [0]
def uid(p):
    _uid[0] += 1
    return f"{p}{_uid[0]}"

def R(x, y, w, h, c="f"):
    return f'<rect class="{c}" x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"/>'

def P(pts, c="f"):
    return f'<polygon class="{c}" points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}"/>'

def C(cx, cy, r, c="f"):
    return f'<circle class="{c}" cx="{cx}" cy="{cy}" r="{r}"/>'

def fluted(x, y, w, h, n, gap, c="f"):
    fw = (w - gap * (n - 1)) / n
    return "".join(R(x + i * (fw + gap), y, fw, h, c) for i in range(n))

# ---------------- Family I : Monumental ----------------
def monolith():
    return R(62, 18, 76, 22) + R(62, 47, 76, 8, "a") + R(62, 62, 76, 120)

def keystone():
    return P([(56, 30), (144, 30), (121, 172), (79, 172)]) + R(96, 30, 8, 74, "a")

def cornerstone():
    return P([(36, 36), (80, 36), (80, 120), (164, 120), (164, 164), (36, 164)]) + R(90, 58, 52, 52, "a")

def block():
    s = P([(100, 26), (164, 63), (100, 100), (36, 63)], "a")
    s += P([(36, 63), (100, 100), (100, 174), (36, 137)])
    s += P([(100, 100), (164, 63), (164, 137), (100, 174)])
    for k in (25, 49):
        s += f'<line class="sb" stroke-width="5" x1="36" y1="{63+k}" x2="100" y2="{100+k}"/>'
        s += f'<line class="sb" stroke-width="5" x1="100" y1="{100+k}" x2="164" y2="{63+k}"/>'
    return s

def vault():
    return (f'<path class="f" fill-rule="evenodd" d="M36,36H164V164H36Z M100,68 a32,32 0 1,0 0.01,0Z"/>'
            + C(100, 100, 12, "a"))

def portal():
    return R(26, 34, 148, 26) + R(42, 68, 36, 112) + R(122, 68, 36, 112) + R(84, 168, 32, 12, "a")

# ---------------- Family II : Classical order ----------------
def capital():
    return (R(24, 36, 152, 22, "a") + P([(34, 62), (166, 62), (139, 94), (61, 94)])
            + R(64, 99, 72, 5) + fluted(64, 109, 72, 73, 5, 3.5))

def ionic():
    s = f'<circle class="sf" stroke-width="13" cx="48" cy="92" r="22"/>'
    s += f'<circle class="sf" stroke-width="13" cx="152" cy="92" r="22"/>'
    s += R(48, 63.5, 104, 13) + C(48, 92, 7, "a") + C(152, 92, 7, "a")
    s += R(80, 92, 40, 12, "a")
    s += fluted(72, 116, 56, 66, 4, 4)
    return s

def temple():
    return (P([(22, 76), (100, 32), (178, 76)], "a") + R(22, 82, 156, 11)
            + fluted(32, 99, 136, 62, 5, 10) + R(16, 166, 168, 12))

def krepidoma():
    return R(10, 140, 180, 32) + R(36, 102, 128, 32) + R(62, 64, 76, 32, "a")

def three_pillars():
    sid = uid("sh")
    d = "M38,24 H162 V100 C162,140 134,166 100,180 C66,166 38,140 38,100 Z"
    s = f'<path class="f" d="{d}"/>'
    s += R(54, 42, 92, 11, "a")
    s += R(62, 62, 18, 70, "b") + R(91, 62, 18, 70, "b") + R(120, 62, 18, 70, "b")
    s += R(56, 138, 88, 6, "b")
    return s

def aspis():
    s = f'<circle class="sf" stroke-width="10" cx="100" cy="100" r="77"/>'
    s += C(100, 100, 60)
    s += R(80, 58, 40, 9, "a") + P([(84, 67), (116, 67), (110, 76), (90, 76)], "a")
    s += fluted(89, 79, 22, 52, 3, 2, "a") + R(80, 134, 40, 8, "a")
    return s

# ---------------- Family III : Athenian emblems ----------------
def meander():
    pts = [(38, 162), (38, 38), (162, 38), (162, 162), (68, 162), (68, 68), (132, 68), (132, 132), (100, 132), (100, 104)]
    s = (f'<polyline class="sf" stroke-width="16" stroke-linecap="butt" stroke-linejoin="miter" '
         f'points="{" ".join(f"{x},{y}" for x, y in pts)}"/>')
    s += R(92, 88, 16, 16, "a")
    return s

def owl():
    d = "M48,32 L82,56 L118,56 L152,32 L152,118 A52,52 0 0 1 48,118 Z"
    s = f'<path class="f" d="{d}"/>'
    s += C(76, 92, 22, "b") + C(124, 92, 22, "b") + C(76, 92, 9, "a") + C(124, 92, 9, "a")
    s += P([(91, 114), (109, 114), (100, 131)], "a")
    return s

def tetradrachm():
    pid = uid("cp")
    s = f'<circle class="sf" stroke-width="5" cx="100" cy="100" r="92"/>'
    s += f'<circle class="sf" stroke-width="1.6" cx="100" cy="100" r="64"/>'
    s += (f'<defs><path id="{pid}" d="M100,100 m-77,0 a77,77 0 1,1 154,0 a77,77 0 1,1 -154,0"/></defs>'
          f'<text class="f" style="font-family:Cinzel;font-weight:700;font-size:15.5px;letter-spacing:4.2px">'
          f'<textPath href="#{pid}" startOffset="0">ALMA GROUP · ATHENS · GREECE · ALMA GROUP · ATHENS ·</textPath></text>')
    s += R(74, 54, 52, 9, "a") + P([(78, 63), (122, 63), (114, 73), (86, 73)], "a")
    s += fluted(84, 77, 32, 56, 4, 2.5) + R(74, 136, 52, 9)
    return s

def laurel():
    s = ""
    stem = ""
    for i in range(9):
        ang = math.radians(112 + i * 17)
        x = 100 + 62 * math.cos(ang); y = 106 + 62 * math.sin(ang)
        t = ang + math.pi / 2          # tangent pointing up along the branch (left side)
        for dv in (-0.62, 0.62):
            d = t + dv
            cx = x + 11 * math.cos(d); cy = y + 11 * math.sin(d)
            rot = math.degrees(d)
            for mx, rr in ((cx, rot), (200 - cx, 180 - rot)):
                s += f'<ellipse class="f" cx="{mx:.1f}" cy="{cy:.1f}" rx="12" ry="4.6" transform="rotate({rr:.1f} {mx:.1f} {cy:.1f})"/>'
    s += '<path class="sf" stroke-width="3.2" fill="none" d="M88,168 A62,62 0 0 1 48,72"/>'
    s += '<path class="sf" stroke-width="3.2" fill="none" d="M112,168 A62,62 0 0 0 152,72"/>'
    s += R(86, 74, 28, 7, "a") + fluted(90, 84, 20, 38, 3, 2.5, "a") + R(84, 125, 32, 7, "a")
    return s

def olive():
    s = '<path class="sf" stroke-width="7" stroke-linecap="round" d="M100,182 C100,140 100,90 100,26"/>'
    leaves = [(56, 150, 34), (74, 108, 30), (90, 70, 26)]
    for d, y, L in leaves:
        for side in (-1, 1):
            cx = 100 + side * (L * 0.62)
            rot = -side * 38
            s += f'<ellipse class="f" cx="{cx:.1f}" cy="{y-10}" rx="{L*0.72:.1f}" ry="{L*0.26:.1f}" transform="rotate({rot} {cx:.1f} {y-10})"/>'
    s += '<ellipse class="a" cx="100" cy="26" rx="11" ry="15"/>'
    return s

def omphalos():
    cid = uid("om")
    dome = "M48,150 C48,86 70,40 100,40 C130,40 152,86 152,150 Z"
    s = f'<defs><clipPath id="{cid}"><path d="{dome}"/></clipPath></defs><path class="f" d="{dome}"/>'
    lines = ""
    for k in range(-6, 7):
        lines += f'<line x1="{100+k*22-80}" y1="180" x2="{100+k*22+80}" y2="20"/>'
        lines += f'<line x1="{100+k*22+80}" y1="180" x2="{100+k*22-80}" y2="20"/>'
    s += f'<g class="sb" stroke-width="3.2" clip-path="url(#{cid})">{lines}</g>'
    s += R(36, 156, 128, 16, "a")
    return s

# ---------------- Family IV : Place & view ----------------
def window():
    s = '<path class="f" fill-rule="evenodd" d="M26,26H174V174H26Z M44,44V156H156V44Z"/>'
    s += P([(50, 156), (64, 136), (136, 134), (150, 156)], "a")
    s += P([(72, 110), (100, 94), (128, 110)], "a") + R(72, 112, 56, 3.5, "a")
    s += fluted(76, 118, 48, 13, 4, 8, "a") + R(70, 131, 60, 3.5, "a")
    return s

def attic_sunset():
    s = C(100, 88, 58, "a")
    s += P([(14, 176), (44, 132), (156, 130), (186, 176)])
    s += P([(66, 106), (100, 88), (134, 106)]) + R(66, 108, 68, 4)
    s += fluted(70, 115, 60, 14, 6, 4.8) + R(62, 128, 76, 6)
    return s

def triangle():
    A, B, Cc = (30, 46), (170, 46), (100, 167)
    s = ""
    for (x1, y1), (x2, y2) in ((A, B), (B, Cc), (Cc, A)):
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; t = 10
        s += (f'<line class="sf" stroke-width="16" stroke-linecap="butt" x1="{x1+ux*t:.1f}" y1="{y1+uy*t:.1f}" '
              f'x2="{x2-ux*t:.1f}" y2="{y2-uy*t:.1f}"/>')
    s += C(100, 86, 13, "a")
    return s

def rooftops():
    s = ""
    for x, top in ((36, 74), (82, 30), (128, 56)):
        s += R(x, top, 36, 8, "a") + R(x, top + 13, 36, 176 - top - 13)
    return s

def facade():
    s = ""
    for i in range(8):
        y = 24 + i * 19
        w = 78 if i % 2 == 0 else 100
        s += R(100 - w / 2, y, w, 12, "a" if i == 0 else "f")
    s += R(64, 178, 72, 0.01)
    return s

def courtyard():
    s = '<rect class="sf" stroke-width="15" x="31.5" y="31.5" width="137" height="137"/>'
    s += '<rect class="sf" stroke-width="9" x="64.5" y="64.5" width="71" height="71"/>'
    s += R(88, 88, 24, 24, "a")
    return s

# ---------------- Family V : Growth, motion, name ----------------
def four_pillars():
    s = ""
    hs = [62, 88, 114, 140]
    for i, h in enumerate(hs):
        x = 36 + i * 36; c = "a" if i == 3 else "f"
        s += R(x - 4, 172 - h, 32, 7, c) + R(x, 172 - h + 10, 24, h - 10, c)
    s += R(26, 176, 148, 6)
    return s

def leap():
    s = R(26, 124, 52, 54) + R(122, 80, 52, 98)
    s += '<path class="sa" stroke-width="11" stroke-linecap="butt" d="M52,112 C58,36 118,24 142,60"/>'
    # arrow head aligned with the curve's end tangent (118,24)->(142,60)
    dx, dy = 24, 36; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; px, py = -uy, ux
    tip = (142 + ux * 20, 60 + uy * 20)
    b1 = (142 + px * 14, 60 + py * 14); b2 = (142 - px * 14, 60 - py * 14)
    s += P([tip, b1, b2], "a")
    return s

def spiral():
    s = ""; n = 12
    for i in range(n):
        a0 = math.radians(-90 + i * 30 + 2); a1 = math.radians(-90 + (i + 1) * 30 - 2)
        r0, r1 = 26, 78
        pts = [(100 + r0 * math.cos(a0), 100 + r0 * math.sin(a0)), (100 + r1 * math.cos(a0), 100 + r1 * math.sin(a0)),
               (100 + r1 * math.cos(a1), 100 + r1 * math.sin(a1)), (100 + r0 * math.cos(a1), 100 + r0 * math.sin(a1))]
        d = (f'M{pts[0][0]:.2f},{pts[0][1]:.2f} L{pts[1][0]:.2f},{pts[1][1]:.2f} '
             f'A{r1},{r1} 0 0 1 {pts[2][0]:.2f},{pts[2][1]:.2f} L{pts[3][0]:.2f},{pts[3][1]:.2f} '
             f'A{r0},{r0} 0 0 0 {pts[0][0]:.2f},{pts[0][1]:.2f} Z')
        if i == n - 1:
            s += f'<path class="a" d="{d}"/>'
        else:
            s += f'<path class="f" opacity="{0.18 + 0.82 * i / (n - 2):.2f}" d="{d}"/>'
    return s

def grid():
    s = ""
    for r in range(3):
        for c in range(3):
            s += R(25 + c * 52, 25 + r * 52, 46, 46, "a" if (r == 0 and c == 2) else "f")
    return s

def m_colonnade():
    s = R(28, 36, 40, 10) + R(132, 36, 40, 10)
    s += R(34, 50, 28, 116) + R(138, 50, 28, 116)
    s += P([(62, 50), (84, 50), (100, 100), (116, 50), (138, 50), (108, 132), (92, 132)])
    s += R(24, 170, 152, 11, "a")
    return s

def architrave():
    return (R(30, 46, 140, 9, "a") + R(30, 60, 140, 3, "f")
            + '<text class="f" x="100" y="146" text-anchor="middle" style="font-family:Cinzel;font-weight:700;font-size:104px">M</text>'
            + R(30, 154, 140, 3, "f") + R(30, 161, 140, 9, "a"))

SYMBOLS = {
    1: monolith, 2: keystone, 3: cornerstone, 4: block, 5: vault, 6: portal,
    7: capital, 8: ionic, 9: temple, 10: krepidoma, 11: three_pillars, 12: aspis,
    13: meander, 14: owl, 15: tetradrachm, 16: laurel, 17: olive, 18: omphalos,
    19: window, 20: attic_sunset, 21: triangle, 22: rooftops, 23: facade, 24: courtyard,
    25: four_pillars, 26: leap, 27: spiral, 28: grid, 29: m_colonnade, 30: architrave,
}

def svg(n, size=None, cls=""):
    body = SYMBOLS[n]()
    st = f' style="width:{size};height:{size}"' if size else ""
    return f'<svg class="sym {cls}" viewBox="0 0 200 200"{st} xmlns="http://www.w3.org/2000/svg">{body}</svg>'
