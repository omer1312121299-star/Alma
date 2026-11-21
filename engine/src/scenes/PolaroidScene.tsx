import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {useT, useTheme} from '../Reel';
import {prog} from '../lib/time';
import type {PolaroidScene} from '../types';

/** A photo dropped onto the screen inside a white instant-photo frame, over a blurred backdrop. */
export const PolaroidSceneView: React.FC<{s: PolaroidScene}> = ({s}) => {
  const t = useT();
  const th = useTheme();
  const p = prog(t, s.from - 0.1, 0.55);
  const drift = (t - s.from) / Math.max(0.1, s.to - s.from);
  const rot = (s.rotate ?? -4) * (1 - 0.25 * p) + drift * 1.5;
  const frame = (child: React.ReactNode, extra: React.CSSProperties) => (
    <div style={{
      position: 'absolute', left: '50%', top: '47%', width: 780, padding: '26px 26px 110px', background: '#f7f4ee',
      boxShadow: '0 30px 80px rgba(0,0,0,0.55), 0 4px 12px rgba(0,0,0,0.4)', ...extra,
    }}>
      {child}
    </div>
  );
  return (
    <AbsoluteFill style={{background: '#16130f', overflow: 'hidden'}}>
      <Img src={staticFile(s.bg ?? s.src)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'blur(26px) brightness(0.45) saturate(0.8)', transform: 'scale(1.15)'}} />
      {frame(<div style={{width: '100%', height: 900, background: '#ddd'}} />, {
        transform: `translate(-50%, -50%) rotate(${rot + 7}deg) translateY(${(1 - p) * 300}px)`, opacity: 0.9 * p,
      })}
      {frame(
        <>
          <Img src={staticFile(s.src)} style={{width: '100%', height: 900, objectFit: 'cover', display: 'block', transform: `scale(${1.04 + drift * 0.05})`}} />
          {s.caption ? (
            <div style={{position: 'absolute', bottom: 30, left: 0, right: 0, textAlign: 'center', fontFamily: th.font, fontWeight: 700, fontSize: 44, color: '#2b2620'}}>{s.caption}</div>
          ) : null}
        </>,
        {transform: `translate(-50%, -50%) rotate(${rot}deg) translateY(${(1 - p) * 700}px) scale(${1.15 - 0.15 * p})`, overflow: 'hidden'},
      )}
    </AbsoluteFill>
  );
};
