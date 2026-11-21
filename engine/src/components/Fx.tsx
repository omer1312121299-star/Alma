import React from 'react';
import {AbsoluteFill, staticFile, useCurrentFrame} from 'remotion';
import {rand} from '../lib/time';

/** Edge darkening that focuses the eye on the middle of the frame. */
export const Vignette: React.FC<{amount: number}> = ({amount}) =>
  amount <= 0 ? null : (
    <AbsoluteFill
      style={{
        pointerEvents: 'none',
        background: `radial-gradient(ellipse 75% 60% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,${amount}) 100%)`,
      }}
    />
  );

/** Animated film grain from 4 pre-baked noise tiles (cheap, no per-frame SVG filters). */
export const Grain: React.FC<{amount: number}> = ({amount}) => {
  const frame = useCurrentFrame();
  if (amount <= 0) return null;
  const k = frame % 4;
  const ox = Math.floor(rand(frame) * 256), oy = Math.floor(rand(frame + 99) * 256);
  return (
    <AbsoluteFill
      style={{
        pointerEvents: 'none', opacity: amount * 4, mixBlendMode: 'overlay',
        backgroundImage: `url(${staticFile(`fx/grain${k}.png`)})`, backgroundRepeat: 'repeat',
        backgroundPosition: `${-ox}px ${-oy}px`,
      }}
    />
  );
};
