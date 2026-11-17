"""30 'wow' marks, round 2. Each function returns (svg_inner, mono_mode)."""
import math
from geo import *

# ======================= I. IMPOSSIBLE =======================
def impossible_frame(N, R, w, rot, strips, gapw=3.2, cy=100):
    """strips: list of (d0, d1, tones_per_bar list) offsets as fraction of w."""
    V = [(100 + R * math.cos(rot + 2 * math.pi * i / N), cy + R * math.sin(rot + 2 * math.pi * i / N)) for i in range(N)]
    cxm = sum(v[0] for v in V) / N; cym = sum(v[1] for v in V) / N
    lines = []
    for i in range(N):
        A, B = V[i], V[(i + 1) % N]
        ex, ey = B[0] - A[0], B[1] - A[1]; L = math.hypot(ex, ey)
        nx, ny = -ey / L, ex / L
        if (cxm - A[0]) * nx + (cym - A[1]) * ny < 0: nx, ny = -nx, -ny
        lines.append((A, nx, ny))
    def hp(i, d, sign=1):  # sign=1: offset >= d ; sign=-1: offset <= d
        A, nx, ny = lines[i]
        c = -(A[0] * nx + A[1] * ny) - d
        return (sign * nx, sign * ny, sign * c)
    def bar(i, d0, d1, ext=0.0):
        P = BIG
        for h in (hp(i, d0 * w - ext), hp(i, d1 * w + ext, -1), hp((i - 1) % N, 0), hp((i + 1) % N, 0)):
            P = clip(P, *h)
        return P
    out = ""
    for i in range(N):
        for d0, d1, tns in strips:
            out += poly(bar(i, d0, d1), tns[i % len(tns)])
    # corners: bar j=i+1 over bar i at vertex V[i+1]
    for i in range(N):
        j = (i + 1) % N
        # background gap: bar j widened by gap, inside strip i
        G = BIG
        for h in (hp(j, -gapw), hp(j, w + gapw, -1), hp(i, 0), hp(i, w, -1)):
            G = clip(G, *h)
        out += f'<polygon class="bk" points="{" ".join(f"{f2(x)},{f2(y)}" for x, y in G)}"/>'
        for d0, d1, tns in strips:
            P = bar(j, d0, d1)
            for h in (hp(i, -0.6), hp(i, w + 0.6, -1)):
                P = clip(P, *h)
            out += poly(P, tns[j % len(tns)])
    return out

def penrose():
    s = impossible_frame(3, 96, 34, -math.pi / 2, [(0, .5, [14, 10, 6]), (.5, 1, [9, 5, 12])], cy=112)
    return s, "sep"

def infinite_square():
    s = impossible_frame(4, 104, 36, -math.pi / 4,
                         [(0, .3, [14, 12, 14, 12]), (.36, .64, [10, 8, 10, 8]), (.7, 1, [6, 4, 6, 4])])
    return s, "sep"

