import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {useT, useTheme} from '../Reel';
import {clamp, easeOut, rand} from '../lib/time';
import type {Scene, Transition} from '../types';
import {MediaSceneView, ColorSceneView, SplitSceneView} from './MediaScene';
import {MapSceneView} from './MapScene';
import {PolaroidSceneView} from './PolaroidScene';

const GRADES: Record<string, string> = {
  none: 'none',
  warm: 'saturate(1.06) contrast(1.06) sepia(0.10) brightness(1.02)',
  cool: 'saturate(0.92) contrast(1.08) hue-rotate(-6deg)',
  dark: 'brightness(0.72) contrast(1.08) saturate(0.9)',
  night: 'brightness(0.85) contrast(1.12) saturate(1.1) hue-rotate(-8deg)',
};

export const SceneView: React.FC<{scene: Scene; tdur: number; index: number}> = ({scene, tdur, index}) => {
  const body = (() => {
    switch (scene.type) {
      case 'media': return <MediaSceneView s={scene} />;
      case 'map': return <MapSceneView s={scene} />;
      case 'polaroid': return <PolaroidSceneView s={scene} />;
      case 'split': return <SplitSceneView s={scene} />;
      case 'color': return <ColorSceneView s={scene} />;
    }
  })();
  const graded = (
    <AbsoluteFill style={{filter: GRADES[scene.grade ?? 'warm']}}>
      {body}
      {scene.badge ? <Badge text={scene.badge} /> : null}
    </AbsoluteFill>
  );
  return (
    <Enter type={scene.transition ?? 'cut'} dur={tdur} start={scene.from - tdur} seed={index}>
      {graded}
    </Enter>
  );
};

/** Wraps the incoming scene and animates it in over `dur` seconds starting at `start` (absolute). */
const Enter: React.FC<{type: Transition; dur: number; start: number; seed: number; children: React.ReactNode}> = ({
  type, dur, start, seed, children,
}) => {
  const t = useT();
  if (dur <= 0 || type === 'cut') return <AbsoluteFill>{children}</AbsoluteFill>;
  const p = interpolate(t, [start, start + dur], [0, 1], clamp);
  if (p >= 1) return <AbsoluteFill>{children}</AbsoluteFill>;
  const e = easeOut(p);

  switch (type) {
    case 'fade':
      return <AbsoluteFill style={{opacity: e}}>{children}</AbsoluteFill>;
    case 'blur':
      return <AbsoluteFill style={{opacity: Math.min(1, p * 2), filter: `blur(${(1 - e) * 30}px)`}}>{children}</AbsoluteFill>;
    case 'zoom':
      return (
        <AbsoluteFill style={{opacity: Math.min(1, p * 2.5), transform: `scale(${1.28 - 0.28 * e})`, filter: `blur(${(1 - e) * 14}px)`}}>
          {children}
        </AbsoluteFill>
      );
    case 'whip':
      return (
        <AbsoluteFill style={{transform: `translateX(${-(1 - e) * 100}%)`, filter: `blur(${(1 - e) * 24}px)`}}>{children}</AbsoluteFill>
      );
    case 'flash':
      return (
        <AbsoluteFill>
          <AbsoluteFill style={{opacity: p > 0.45 ? 1 : 0}}>{children}</AbsoluteFill>
          <AbsoluteFill style={{background: '#fff', opacity: 1 - Math.abs(p - 0.45) / 0.55}} />
        </AbsoluteFill>
      );
    case 'glitch': {
      // Horizontal slices displaced sideways, collapsing to 0 — plus chroma-shifted ghost copies.
      const N = 9;
      const amp = Math.pow(1 - p, 1.6);
      const step = Math.floor(p * 10); // re-randomize ~10x across the transition (stuttery)
      const slices = Array.from({length: N}, (_, i) => {
        const r = rand(seed * 31 + i * 7 + step * 13);
        const top = (i / N) * 100;
        const h = 100 / N;
        const dx = (r - 0.5) * 2 * 260 * amp;
        const show = p > 0.08 || r > 0.5;
        return (
          <AbsoluteFill
            key={i}
            style={{
              clipPath: `inset(${top}% 0 ${100 - top - h}% 0)`,
              transform: `translateX(${dx}px) scaleX(${1 + amp * 0.15 * r})`,
              opacity: show ? 1 : 0,
            }}
          >
            {children}
          </AbsoluteFill>
        );
      });
      return (
        <AbsoluteFill>
          {slices}
          <AbsoluteFill style={{mixBlendMode: 'screen', opacity: 0.55 * amp, transform: `translateX(${18 * amp}px)`, filter: 'sepia(1) saturate(6) hue-rotate(-50deg)'}}>
            {children}
          </AbsoluteFill>
          <AbsoluteFill style={{mixBlendMode: 'screen', opacity: 0.45 * amp, transform: `translateX(${-18 * amp}px)`, filter: 'sepia(1) saturate(6) hue-rotate(150deg)'}}>
            {children}
          </AbsoluteFill>
        </AbsoluteFill>
      );
    }
    default:
      return <AbsoluteFill>{children}</AbsoluteFill>;
  }
};

export const Badge: React.FC<{text: string}> = ({text}) => {
  const th = useTheme();
  return (
    <div
      style={{
        position: 'absolute', top: 110, right: 64, padding: '6px 16px', borderRadius: 8,
        background: 'rgba(0,0,0,0.38)', border: '1.5px solid rgba(255,255,255,0.35)',
        color: 'rgba(255,255,255,0.9)', fontFamily: th.font, fontWeight: 500, fontSize: 26,
      }}
    >
      {text}
    </div>
  );
};
