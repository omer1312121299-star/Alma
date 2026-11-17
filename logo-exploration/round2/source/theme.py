def lerp(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
def hx(c): return tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
def ramp(stops):
    stops = [(p, hx(c)) for p, c in stops]; out = []
    for k in range(16):
        t = k / 15
        for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
            if p0 <= t <= p1:
                out.append('#%02x%02x%02x' % lerp(c0, c1, (t - p0) / (p1 - p0) if p1 > p0 else 0)); break
    return out
GOLD = ramp([(0, '#22190c'), (.3, '#5e4423'), (.62, '#b48b4c'), (.82, '#dcbd80'), (1, '#fff3d4')])
INK = ramp([(0, '#0d0c0b'), (.5, '#3a3128'), (.8, '#7f6643'), (1, '#b8955c')])
def ramp48(stops):
    stops2=[(p, hx(c)) for p,c in stops]; out=[]
    for k in range(48):
        tt=k/47
        for (p0,c0),(p1,c1) in zip(stops2,stops2[1:]):
            if p0<=tt<=p1: out.append('#%02x%02x%02x' % lerp(c0,c1,(tt-p0)/(p1-p0))); break
    return out
GOLDS=[(0, '#22190c'), (.3, '#5e4423'), (.62, '#b48b4c'), (.82, '#dcbd80'), (1, '#fff3d4')]
INKS=[(0, '#0d0c0b'), (.5, '#3a3128'), (.8, '#7f6643'), (1, '#b8955c')]
def hv(r): return ';'.join(f'--h{k}:{c}' for k,c in enumerate(r))
def vars_(r): return ";".join(f"--g{k}:{c}" for k, c in enumerate(r))
CSS = f"""
.mk polygon, .mk rect, .mk circle {{ }}
""" + "".join(f".mk .g{k}{{fill:var(--g{k});stroke:var(--g{k});stroke-width:.45}} .mk .s{k}{{stroke:var(--g{k});fill:none}}\n" for k in range(16)) + f"""
""" + "".join(f".mk .h{k}{{fill:var(--h{k});stroke:var(--h{k});stroke-width:.6}}" for k in range(48)) + f"""
.mk .bk {{ fill:var(--bg); stroke:none }} .mk .sbk {{ stroke:var(--bg); fill:none }}
.th-dark {{ --bg:#0c0b0a; --fg:#f2ead9; {vars_(GOLD)}; {hv(ramp48(GOLDS))} }}
.th-light {{ --bg:#ece6dc; --fg:#121110; {vars_(INK)}; {hv(ramp48(INKS))} }}
.th-mono {{ --bg:#121110; --fg:#ece6dc; {vars_(['#ece6dc']*16)}; {hv(['#ece6dc']*48)} }}
.th-monol {{ --bg:#ffffff; --fg:#121110; {vars_(['#121110']*16)}; {hv(['#121110']*48)} }}
.th-mono .mk.sep polygon, .th-mono .mk.sep rect, .th-monol .mk.sep polygon, .th-monol .mk.sep rect {{ stroke:var(--bg) !important; stroke-width:2.2 !important }}
""" + "".join(f".th-mono .mk.thr .g{k}, .th-monol .mk.thr .g{k}{{fill:var(--bg)!important;stroke:var(--bg)!important}}\n" for k in range(5)).replace(".g", ".h")
