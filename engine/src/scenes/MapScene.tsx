import React from 'react';
import {AbsoluteFill, Img, staticFile, useVideoConfig} from 'remotion';
import {useT, useTheme} from '../Reel';
import {easeInOut, pop, prog} from '../lib/time';
import type {Camera, MapScene, Pin} from '../types';

/** Interpolate camera keyframes (t relative to scene start). */
function cameraAt(cams: Camera[], rt: number): Camera {
  if (cams.length === 0) return {t: 0, x: 0.5, y: 0.5, zoom: 1};
  if (rt <= cams[0].t) return cams[0];
  for (let i = 0; i < cams.length - 1; i++) {
    const a = cams[i], b = cams[i + 1];
    if (rt <= b.t) {
      const k = easeInOut((rt - a.t) / Math.max(0.001, b.t - a.t));
      // zoom interpolated in log space = perceptually constant speed (Google-Earth feel)
      const z = Math.exp(Math.log(a.zoom) + (Math.log(b.zoom) - Math.log(a.zoom)) * k);
      return {t: rt, x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, zoom: z};
    }
  }
  return cams[cams.length - 1];
}

export const MapSceneView: React.FC<{s: MapScene}> = ({s}) => {
  const t = useT();
  const th = useTheme();
  const {width: W, height: H} = useVideoConfig();
  const cam = cameraAt(s.camera, t - s.from);

  // cover scale, then camera zoom; clamp so the image always covers the frame
  const s0 = Math.max(W / s.width, H / s.height);
  const sc = s0 * cam.zoom;
  const halfW = W / 2 / sc, halfH = H / 2 / sc;
  const cx = Math.min(Math.max(cam.x * s.width, halfW), s.width - halfW);
  const cy = Math.min(Math.max(cam.y * s.height, halfH), s.height - halfH);
  const toScreen = (x: number, y: number) => ({X: W / 2 + (x * s.width - cx) * sc, Y: H / 2 + (y * s.height - cy) * sc});

  const pinsByName = Object.fromEntries((s.pins ?? []).map((p) => [p.name, p]));

  return (
    <AbsoluteFill style={{overflow: 'hidden', background: '#0d0f12'}}>
      <Img
        src={staticFile(s.src)}
        style={{
          position: 'absolute', left: 0, top: 0, width: s.width, height: s.height,
          transformOrigin: '0 0',
          transform: `translate(${W / 2 - cx * sc}px, ${H / 2 - cy * sc}px) scale(${sc})`,
          filter: 'saturate(0.7) brightness(0.66) contrast(1.15)',
        }}
      />
      {/* Google-Earth-like atmosphere: cool tint + dark edges */}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(10,20,35,0.45) 0%, rgba(10,20,35,0.05) 30%, rgba(10,20,35,0.05) 65%, rgba(5,8,12,0.6) 100%)'}} />

      {/* routes */}
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {(s.route ?? []).map((r, i) => {
          const a = pinsByName[r.from], b = pinsByName[r.to];
          if (!a || !b) return null;
          const A = toScreen(a.x, a.y), B = toScreen(b.x, b.y);
          const mx = (A.X + B.X) / 2, my = (A.Y + B.Y) / 2 - Math.hypot(B.X - A.X, B.Y - A.Y) * 0.18;
          const p = prog(t, r.at, r.dur ?? 0.9);
          const len = Math.hypot(B.X - A.X, B.Y - A.Y) * 1.15;
          return (
            <path key={i} d={`M${A.X},${A.Y} Q${mx},${my} ${B.X},${B.Y}`} fill="none" stroke={th.gold}
              strokeWidth={6} strokeLinecap="round" strokeDasharray={`${len}`} strokeDashoffset={len * (1 - p)}
              style={{filter: 'drop-shadow(0 0 8px rgba(212,175,106,0.7))'}} />
          );
        })}
      </svg>

      {(s.pins ?? []).map((p, i) => {
        const {X, Y} = toScreen(p.x, p.y);
        return <PinLabel key={i} pin={p} X={X} Y={Y} t={t} />;
      })}

      {s.title ? <MapTitle text={s.title.text} t={t} at={s.title.at} to={s.title.to ?? s.to} /> : null}

      <div style={{position: 'absolute', bottom: 26, left: 30, fontSize: 18, color: 'rgba(255,255,255,0.55)', fontFamily: 'Heebo', direction: 'ltr'}}>
        Copernicus Sentinel-2
      </div>
    </AbsoluteFill>
  );
};

