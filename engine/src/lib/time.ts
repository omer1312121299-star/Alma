import {Easing, interpolate} from 'remotion';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const easeOut = Easing.bezier(0.16, 1, 0.3, 1);
export const easeInOut = Easing.bezier(0.65, 0, 0.35, 1);

/** 0..1 progress of an "in" animation that starts at `at` seconds and lasts `dur` seconds. */
export const prog = (t: number, at: number, dur = 0.35, ease = easeOut) =>
  interpolate(t, [at, at + dur], [0, 1], {...clamp, easing: ease});

/** spring-like pop: overshoots a bit then settles. returns scale */
export const pop = (t: number, at: number, dur = 0.4) => {
  const p = Math.max(0, Math.min(1, (t - at) / dur));
  if (p <= 0) return 0;
  // damped spring approximation
  return 1 - Math.exp(-6 * p) * Math.cos(9 * p);
};

/** deterministic pseudo-random 0..1 */
export const rand = (seed: number) => {
  const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
};

export const isVideo = (src: string) => /\.(mp4|mov|webm|m4v)$/i.test(src);
