import React from 'react';
import {AbsoluteFill, useVideoConfig} from 'remotion';
import {useT, useTheme} from '../Reel';
import {pop, prog, easeInOut} from '../lib/time';
import type {
  CommentCtaOverlay, EndCardOverlay, HeadlineOverlay, Overlay, PriceOverlay, SoldGridOverlay,
  StatRingOverlay, StepsOverlay, StickerOverlay, TextOverlay,
} from '../types';

export const OverlayView: React.FC<{overlay: Overlay}> = ({overlay: o}) => {
  switch (o.type) {
    case 'statRing': return <StatRing o={o} />;
    case 'headline': return <Headline o={o} />;
    case 'sticker': return <Sticker o={o} />;
    case 'steps': return <Steps o={o} />;
    case 'soldGrid': return <SoldGrid o={o} />;
    case 'price': return <Price o={o} />;
    case 'commentCta': return <CommentCta o={o} />;
    case 'endCard': return <EndCard o={o} />;
    case 'text': return <TextOv o={o} />;
  }
};

/** fade in at `from`, fade out before `to` */
const useLife = (from: number, to: number, fadeIn = 0.25, fadeOut = 0.25) => {
  const t = useT();
  return Math.min(prog(t, from, fadeIn), 1 - prog(t, to - fadeOut, fadeOut));
};

const shadow = '0 4px 24px rgba(0,0,0,0.55), 0 2px 4px rgba(0,0,0,0.5)';
const fmt = (n: number, d = 0) => n.toLocaleString('en-US', {minimumFractionDigits: d, maximumFractionDigits: d});

// ---------------------------------------------------------------- 8% ring
const StatRing: React.FC<{o: StatRingOverlay}> = ({o}) => {
  const t = useT(), th = useTheme();
  const {width: W} = useVideoConfig();
  const life = useLife(o.from, o.to);
  const N = o.segments ?? 5;
  const R = 250, SW = 26, cx = W / 2, cy = 560;
  const fill = prog(t, o.from + 0.35, 1.6, easeInOut);
  const count = prog(t, o.from + 0.1, 1.2);
  const value = (o.countFrom ?? 0) + (o.value - (o.countFrom ?? 0)) * count;
  const gap = 7; // degrees
  const seg = 360 / N;
  const arc = (a0: number, a1: number) => {
    const p = (a: number) => [cx + R * Math.sin((a * Math.PI) / 180), cy - R * Math.cos((a * Math.PI) / 180)];
    const [x0, y0] = p(a0), [x1, y1] = p(a1);
    return `M${x0},${y0} A${R},${R} 0 ${a1 - a0 > 180 ? 1 : 0} 1 ${x1},${y1}`;
  };
  return (
    <AbsoluteFill style={{opacity: life}}>
      <AbsoluteFill style={{background: `rgba(10,11,14,${o.dim ?? 0.55})`}} />
      <svg width={W} height={1920} style={{position: 'absolute', inset: 0}}>
        {Array.from({length: N}, (_, i) => {
          // RTL reading: segment 1 starts at top and runs clockwise (matches reference)
          const a0 = i * seg + gap / 2, a1 = (i + 1) * seg - gap / 2;
          const local = Math.max(0, Math.min(1, fill * N - i));
          return (
            <g key={i}>
              <path d={arc(a0, a1)} stroke="rgba(255,255,255,0.22)" strokeWidth={SW} fill="none" strokeLinecap="butt" />
              {local > 0 ? (
                <path d={arc(a0, a0 + (a1 - a0) * local)} stroke={th.gold} strokeWidth={SW} fill="none"
                  style={{filter: 'drop-shadow(0 0 14px rgba(212,175,106,0.55))'}} />
              ) : null}
            </g>
          );
        })}
      </svg>
      {(o.segmentLabels ?? []).map((lab, i) => {
        const a = ((i + 0.5) * seg * Math.PI) / 180;
        const x = cx + (R + 78) * Math.sin(a), y = cy - (R + 62) * Math.cos(a);
        return (
          <div key={i} style={{position: 'absolute', left: x, top: y, transform: 'translate(-50%,-50%)', fontFamily: th.font, fontWeight: 800, fontSize: 30, color: 'rgba(255,255,255,0.85)', textShadow: shadow, whiteSpace: 'nowrap'}}>{lab}</div>
        );
      })}
      <div style={{position: 'absolute', left: 0, right: 0, top: cy - 125, textAlign: 'center', direction: 'ltr', fontFamily: th.font, fontWeight: 900, fontSize: 210, lineHeight: 1, color: th.gold, textShadow: '0 6px 30px rgba(0,0,0,0.5)'}}>
        {fmt(value, o.decimals ?? 0)}{o.suffix ?? ''}
      </div>
      {o.headline ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: cy + R + 95, textAlign: 'center', fontFamily: th.font, fontWeight: 800, fontSize: 70, color: '#fff', textShadow: shadow, opacity: prog(t, o.from + 0.5, 0.35), transform: `translateY(${(1 - prog(t, o.from + 0.5, 0.35)) * 20}px)`}}>{o.headline}</div>
      ) : null}
      {o.footnote ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: cy + R + 185, textAlign: 'center', fontFamily: th.font, fontWeight: 500, fontSize: 30, color: 'rgba(255,255,255,0.72)', opacity: prog(t, o.from + 0.7, 0.35)}}>{o.footnote}</div>
      ) : null}
      {(o.lines ?? []).map((l, i) => {
        const s = pop(t, l.at, 0.45);
        return s <= 0 ? null : (
          <div key={i} style={{position: 'absolute', left: 0, right: 0, top: cy + R + 260 + i * 92, textAlign: 'center', fontFamily: th.font, fontWeight: 900, fontSize: l.size ?? 72, color: l.color === 'white' ? '#fff' : th.gold, textShadow: shadow, transform: `scale(${s})`}}>{l.text}</div>
        );
      })}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- stacked headline (top)
