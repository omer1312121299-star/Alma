import React from 'react';
import {AbsoluteFill, Img, OffthreadVideo, staticFile, interpolate} from 'remotion';
import {useT} from '../Reel';
import {clamp, easeInOut, isVideo} from '../lib/time';
import type {ColorScene, MediaScene, SplitScene} from '../types';

/** Cover-fit image or video with Ken Burns motion. */
export const Media: React.FC<{
  src: string; t: number; from: number; to: number;
  move?: MediaScene['move']; amount?: number; focus?: [number, number]; startFrom?: number;
  style?: React.CSSProperties;
}> = ({src, t, from, to, move = 'in', amount = 0.12, focus = [0.5, 0.5], startFrom = 0, style}) => {
  const p = interpolate(t, [from, to], [0, 1], {...clamp, easing: easeInOut});
  let scale = 1.04, tx = 0, ty = 0;
  const a = amount;
  switch (move) {
    case 'in': scale = 1.02 + a * p; break;
    case 'out': scale = 1.02 + a * (1 - p); break;
    case 'left': scale = 1.04 + a; tx = (0.5 - p) * a * 100 * 0.8; break;
    case 'right': scale = 1.04 + a; tx = (p - 0.5) * a * 100 * 0.8; break;
    case 'up': scale = 1.04 + a; ty = (0.5 - p) * a * 100 * 0.8; break;
    case 'down': scale = 1.04 + a; ty = (p - 0.5) * a * 100 * 0.8; break;
    case 'none': scale = 1; break;
  }
  const common: React.CSSProperties = {
    width: '100%', height: '100%', objectFit: 'cover',
    objectPosition: `${focus[0] * 100}% ${focus[1] * 100}%`,
    transform: `translate(${tx}%, ${ty}%) scale(${scale})`,
    ...style,
  };
  return isVideo(src) ? (
    <OffthreadVideo src={staticFile(src)} startFrom={Math.round(startFrom * 30)} muted style={common} />
  ) : (
    <Img src={staticFile(src)} style={common} />
  );
};

export const MediaSceneView: React.FC<{s: MediaScene}> = ({s}) => {
  const t = useT();
  if (s.blurBg) {
    return (
      <AbsoluteFill style={{overflow: 'hidden', background: '#000'}}>
        <Media src={s.src} t={t} from={s.from} to={s.to} move="none" style={{filter: 'blur(40px) brightness(0.55)', transform: 'scale(1.2)'}} />
        <AbsoluteFill style={{justifyContent: 'center'}}>
          <Media src={s.src} t={t} from={s.from} to={s.to} move={s.move} amount={s.amount}
            style={{objectFit: 'contain', height: '100%'}} />
        </AbsoluteFill>
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{overflow: 'hidden', background: '#000'}}>
      <Media src={s.src} t={t} from={s.from} to={s.to} move={s.move} amount={s.amount} focus={s.focus} startFrom={s.startFrom} />
    </AbsoluteFill>
  );
};

export const SplitSceneView: React.FC<{s: SplitScene}> = ({s}) => {
  const t = useT();
  const half: React.CSSProperties = {position: 'absolute', left: 0, right: 0, height: '50%', overflow: 'hidden'};
  return (
    <AbsoluteFill style={{background: '#0b0b0c'}}>
      <div style={{...half, top: 0}}>
        <Media src={s.top} t={t} from={s.from} to={s.to} move="left" amount={0.08} />
      </div>
      <div style={{...half, bottom: 0}}>
        <Media src={s.bottom} t={t} from={s.from} to={s.to} move="right" amount={0.08} />
      </div>
      <div style={{position: 'absolute', top: 'calc(50% - 3px)', left: 0, right: 0, height: 6, background: '#0b0b0c'}} />
    </AbsoluteFill>
  );
};

export const ColorSceneView: React.FC<{s: ColorScene}> = ({s}) => {
  const t = useT();
  return (
    <AbsoluteFill style={{background: s.color ?? '#141518', overflow: 'hidden'}}>
      {s.src ? (
        <Media src={s.src} t={t} from={s.from} to={s.to} move="in" amount={0.06}
          style={{filter: 'blur(12px) brightness(0.62) saturate(0.9)'}} />
      ) : null}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.35), rgba(0,0,0,0.1) 40%, rgba(0,0,0,0.55))'}} />
    </AbsoluteFill>
  );
};
