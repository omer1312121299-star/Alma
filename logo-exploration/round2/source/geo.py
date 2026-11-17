"""Geometry engine for round-2 'wow' marks. Every symbol is drawn on a 200x200 grid.
Tones: classes g0 (darkest) .. g15 (lightest) for fills, s0..s15 for strokes, 'bk' = background fill,
'sbk' = background stroke. A symbol declares a mono mode: 'sep' (all tones -> fg, faces separated
by background hairlines) or 'thr' (threshold: dark tones -> bg, light -> fg)."""
import math

_uid = [0]
def uid(p="u"):
    _uid[0] += 1
    return f"{p}{_uid[0]}"

def f2(v): return f"{v:.2f}"

def poly(pts, k, extra=""):
    return f'<polygon class="g{k}"{extra} points="{" ".join(f"{f2(x)},{f2(y)}" for x, y in pts)}"/>'

def path_d(pts, closed=True):
    d = "M" + " L".join(f"{f2(x)},{f2(y)}" for x, y in pts)
    return d + (" Z" if closed else "")

def clamp(v, a, b): return max(a, min(b, v))
def tone(v):  # v in 0..1 -> 0..15
    return int(round(clamp(v, 0, 1) * 15))

# ---------- convex clipping ----------
def clip(polyg, a, b, c):
    """keep points with a*x+b*y+c >= 0"""
    out = []
    n = len(polyg)
    for i in range(n):
        P, Q = polyg[i], polyg[(i + 1) % n]
        fp, fq = a * P[0] + b * P[1] + c, a * Q[0] + b * Q[1] + c
        if fp >= 0: out.append(P)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return out

BIG = [(-1000, -1000), (1200, -1000), (1200, 1200), (-1000, 1200)]

# ---------- fitting ----------
def fit(groups, pad=12, cx=100, cy=100):
    """groups: list of point lists. returns transform function mapping into the 200 box."""
    xs = [p[0] for g in groups for p in g]; ys = [p[1] for g in groups for p in g]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    s = (200 - 2 * pad) / max(x1 - x0, y1 - y0)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    return lambda p: (cx + (p[0] - mx) * s, cy + (p[1] - my) * s), s

# ---------- 3D ----------
def rotx(p, a):
    x, y, z = p; c, s = math.cos(a), math.sin(a); return (x, y * c - z * s, y * s + z * c)
def roty(p, a):
    x, y, z = p; c, s = math.cos(a), math.sin(a); return (x * c + z * s, y, -x * s + z * c)
def rotz(p, a):
    x, y, z = p; c, s = math.cos(a), math.sin(a); return (x * c - y * s, x * s + y * c, z)
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def norm(a):
    l = math.sqrt(dot(a, a)) or 1; return (a[0] / l, a[1] / l, a[2] / l)

LIGHT = norm((-0.45, -0.65, 0.62))   # x right, y down (screen), z toward viewer
def shade(n, amb=0.12, spec=0.35):
    n = norm(n)
    d = abs(dot(n, LIGHT))
    h = norm((LIGHT[0], LIGHT[1], LIGHT[2] + 1))
    sp = abs(dot(n, h)) ** 24
    return amb + (1 - amb) * d * 0.85 + spec * sp

def render_quads(quads, view, pad=10, lo=0.0, hi=1.0):
    """quads: list of 4-point 3D lists (world). view: fn(p)->p (rotation). y is screen-down."""
    vq = [[view(p) for p in q] for q in quads]
    proj = [[(p[0], p[1]) for p in q] for q in vq]
    T, _ = fit(proj, pad)
    items = []
    for q in vq:
        n = cross(sub(q[2], q[0]), sub(q[3], q[1]))
        zc = sum(p[2] for p in q) / 4
        v = lo + (hi - lo) * clamp(shade(n), 0, 1)
        items.append((zc, [T((p[0], p[1])) for p in q], int(round(clamp(v, 0, 1) * 47))))
    items.sort(key=lambda t: t[0])
    return "".join(f'<polygon class="h{k}" points="{" ".join(f"{f2(x)},{f2(y)}" for x, y in pts)}"/>' for _, pts, k in items)