const Headline: React.FC<{o: HeadlineOverlay}> = ({o}) => {
  const t = useT(), th = useTheme();
  const life = useLife(o.from, o.to);
  let y = (o.y ?? 0.06) * 1920;
  return (
    <AbsoluteFill style={{opacity: life}}>
      {o.scrim !== false ? <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 760, background: 'linear-gradient(180deg, rgba(0,0,0,0.62), rgba(0,0,0,0.35) 55%, rgba(0,0,0,0))'}} /> : null}
      {o.lines.map((l, i) => {
        const size = l.size ?? 64;
        const top = y; y += size * 1.3;
        const p = prog(t, l.at, 0.35);
        return p <= 0 ? null : (
          <div key={i} style={{position: 'absolute', left: 40, right: 40, top, textAlign: 'center', fontFamily: th.font, fontWeight: l.weight ?? 900, fontSize: size, lineHeight: 1.15, color: l.color === 'gold' ? th.gold : '#fff', textShadow: shadow, opacity: p, transform: `translateY(${(1 - p) * 24}px)`}}>{l.text}</div>
        );
      })}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- sticker / tag
const Sticker: React.FC<{o: StickerOverlay}> = ({o}) => {
  const t = useT(), th = useTheme();
  const s = pop(t, o.from, 0.5);
  const out = 1 - prog(t, o.to - 0.2, 0.2);
  const size = o.size ?? 96;
  const style = o.style ?? 'gold';
  const bg = style === 'gold' ? `linear-gradient(160deg, ${th.goldLight}, ${th.gold})` : style === 'cream' ? th.cream : 'rgba(18,18,20,0.9)';
  const fg = style === 'dark' ? '#fff' : '#1b1712';
  const chipP = o.chip ? pop(t, o.chipAt ?? o.from + 0.4, 0.45) : 0;
  return (
    <div style={{position: 'absolute', left: (o.x ?? 0.5) * 1080, top: (o.y ?? 0.16) * 1920, transform: `translate(-50%,-50%) rotate(${o.rotate ?? -4}deg) scale(${s * out})`, display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <div style={{background: bg, padding: `${size * 0.12}px ${size * 0.38}px ${size * 0.16}px`, borderRadius: 16, boxShadow: '0 16px 40px rgba(0,0,0,0.45), inset 0 0 0 3px rgba(255,255,255,0.25)', textAlign: 'center'}}>
        <div style={{fontFamily: th.font, fontWeight: 900, fontSize: size, lineHeight: 1.12, color: fg, whiteSpace: 'pre-line'}}>{o.text}</div>
      </div>
      {o.sub ? (
        <div style={{marginTop: -10, background: 'rgba(18,18,20,0.92)', color: '#fff', padding: '6px 18px', borderRadius: 8, fontFamily: th.font, fontWeight: 700, fontSize: size * 0.3}}>{o.sub}</div>
      ) : null}
      {o.chip && chipP > 0 ? (
        <div style={{marginTop: 18, transform: `scale(${chipP})`, background: 'rgba(18,18,20,0.88)', border: `2px solid ${th.gold}`, color: th.goldLight, padding: '8px 26px', borderRadius: 40, fontFamily: th.font, fontWeight: 800, fontSize: size * 0.36}}>{o.chip}</div>
      ) : null}
    </div>
  );
};

// ---------------------------------------------------------------- construction steps bar
const Steps: React.FC<{o: StepsOverlay}> = ({o}) => {
  const t = useT(), th = useTheme();
  const life = useLife(o.from, o.to);
  const n = o.steps.length;
  let active = -1;
  o.activeAt.forEach((a, i) => { if (t >= a) active = i; });
  const lastAt = o.activeAt[Math.max(0, active)] ?? o.from;
  const bar = active < 0 ? 0 : (active + prog(t, lastAt, 0.5)) / n;
  return (
    <div style={{position: 'absolute', top: 140, left: 60, right: 60, opacity: life, padding: '22px 26px 26px', borderRadius: 18, background: 'rgba(10,11,14,0.45)'}}>
      <div style={{display: 'flex', justifyContent: 'space-between'}}>
        {o.steps.map((s, i) => (
          <div key={i} style={{fontFamily: th.font, fontWeight: i === active ? 900 : 700, fontSize: i === active ? 52 : 40, color: i <= active ? (i === active ? th.gold : '#fff') : 'rgba(255,255,255,0.5)', textShadow: shadow}}>{s}</div>
        ))}
      </div>
      <div style={{marginTop: 16, height: 6, borderRadius: 3, background: 'rgba(255,255,255,0.25)'}}>
        <div style={{width: `${bar * 100}%`, height: '100%', borderRadius: 3, background: th.gold, marginRight: 0, boxShadow: '0 0 12px rgba(212,175,106,0.8)'}} />
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- units sold grid
const SoldGrid: React.FC<{o: SoldGridOverlay}> = ({o}) => {
  const t = useT(), th = useTheme();
  const life = useLife(o.from, o.to);
  const cw = 150, ch = 66, g = 14;
  const W = o.cols * cw + (o.cols - 1) * g;
  const order = new Map(o.sold.map((idx, k) => [idx, k]));
  return (
    <AbsoluteFill style={{opacity: life}}>
      <AbsoluteFill style={{background: 'rgba(8,9,12,0.45)'}} />
      <div style={{position: 'absolute', left: (1080 - W) / 2, top: 560, width: W, display: 'grid', gridTemplateColumns: `repeat(${o.cols}, ${cw}px)`, gap: g}}>
        {Array.from({length: o.cols * o.rows}, (_, i) => {
          const k = order.get(i);
          const flip = k === undefined ? 0 : prog(t, o.startAt + k * (o.stagger ?? 0.09), 0.3);
          const rot = flip * 180;
          const sold = rot > 90;
          return (
            <div key={i} style={{width: cw, height: ch, borderRadius: 10, transform: `perspective(600px) rotateY(${sold ? rot - 180 : rot}deg)`, background: sold ? `linear-gradient(160deg, ${th.goldLight}, ${th.gold})` : 'rgba(255,255,255,0.10)', border: sold ? 'none' : '2px solid rgba(255,255,255,0.35)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: th.font, fontWeight: 800, fontSize: 28, color: '#1b1712', boxShadow: sold ? '0 6px 18px rgba(0,0,0,0.4)' : 'none'}}>
              {sold ? o.soldLabel ?? 'נמכרה' : ''}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- price reveal
const Price: React.FC<{o: PriceOverlay}> = ({o}) => {
  const t = useT(), th = useTheme();
  const life = useLife(o.from, o.to);
  const p = prog(t, o.valueAt, 0.9);
  const s = pop(t, o.valueAt, 0.5);
  const top = (o.y ?? 0.06) * 1920;
  return (
    <AbsoluteFill style={{opacity: life}}>
      {o.question ? (
        <div style={{position: 'absolute', top, left: 0, right: 0, textAlign: 'center', fontFamily: th.font, fontWeight: 800, fontSize: 64, color: '#fff', textShadow: shadow}}>{o.question}</div>
      ) : null}
      {s > 0 ? (
        <div style={{position: 'absolute', top: top + 110, left: 0, right: 0, textAlign: 'center', direction: 'ltr', fontFamily: th.font, fontWeight: 900, fontSize: 170, lineHeight: 1, color: th.gold, textShadow: '0 8px 40px rgba(0,0,0,0.55)', transform: `scale(${s})`}}>
          {o.prefix ?? ''}{fmt(Math.round((o.value * p) / 1000) * 1000)}{o.suffix ?? ''}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- "write me in the comments"
const CommentCta: React.FC<{o: CommentCtaOverlay}> = ({o}) => {
  const t = useT(), th = useTheme();
  const life = useLife(o.from, o.to, 0.3, 0.01);
  const titleP = pop(t, o.titleAt ?? o.from, 0.5);
  const subP = prog(t, o.subAt ?? o.from + 0.6, 0.35);
  const boxP = prog(t, o.typeAt - 0.3, 0.3);
  const chars = Math.max(0, Math.min(o.typed.length, Math.floor((t - o.typeAt) / 0.09)));
  const cursorOn = Math.floor(t * 2.2) % 2 === 0;
  const heart = o.heartAt !== undefined ? pop(t, o.heartAt, 0.5) : 0;
  return (
    <AbsoluteFill style={{opacity: life}}>
      <AbsoluteFill style={{background: 'rgba(10,10,12,0.12)'}} />
      <div style={{position: 'absolute', top: 210, left: 0, right: 0, textAlign: 'center', fontFamily: th.font, fontWeight: 900, fontSize: 118, color: '#fff', textShadow: shadow, transform: `scale(${titleP})`}}>{o.title}</div>
      {o.sub ? <div style={{position: 'absolute', top: 360, left: 0, right: 0, textAlign: 'center', fontFamily: th.font, fontWeight: 800, fontSize: 58, color: th.gold, textShadow: shadow, opacity: subP}}>{o.sub}</div> : null}
      <div style={{position: 'absolute', top: 500, left: 90, right: 90, display: 'flex', alignItems: 'center', gap: 22, opacity: boxP, transform: `translateY(${(1 - boxP) * 30}px)`}}>
        <div style={{width: 84, height: 84, borderRadius: 42, background: `linear-gradient(160deg, ${th.goldLight}, ${th.gold})`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
          <svg width={40} height={40} viewBox="0 0 24 24"><circle cx="12" cy="8" r="4.2" fill="#2a2418" /><path d="M3.5 21c.8-4.4 4.3-7 8.5-7s7.7 2.6 8.5 7z" fill="#2a2418" /></svg>
        </div>
        <div style={{flex: 1, height: 100, borderRadius: 50, background: th.cream, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 20px 0 40px', boxShadow: '0 10px 30px rgba(0,0,0,0.4)'}}>
          <div style={{fontFamily: th.font, fontWeight: 800, fontSize: 52, color: '#16130f'}}>
            {o.typed.slice(0, chars)}<span style={{opacity: cursorOn ? 1 : 0, fontWeight: 300}}>|</span>
          </div>
          <div style={{width: 64, height: 64, borderRadius: 32, background: th.gold, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <svg width={30} height={30} viewBox="0 0 24 24" style={{transform: 'scaleX(-1)'}}><path d="M3 11.5 20 4l-7.5 17-2.2-7.3z" fill="none" stroke="#1b1712" strokeWidth={2.2} strokeLinejoin="round" /></svg>
          </div>
        </div>
      </div>
      {heart > 0 ? (
        <svg width={90} height={80} viewBox="0 0 24 22" style={{position: 'absolute', top: 650, left: 495, transform: `scale(${heart})`}}>
          <path d="M12 21s-9-5.6-9-12A5 5 0 0 1 12 6a5 5 0 0 1 9 3c0 6.4-9 12-9 12z" fill="#E8344E" />
        </svg>
      ) : null}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- end card / logo lockup
const EndCard: React.FC<{o: EndCardOverlay}> = ({o}) => {
  const t = useT(), th = useTheme();
  const p = prog(t, o.from, 0.8);
  return (
    <AbsoluteFill style={{opacity: p}}>
      <div style={{position: 'absolute', top: 1180, left: 0, right: 0, textAlign: 'center', color: '#fff', transform: `translateY(${(1 - p) * 20}px)`}}>
        <div style={{fontFamily: th.serif, fontWeight: 600, fontSize: 46, letterSpacing: 2, direction: 'ltr'}}>AG</div>
        {o.logoTop ? <div style={{fontFamily: th.serif, fontWeight: 600, fontSize: 22, letterSpacing: 6, direction: 'ltr', opacity: 0.85}}>{o.logoTop}</div> : null}
        <div style={{width: 260, height: 1.5, background: 'rgba(255,255,255,0.6)', margin: '14px auto 18px'}} />
        <div style={{fontFamily: th.serif, fontWeight: 600, fontSize: 70, letterSpacing: 12, direction: 'ltr'}}>{o.title}</div>
        {o.subtitle ? <div style={{fontFamily: th.serif, fontWeight: 600, fontSize: 24, letterSpacing: 10, direction: 'ltr', opacity: 0.8, marginTop: 6}}>{o.subtitle}</div> : null}
        {o.credit ? <div style={{fontFamily: th.font, fontWeight: 700, fontSize: 38, marginTop: 34}}>{o.credit}</div> : null}
      </div>
      <div style={{position: 'absolute', bottom: 70, left: 60, right: 60, textAlign: 'center', fontFamily: th.font, color: 'rgba(255,255,255,0.6)'}}>
        {o.disclaimer ? <div style={{fontSize: 22, fontWeight: 500}}>{o.disclaimer}</div> : null}
        {o.attribution ? <div style={{fontSize: 17, marginTop: 8, direction: 'ltr', opacity: 0.8}}>{o.attribution}</div> : null}
      </div>
    </AbsoluteFill>
  );
};

const TextOv: React.FC<{o: TextOverlay}> = ({o}) => {
  const th = useTheme();
  const life = useLife(o.from, o.to);
  const color = o.color === 'gold' ? th.gold : o.color === 'cream' ? th.cream : '#fff';
  return (
    <div style={{position: 'absolute', left: (o.x ?? 0.5) * 1080, top: (o.y ?? 0.5) * 1920, transform: 'translate(-50%,-50%)', opacity: life, fontFamily: th.font, fontWeight: 900, fontSize: o.size ?? 64, color, textShadow: shadow, whiteSpace: 'nowrap', ...(o.box ? {background: 'rgba(14,14,16,0.85)', padding: '10px 28px', borderRadius: 14} : {})}}>{o.text}</div>
  );
};