const PinLabel: React.FC<{pin: Pin; X: number; Y: number; t: number}> = ({pin, X, Y, t}) => {
  const th = useTheme();
  const out = pin.until !== undefined ? prog(t, pin.until - 0.2, 0.2) : 0;
  const sc = pop(t, pin.at, 0.45) * (1 - out);
  if (sc <= 0.001) return null;
  let [ox, oy] = pin.offset ?? [0, 0];
  // keep the card on screen: estimate its width from text length
  const fs = pin.latin ? 50 : 44;
  const estW = Math.max(pin.name.length * fs * (pin.latin ? 0.5 : 0.56), (pin.sub ?? '').length * 15) + 44;
  const left = X + ox - estW / 2, right = X + ox + estW / 2, M = 28;
  if (left < M) ox += M - left;
  if (right > 1080 - M) ox -= right - (1080 - M);
  const active = pin.activeFrom !== undefined && t >= pin.activeFrom && (pin.activeTo === undefined || t < pin.activeTo);
  const ap = pin.activeFrom !== undefined ? prog(t, pin.activeFrom, 0.25) : 0;
  const bg = active ? th.gold : th.cream;
  const icon = pin.icon ?? 'pin';
  return (
    <div style={{position: 'absolute', left: X, top: Y, transform: `translate(-50%, -100%) scale(${sc * (active ? 1 + 0.08 * ap : 1)})`, transformOrigin: '50% 100%', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
      <div style={{
        transform: `translate(${ox}px, ${oy}px)`,
        background: bg, borderRadius: 10, padding: pin.sub ? '8px 18px 6px' : '8px 20px',
        boxShadow: active ? '0 0 0 3px rgba(255,255,255,0.65), 0 10px 30px rgba(0,0,0,0.45)' : '0 8px 24px rgba(0,0,0,0.45)',
        textAlign: 'center', whiteSpace: 'nowrap',
      }}>
        <div style={{
          fontFamily: pin.latin ? th.serif : th.font, fontWeight: pin.latin ? 600 : 800,
          fontSize: pin.latin ? 50 : 44, lineHeight: 1.05, color: th.ink, direction: pin.latin ? 'ltr' : 'rtl',
        }}>{pin.name}</div>
        {pin.sub ? <div style={{fontFamily: th.font, fontWeight: 600, fontSize: 28, color: 'rgba(17,18,20,0.75)', marginTop: 2}}>{pin.sub}</div> : null}
      </div>
      {icon === 'pin' ? (
        <svg width={54} height={70} viewBox="0 0 44 58" style={{marginTop: 6, filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.5))'}}>
          <path d="M22 2C11 2 3 10.5 3 21c0 14 19 34 19 34s19-20 19-34C41 10.5 33 2 22 2z" fill={th.gold} stroke="#3a2f1c" strokeWidth={2} />
          <circle cx={22} cy={21} r={7} fill="#2a2418" />
        </svg>
      ) : icon === 'metro' ? (
        <div style={{marginTop: 8, width: 44, height: 44, borderRadius: 22, background: '#2F6FD6', border: '3px solid #fff', color: '#fff', fontWeight: 900, fontSize: 24, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Heebo', boxShadow: '0 4px 10px rgba(0,0,0,0.5)'}}>M</div>
      ) : (
        <div style={{marginTop: 6, width: 14, height: 14, borderRadius: 7, background: th.gold, border: '2px solid #fff'}} />
      )}
    </div>
  );
};

const MapTitle: React.FC<{text: string; t: number; at: number; to: number}> = ({text, t, at, to}) => {
  const p = prog(t, at, 0.5);
  const out = prog(t, to - 0.35, 0.35);
  if (p <= 0) return null;
  return (
    <div style={{
      position: 'absolute', top: '17%', left: 0, right: 0, textAlign: 'center',
      fontFamily: 'Heebo', fontWeight: 900, fontSize: 128, color: '#fff', letterSpacing: -1,
      textShadow: '0 6px 40px rgba(0,0,0,0.65), 0 2px 6px rgba(0,0,0,0.6)',
      opacity: p * (1 - out), transform: `translateY(${(1 - p) * 40}px) scale(${0.94 + 0.06 * p})`,
    }}>{text}</div>
  );
};