# ---------- interlace (ribbons) ----------
def seg_inter(p1, p2, p3, p4):
    d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
    if abs(d) < 1e-9: return None
    t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d
    u = ((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / d
    if 0 <= t < 1 and 0 <= u < 1: return t, u
    return None

def interlace(strands, width, gap, tones, inner=None, closed=True):
    """strands: list of closed point lists (dense). tones: tone per strand.
    inner: optional (tone, width) for a centre line. Alternating over/under."""
    # find crossings
    cr = []  # (sa, ia+ta, sb, ib+tb)
    for a in range(len(strands)):
        for b in range(a, len(strands)):
            A, B = strands[a], strands[b]
            na, nb = len(A), len(B)
            for i in range(na):
                p1, p2 = A[i], A[(i + 1) % na]
                for j in range(nb):
                    if a == b and abs(i - j) <= 2 or (a == b and (i, j) in ((0, nb - 1), (na - 1, 0))): continue
                    if a == b and j <= i: continue
                    r = seg_inter(p1, p2, B[j], B[(j + 1) % nb])
                    if r: cr.append((a, i + r[0], b, j + r[1]))
    over = {}  # crossing id -> strand index that is over (by visit tuple)
    visits = {s: [] for s in range(len(strands))}
    for cid, (a, ta, b, tb) in enumerate(cr):
        visits[a].append((ta, cid, 0)); visits[b].append((tb, cid, 1))
    state = {}  # cid -> which visit-side (0 or 1) is over
    for s in range(len(strands)):
        vs = sorted(visits[s])
        if not vs: continue
        start = None
        for k, (t, cid, side) in enumerate(vs):
            if cid in state:
                start = (k, state[cid] == side); break
        if start is None: start = (0, True)
        k0, is_over = start
        n = len(vs)
        for m in range(n):
            k = (k0 + m) % n
            t, cid, side = vs[k]
            o = is_over if m % 2 == 0 else (not is_over)
            if cid not in state:
                state[cid] = side if o else 1 - side
    def sub_path(S, t0, t1):
        n = len(S); pts = []
        def at(t):
            t %= n; i = int(t); f = t - i
            P, Q = S[i], S[(i + 1) % n]
            return (P[0] + f * (Q[0] - P[0]), P[1] + f * (Q[1] - P[1]))
        pts.append(at(t0))
        k = math.floor(t0) + 1
        while k < t1:
            pts.append(S[k % n]); k += 1
        pts.append(at(t1))
        return pts
    def seglen(S):
        n = len(S); return sum(math.dist(S[i], S[(i + 1) % n]) for i in range(n)) / n
    def draw(pts, s, closed_):
        d = path_d(pts, closed_)
        o = f'<path class="sbk" d="{d}" stroke-width="{f2(width + 2 * gap)}" stroke-linejoin="round"/>'
        o += f'<path class="s{tones[s]}" d="{d}" stroke-width="{f2(width)}" stroke-linejoin="round"/>'
        if inner:
            o += f'<path class="s{inner[0]}" d="{d}" stroke-width="{f2(inner[1])}" stroke-linejoin="round"/>'
        return o
    out = "".join(draw(S, s, True) for s, S in enumerate(strands))
    for cid, (a, ta, b, tb) in enumerate(cr):
        side = state[cid]
        s, t = (a, ta) if side == 0 else (b, tb)
        S = strands[s]
        L = (width * 1.6 + gap * 2) / seglen(S)
        out += draw(sub_path(S, t - L, t + L), s, False)
    return out

def sample(fn, n, t0=0, t1=2 * math.pi):
    return [fn(t0 + (t1 - t0) * i / n) for i in range(n)]