def iso_hex(C, e):
    return [(C[0] + e * math.cos(math.radians(-90 + 60 * k)), C[1] + e * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]

def cube_faces(C, e, tones=(14, 9, 5)):
    H = iso_hex(C, e)
    top = [C, H[5], H[0], H[1]]; left = [C, H[3], H[4], H[5]]; right = [C, H[1], H[2], H[3]]
    return poly(top, tones[0], ' stroke-linejoin="round"') + poly(left, tones[1]) + poly(right, tones[2])

def ambiguous_cube():
    C = (100, 100); E = 92; e = 42
    H = iso_hex(C, E)
    s = poly([C, H[5], H[0], H[1]], 14) + poly([C, H[3], H[4], H[5]], 9) + poly([C, H[1], H[2], H[3]], 5)
    h = iso_hex(C, e)
    # inverted corner: floor (light) at bottom, walls above
    s += poly([C, h[2], h[3], h[4]], 12) + poly([C, h[4], h[5], h[0]], 4) + poly([C, h[0], h[1], h[2]], 7)
    s += f'<polygon class="sbk" fill="none" stroke-width="2.4" points="{" ".join(f"{f2(x)},{f2(y)}" for x, y in h)}"/>'
    for P in (h[0], h[2], h[4]):
        s += f'<line class="sbk" stroke-width="2.4" x1="{f2(C[0])}" y1="{f2(C[1])}" x2="{f2(P[0])}" y2="{f2(P[1])}"/>'
    for P in (H[1], H[3], H[5]):
        s += f'<line class="sbk" stroke-width="2.4" x1="{f2(C[0])}" y1="{f2(C[1])}" x2="{f2(P[0])}" y2="{f2(P[1])}"/>'
    # redraw small cube over the big-cube seams
    s += poly([C, h[2], h[3], h[4]], 12) + poly([C, h[4], h[5], h[0]], 4) + poly([C, h[0], h[1], h[2]], 7)
    for P in (h[0], h[2], h[4]):
        s += f'<line class="sbk" stroke-width="2.4" x1="{f2(C[0])}" y1="{f2(C[1])}" x2="{f2(P[0])}" y2="{f2(P[1])}"/>'
    return s, "sep"

def cube_ring():
    e = 37; R = 58
    cs = [(100 + R * math.cos(math.radians(-90 + 60 * k)), 100 + R * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]
    def cube(C):
        return f'<g class="cb">{cube_faces(C, e)}</g>'
    s = "".join(cube(C) for C in cs)
    cid = uid("cr")
    hx = iso_hex(cs[5], e + 1.6)
    s += (f'<defs><clipPath id="{cid}"><polygon points="{" ".join(f"{f2(x)},{f2(y)}" for x, y in hx)}"/></clipPath></defs>'
          f'<g clip-path="url(#{cid})">{cube(cs[0])}</g>')
    return s, "sep"

def tesseract():
    V4 = [(x, y, z, w) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1) for w in (-1, 1)]
    E = [(i, j) for i in range(16) for j in range(i + 1, 16) if sum(a != b for a, b in zip(V4[i], V4[j])) == 1]
    def P(v):
        x, y, z, w = v
        k = 1 / (2.6 - w)
        p = (x * k, y * k, z * k)
        p = roty(p, math.radians(45)); p = rotx(p, math.radians(35.264))
        return p
    V3 = [P(v) for v in V4]
    T, _ = fit([[(p[0], p[1]) for p in V3]], 14)
    zs = [p[2] for p in V3]; z0, z1 = min(zs), max(zs)
    items = []
    for i, j in E:
        a, b = V3[i], V3[j]
        z = (a[2] + b[2]) / 2; t = (z - z0) / (z1 - z0)
        inner = V4[i][3] < 0 and V4[j][3] < 0
        wdt = 2.2 + 4.2 * t
        k = tone(0.35 + 0.65 * t)
        A, B = T((a[0], a[1])), T((b[0], b[1]))
        items.append((z, f'<line class="sbk" stroke-linecap="round" stroke-width="{f2(wdt+3)}" x1="{f2(A[0])}" y1="{f2(A[1])}" x2="{f2(B[0])}" y2="{f2(B[1])}"/>'
                         f'<line class="s{k}" stroke-linecap="round" stroke-width="{f2(wdt)}" x1="{f2(A[0])}" y1="{f2(A[1])}" x2="{f2(B[0])}" y2="{f2(B[1])}"/>'))
    items.sort(key=lambda t: t[0])
    return "".join(x for _, x in items), "sep"

def mobius():
    nu, nv = 200, 6; W = 0.6
    def S(u, v):
        return ((1 + v / 2 * math.cos(u / 2)) * math.cos(u), (1 + v / 2 * math.cos(u / 2)) * math.sin(u), v / 2 * math.sin(u / 2))
    Q = []
    for i in range(nu):
        for j in range(nv):
            u0, u1 = 2 * math.pi * i / nu, 2 * math.pi * (i + 1) / nu
            v0, v1 = -W * 2 + 4 * W * j / nv, -W * 2 + 4 * W * (j + 1) / nv
            Q.append([S(u0, v0), S(u1, v0), S(u1, v1), S(u0, v1)])
    view = lambda p: rotx(rotz(p, math.radians(90)), math.radians(-55))
    return render_quads(Q, view, pad=8, lo=0.05), "thr"

# ======================= II. OPTICAL =======================
def op_sphere():
    cx, cy, r = 100, 100, 86; n = 17; sp = 2 * r / n
    L = norm((-0.55, -0.6, 0.58)); s = ""
    for k in range(n):
        yc = cy - r + sp * (k + 0.5)
        dy = yc - cy
        if abs(dy) >= r: continue
        half = math.sqrt(r * r - dy * dy)
        xs = [cx - half + 2 * half * i / 60 for i in range(61)]
        top, bot = [], []
        for x in xs:
            nx, ny = (x - cx) / r, (yc - cy) / r
            nz = math.sqrt(max(0, 1 - nx * nx - ny * ny))
            lum = max(0, nx * L[0] + ny * L[1] + nz * L[2])
            t = sp * (0.24 + 0.68 * (1 - lum) ** 1.2)
            top.append((x, yc - t / 2)); bot.append((x, yc + t / 2))
        s += poly(top + bot[::-1], 13)
    return s, "sep"

def hidden_diamond():
    x0, x1 = 22, 178; p = 9.75
    def stripes(off, k):
        o = ""
        x = x0 + off
        while x < x1 - 0.1:
            o += f'<rect class="g{k}" x="{f2(x)}" y="{x0}" width="{f2(min(p/2, x1-x))}" height="{x1-x0}"/>'
            x += p
        return o
    def diamond(r):
        return f"M100,{100-r} L{100+r},100 L100,{100+r} L{100-r},100 Z"
    c1, c2 = uid("hd"), uid("hd")
    sq = f"M{x0},{x0} H{x1} V{x1} H{x0} Z"
    rA = sq + " " + diamond(70) + " " + diamond(44) + " " + diamond(18)
    rB = diamond(70) + " " + diamond(44) + " " + diamond(18)
    s = (f'<defs><clipPath id="{c1}"><path clip-rule="evenodd" d="{rA}"/></clipPath>'
         f'<clipPath id="{c2}"><path clip-rule="evenodd" d="{rB}"/></clipPath></defs>')
    s += f'<g clip-path="url(#{c1})">{stripes(0, 13)}</g><g clip-path="url(#{c2})">{stripes(p/2, 13)}</g>'
    return s, "sep"

def gravity():
    n = 15; a, b = 18, 182
    def warp(x, y):
        dx, dy = x - 100, y - 100; r = math.hypot(dx, dy)
        f = 1 - 0.62 * math.exp(-(r / 52) ** 2)
        return (100 + dx * f, 100 + dy * f)
    s = ""
    for i in range(n):
        v = a + (b - a) * i / (n - 1)
        h = [warp(a + (b - a) * j / 80, v) for j in range(81)]
        vv = [warp(v, a + (b - a) * j / 80) for j in range(81)]
        for pts in (h, vv):
            s += f'<path class="s10" d="{path_d(pts, False)}" stroke-width="1.5" fill="none"/>'
    gid = uid("gr")
    s += (f'<defs><radialGradient id="{gid}" cx="38%" cy="34%" r="70%"><stop offset="0" style="stop-color:var(--g15)"/>'
          f'<stop offset=".55" style="stop-color:var(--g10)"/><stop offset="1" style="stop-color:var(--g3)"/></radialGradient></defs>'
          f'<circle class="sbk" cx="100" cy="100" r="25" stroke-width="5" style="fill:url(#{gid})"/>')
    return s, "sep"

def shift():
    r = 84; n = 9; gap = 3.4; s = ""
    band = (2 * r - gap * (n - 1)) / n
    for i in range(n):
        y0 = 100 - r + i * (band + gap); y1 = y0 + band
        off = 13 * math.sin((i - 4) * 0.78)
        pts = []
        ys = [y0 + (y1 - y0) * k / 12 for k in range(13)]
        right = [(100 + math.sqrt(max(0, r * r - (y - 100) ** 2)) + off, y) for y in ys]
        left = [(100 - math.sqrt(max(0, r * r - (y - 100) ** 2)) + off, y) for y in ys[::-1]]
        s += poly(right + left, 15 - i)
    return s, "sep"

def tunnel():
    s = ""; r = 88; k = 0; cx = 100
    while r > 6 and k < 20:
        x = 100 + (88 - r) * 0.5
        s += f'<circle class="{"g13" if k % 2 == 0 else "bk"}" cx="{f2(x)}" cy="100" r="{f2(r)}"/>'
        r *= 0.84; k += 1
    return s, "sep"

def tension():
    a, b = 24, 176; n = 15; s = ""
    C = [(a, a), (b, a), (b, b), (a, b)]
    for c in range(4):
        P, Q, R = C[c], C[(c + 1) % 4], C[(c + 2) % 4]
        for i in range(n + 1):
            t = i / n
            A = (P[0] + (Q[0] - P[0]) * t, P[1] + (Q[1] - P[1]) * t)
            B = (Q[0] + (R[0] - Q[0]) * t, Q[1] + (R[1] - Q[1]) * t)
            s += f'<line class="s12" stroke-width="1.15" x1="{f2(A[0])}" y1="{f2(A[1])}" x2="{f2(B[0])}" y2="{f2(B[1])}"/>'
    return s, "sep"

# ======================= III. SCULPTURAL =======================
def twist():
    n = 21; h = 6.2; g = 1.9; s = ""
    for k in range(n):
        th = math.radians(k * 4.3)
        side = 64 - k * 1.3
        a, b = side * math.cos(th), side * math.sin(th)
        W = a + b; x0 = 100 - W / 2
        y = 188 - (k + 1) * (h + g)
        ta = tone(0.86 - 0.3 * k / n); tb = tone(0.22 + 0.25 * k / n)
        s += poly([(x0, y), (x0 + a, y), (x0 + a, y + h), (x0, y + h)], ta)
        if b > 0.3: s += poly([(x0 + a, y), (x0 + W, y), (x0 + W, y + h), (x0 + a, y + h)], tb)
    return s, "sep"

def crystal():
    ap, bp = (100, 10), (100, 190)
    L0, L1, R1, R0 = (58, 66), (84, 58), (116, 58), (142, 66)
    l0, l1, r1, r0 = (58, 144), (84, 152), (116, 152), (142, 144)
    F = [([ap, L0, L1], 15), ([ap, L1, R1], 12), ([ap, R1, R0], 7),
         ([L0, L1, l1, l0], 10), ([L1, R1, (100, 105)], 14), ([L1, (100, 105), l1], 11), ([R1, (100, 105), r1], 8),
         ([(100, 105), l1, r1], 6), ([R1, R0, r0, r1], 4),
         ([l0, l1, bp], 6), ([l1, r1, bp], 3), ([r1, r0, bp], 1)]
    return "".join(poly(p, k) for p, k in F), "sep"

def fold():
    a, b = 26, 174; m = 100; s = ""
    V = [(a, a), (b, a), (b, b), (a, b)]
    q = a + (b - a) * 0.64; q2 = b - (b - a) * 0.64
    M = [(q, a), (b, q), (q2, b), (a, q2)]
    C = (100, 100)
    for k in range(4):
        s += poly([V[k], M[k], C], 14 - (k % 2) * 2) + poly([M[k], V[(k + 1) % 4], C], 5 + (k % 2) * 2)
    return s, "sep"

def shard():
    a = 52; H = 190
    def P3(x, y, z):
        return (( x - y) * math.cos(math.radians(30)), (x + y) * math.sin(math.radians(30)) - z)
    def zt(x, y): return H - 1.25 * (x + a / 2) - 0.55 * (y + a / 2)
    pts = {}
    xs = (-a / 2, a / 2)
    top = [P3(x, y, zt(x, y)) for x, y in ((-a/2, -a/2), (a/2, -a/2), (a/2, a/2), (-a/2, a/2))]
    fx = [P3(a/2, -a/2, 0), P3(a/2, a/2, 0), P3(a/2, a/2, zt(a/2, a/2)), P3(a/2, -a/2, zt(a/2, -a/2))]
    fy = [P3(-a/2, a/2, 0), P3(a/2, a/2, 0), P3(a/2, a/2, zt(a/2, a/2)), P3(-a/2, a/2, zt(-a/2, a/2))]
    T, _ = fit([top, fx, fy], 10)
    tr = lambda L: [T(p) for p in L]
    return poly(tr(fx), 5) + poly(tr(fy), 10) + poly(tr(top), 15), "sep"

def knot():
    n, m = 260, 10; r = 0.48
    def C(t): return (math.sin(t) + 2 * math.sin(2 * t), math.cos(t) - 2 * math.cos(2 * t), -math.sin(3 * t))
    pts = [C(2 * math.pi * i / n) for i in range(n)]
    Q = []
    frames = []
    for i in range(n):
        Tg = norm(sub(pts[(i + 1) % n], pts[i - 1]))
        up = (0, 0, 1) if abs(Tg[2]) < 0.9 else (1, 0, 0)
        N1 = norm(cross(Tg, up)); N2 = cross(Tg, N1)
        frames.append((N1, N2))
    ring = []
    for i in range(n):
        N1, N2 = frames[i]; P = pts[i]
        ring.append([(P[0] + r * (math.cos(2 * math.pi * j / m) * N1[0] + math.sin(2 * math.pi * j / m) * N2[0]),
                      P[1] + r * (math.cos(2 * math.pi * j / m) * N1[1] + math.sin(2 * math.pi * j / m) * N2[1]),
                      P[2] + r * (math.cos(2 * math.pi * j / m) * N1[2] + math.sin(2 * math.pi * j / m) * N2[2])) for j in range(m)])
    for i in range(n):
        for j in range(m):
            Q.append([ring[i][j], ring[(i + 1) % n][j], ring[(i + 1) % n][(j + 1) % m], ring[i][(j + 1) % m]])
    view = lambda p: rotx(rotz(p, math.radians(90)), math.radians(-12))
    return render_quads(Q, view, pad=8, lo=0.08), "thr"

def infinity3d():
    n, m = 260, 5; Wd = 0.3
    def C(t): return (1.7 * math.cos(t), math.sin(2 * t) * 0.9, 0.75 * math.sin(t))
    Q = []
    def S(t, v):
        P = C(t); d = norm(sub(C(t + 1e-3), C(t - 1e-3)))
        z = (0, 0, 1); side = norm(cross(d, z)); nz = cross(side, d)
        ph = t / 2
        wv = (math.cos(ph) * nz[0] + math.sin(ph) * side[0], math.cos(ph) * nz[1] + math.sin(ph) * side[1], math.cos(ph) * nz[2] + math.sin(ph) * side[2])
        return (P[0] + v * wv[0], P[1] + v * wv[1], P[2] + v * wv[2])
    for i in range(n):
        for j in range(m):
            t0, t1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            v0, v1 = -Wd + 2 * Wd * j / m, -Wd + 2 * Wd * (j + 1) / m
            Q.append([S(t0, v0), S(t1, v0), S(t1, v1), S(t0, v1)])
    view = lambda p: rotx(p, math.radians(-24))
    return render_quads(Q, view, pad=6, lo=0.05), "thr"

# ======================= IV. INTERLACE =======================
def borromean():
    rr = 46; d = 31; S = []
    for k in range(3):
        a = math.radians(-90 + 120 * k)
        cx, cy = 100 + d * math.cos(a), 106 + d * math.sin(a)
        S.append(sample(lambda t, cx=cx, cy=cy: (cx + rr * math.cos(t), cy + rr * math.sin(t)), 220))
    return interlace(S, 15, 3.2, [14, 10, 6]), "sep"

def octagram():
    def sq(rot):
        V = [(100 + 80 * math.cos(rot + math.pi / 2 * i), 100 + 80 * math.sin(rot + math.pi / 2 * i)) for i in range(4)]
        pts = []
        for i in range(4):
            A, B = V[i], V[(i + 1) % 4]
            pts += [(A[0] + (B[0] - A[0]) * t / 40, A[1] + (B[1] - A[1]) * t / 40) for t in range(40)]
        return pts
    return interlace([sq(math.pi / 4), sq(0)], 13, 3.2, [14, 8]), "sep"

def trefoil():
    S = sample(lambda t: (100 + 27 * (math.sin(t) + 2 * math.sin(2 * t)), 104 - 27 * (math.cos(t) - 2 * math.cos(2 * t))), 360)
    return interlace([S], 17, 3.4, [13], inner=(6, 3)), "sep"

def gyroscope():
    S = []
    for k in range(3):
        a = math.radians(60 * k)
        S.append(sample(lambda t, a=a: (100 + 86 * math.cos(t) * math.cos(a) - 30 * math.sin(t) * math.sin(a),
                                         100 + 86 * math.cos(t) * math.sin(a) + 30 * math.sin(t) * math.cos(a)), 240))
    s = interlace(S, 9, 2.8, [14, 11, 8])
    gid = uid("gy")
    s += (f'<defs><radialGradient id="{gid}" cx="38%" cy="34%" r="70%"><stop offset="0" style="stop-color:var(--g15)"/>'
          f'<stop offset="1" style="stop-color:var(--g5)"/></radialGradient></defs>'
          f'<circle class="sbk" stroke-width="4" cx="100" cy="100" r="15" style="fill:url(#{gid})"/>')
    return s, "sep"

def weave():
    w = 26; cs = [58, 100, 142]; a0, a1 = 26, 174; g = 3
    s = ""
    for c in cs: s += f'<rect class="g13" x="{c-w/2}" y="{a0}" width="{w}" height="{a1-a0}"/>'
    for c in cs: s += f'<rect class="g7" x="{a0}" y="{c-w/2}" width="{a1-a0}" height="{w}"/>'
    for i, cx in enumerate(cs):
        for j, cy in enumerate(cs):
            if (i + j) % 2 == 0:
                s += f'<rect class="bk" x="{cx-w/2-g}" y="{cy-w/2}" width="{w+2*g}" height="{w}"/>'
                s += f'<rect class="g13" x="{cx-w/2}" y="{cy-w/2-1}" width="{w}" height="{w+2}"/>'
            else:
                s += f'<rect class="bk" x="{cx-w/2}" y="{cy-w/2-g}" width="{w}" height="{w+2*g}"/>'
                s += f'<rect class="g7" x="{cx-w/2-1}" y="{cy-w/2}" width="{w+2}" height="{w}"/>'
    return f'<g transform="rotate(45 100 100) translate(100 100) scale(0.86) translate(-100 -100)">{s}</g>', "sep"

def circle_square():
    def sq():
        V = [(100 + 74 * math.cos(math.pi / 4 + math.pi / 2 * i) * math.sqrt(2) / math.sqrt(2), 0) for i in range(4)]
        h = 60; V = [(100 - h, 100 - h), (100 + h, 100 - h), (100 + h, 100 + h), (100 - h, 100 + h)]
        pts = []
        for i in range(4):
            A, B = V[i], V[(i + 1) % 4]
            pts += [(A[0] + (B[0] - A[0]) * t / 40, A[1] + (B[1] - A[1]) * t / 40) for t in range(40)]
        return pts
    C = sample(lambda t: (100 + 77 * math.cos(t + 0.1), 100 + 77 * math.sin(t + 0.1)), 240)
    return interlace([sq(), C], 13, 3.2, [7, 14]), "sep"

# ======================= V. MATHEMATICAL =======================
def golden():
    U = 200 / 21 * 0.9
    tiles = [(0, 0, 13, 'L'), (13, 0, 8, 'T'), (16, 8, 5, 'R'), (13, 10, 3, 'B'), (13, 8, 2, 'L'), (15, 8, 1, 'T'), (15, 9, 1, 'R')]
    ox, oy = 100 - 21 * U / 2, 100 - 13 * U / 2
    tn = [4, 6, 8, 10, 12, 14, 15]
    s = ""
    for (x, y, sz, _), k in zip(tiles, tn):
        X, Y = ox + x * U, oy + y * U
        s += f'<rect class="g{k}" x="{f2(X+0.9)}" y="{f2(Y+0.9)}" width="{f2(sz*U-1.8)}" height="{f2(sz*U-1.8)}"/>'
    d = ""
    for x, y, sz, o in tiles:
        X, Y, S = ox + x * U, oy + y * U, sz * U
        if o == 'L': a, b = (X, Y + S), (X + S, Y)
        elif o == 'T': a, b = (X, Y), (X + S, Y + S)
        elif o == 'R': a, b = (X + S, Y), (X, Y + S)
        else: a, b = (X + S, Y + S), (X, Y)
        d += (f"M{f2(a[0])},{f2(a[1])} " if not d else "") + f"A{f2(S)},{f2(S)} 0 0 1 {f2(b[0])},{f2(b[1])} "
    s += f'<path class="sbk" d="{d}" stroke-width="4.2" fill="none" stroke-linecap="round"/>'
    return s, "sep"

def fractal():
    N = 27; cell = 172 / N; o = 100 - 86; s = ""
    def hole(i, j):
        while i or j:
            if i % 3 == 1 and j % 3 == 1: return True
            i //= 3; j //= 3
        return False
    for i in range(N):
        for j in range(N):
            if not hole(i, j):
                dd = math.hypot(i - 13, j - 13) / 19
                k = tone(0.95 - 0.45 * dd)
                s += f'<rect class="g{k}" x="{f2(o+i*cell+0.45)}" y="{f2(o+j*cell+0.45)}" width="{f2(cell-0.9)}" height="{f2(cell-0.9)}"/>'
    s += f'<rect class="g15" x="{f2(100-cell*1.5+cell*1.0)}" y="{f2(100-cell*1.5+cell*1.0)}" width="{f2(cell-0.9)}" height="{f2(cell-0.9)}"/>'
    return s, "plain"

def vortex():
    a = math.radians(8); n = 22; side = 168; s = ""; rot = 0
    for k in range(n):
        h = side / 2
        V = [(100 + h * math.cos(rot + math.pi / 4 + math.pi / 2 * i) * math.sqrt(2), 100 + h * math.sin(rot + math.pi / 4 + math.pi / 2 * i) * math.sqrt(2)) for i in range(4)]
        s += poly(V, tone(0.12 + 0.88 * k / (n - 1)))
        side = side / (math.cos(a) + math.sin(a)); rot += a
    return s, "sep"

def aperture():
    n = 8; R = 86; r = 30; s = ""
    P = [(100 + r * math.cos(math.radians(22.5 + 45 * k)), 100 + r * math.sin(math.radians(22.5 + 45 * k))) for k in range(n)]
    def hit(A, B):
        dx, dy = B[0] - A[0], B[1] - A[1]
        fx, fy = A[0] - 100, A[1] - 100
        a = dx * dx + dy * dy; b = 2 * (fx * dx + fy * dy); c = fx * fx + fy * fy - R * R
        t = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
        return (A[0] + t * dx, A[1] + t * dy)
    Aext = [hit(P[k], P[(k + 1) % n]) for k in range(n)]
    for k in range(n):
        A1, A0 = Aext[k], Aext[(k - 1) % n]
        a1 = math.atan2(A1[1] - 100, A1[0] - 100); a0 = math.atan2(A0[1] - 100, A0[0] - 100)
        while a0 < a1: a0 += 2 * math.pi
        arc = [(100 + R * math.cos(a1 + (a0 - a1) * i / 16), 100 + R * math.sin(a1 + (a0 - a1) * i / 16)) for i in range(17)]
        s += poly([P[k]] + arc, [14, 6, 12, 4, 13, 7, 11, 5][k], ' stroke-linejoin="round"')
    s += "".join(f'<line class="sbk" stroke-width="2.6" x1="{f2(P[k][0])}" y1="{f2(P[k][1])}" x2="{f2(Aext[k][0])}" y2="{f2(Aext[k][1])}"/>' for k in range(n))
    return s, "sep"

def north_star():
    s = ""
    def ray(ang, L, b, tl, td):
        a = math.radians(ang)
        tip = (100 + L * math.cos(a), 100 + L * math.sin(a))
        l = (100 + b * math.cos(a - math.pi / 2), 100 + b * math.sin(a - math.pi / 2))
        r = (100 + b * math.cos(a + math.pi / 2), 100 + b * math.sin(a + math.pi / 2))
        return poly([(100, 100), tip, l], tl) + poly([(100, 100), tip, r], td)
    for k in range(8): s += ray(-90 + 22.5 + 45 * k, 46, 8, 11, 5)
    for k in range(4): s += ray(-45 + 90 * k, 66, 12, 13, 6)
    for k in range(4): s += ray(-90 + 90 * k, 94, 15, 15, 7)
    return s, "sep"

def guilloche():
    s = ""
    for ring, (r0, amp, nlob, cnt, k) in enumerate([(70, 13, 14, 16, 13), (38, 9, 9, 12, 10)]):
        for c in range(cnt):
            ph = 2 * math.pi * c / cnt / nlob
            pts = [(100 + (r0 + amp * math.sin(nlob * (t + ph) * 1.0)) * math.cos(t),
                    100 + (r0 + amp * math.sin(nlob * (t + ph))) * math.sin(t)) for t in [2 * math.pi * i / 400 for i in range(400)]]
            s += f'<path class="s{k}" d="{path_d(pts)}" stroke-width=".75" fill="none"/>'
    s += f'<circle class="s13" cx="100" cy="100" r="92" fill="none" stroke-width="1.6"/>'
    s += f'<circle class="s13" cx="100" cy="100" r="87" fill="none" stroke-width=".6"/>'
    s += f'<circle class="g14" cx="100" cy="100" r="9"/>'
    return s, "sep"

MARKS = {
    1: penrose, 2: infinite_square, 3: ambiguous_cube, 4: cube_ring, 5: tesseract, 6: mobius,
    7: op_sphere, 8: hidden_diamond, 9: gravity, 10: shift, 11: tunnel, 12: tension,
    13: twist, 14: crystal, 15: fold, 16: shard, 17: knot, 18: infinity3d,
    19: borromean, 20: octagram, 21: trefoil, 22: gyroscope, 23: weave, 24: circle_square,
    25: golden, 26: fractal, 27: vortex, 28: aperture, 29: north_star, 30: guilloche,
}

_cache = {}
def svg(n, size=None, cls=""):
    if n not in _cache or "url(#" in _cache[n][0] or "id=" in _cache[n][0]:
        _cache[n] = MARKS[n]()
    body, mode = _cache[n]
    if "id=" in body:   # regenerate for unique ids
        body, mode = MARKS[n]()
    st = f' style="width:{size};height:{size}"' if size else ""
    return f'<svg class="mk {mode} {cls}" viewBox="0 0 200 200"{st} xmlns="http://www.w3.org/2000/svg">{body}</svg>'
