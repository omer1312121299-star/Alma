import React, {useMemo} from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {useTheme} from '../Reel';
import {clamp, easeOut} from '../lib/time';
import {interpolate} from 'remotion';
import type {CaptionsConfig, CaptionWord} from '../types';

type Chunk = {words: (CaptionWord & {gold: boolean})[]; start: number; end: number};

const norm = (s: string) => s.replace(/[.,!?:;"'״׳()\-–]/g, '').trim();

/** Group words into short chunks (≤ maxWords), breaking on punctuation and pauses. Times in seconds. */
export function buildChunks(words: CaptionWord[], cfg: CaptionsConfig): Chunk[] {
  const max = cfg.maxWords ?? 3;
  const gold = new Set((cfg.highlight ?? []).map(norm));
  const fixes = cfg.fixes ?? {};
  const strip = cfg.stripPunctuation ?? true;
  const ws = words.map((w) => {
    let text = fixes[w.text] ?? fixes[norm(w.text)] ?? w.text;
    if (strip) text = text.replace(/[.,]+$/g, '');
    return {...w, text, gold: gold.has(norm(text))};
  });
  const chunks: Chunk[] = [];
  let cur: Chunk['words'] = [];
  const flush = () => {
    if (cur.length) chunks.push({words: cur, start: cur[0].startMs / 1000, end: cur[cur.length - 1].endMs / 1000});
    cur = [];
  };
  ws.forEach((w, i) => {
    cur.push(w);
    const next = ws[i + 1];
    const endsSentence = /[.,!?]$/.test(words[i].text);
    const pause = next ? next.startMs - w.endMs > 350 : true;
    if (cur.length >= max || endsSentence || pause) flush();
  });
  flush();
  // hold each chunk until the next one starts (max +0.7s after last word)
  chunks.forEach((c, i) => {
    const nextStart = chunks[i + 1]?.start ?? Infinity;
    c.end = Math.min(nextStart, c.end + 0.7);
  });
  const hide = cfg.hide ?? [];
  return chunks.filter((c) => !hide.some(([a, b]) => c.start >= a - 0.05 && c.start < b));
}

export const Captions: React.FC<{cfg: CaptionsConfig; words: CaptionWord[]}> = ({cfg, words}) => {
  const frame = useCurrentFrame();
  const {fps, height} = useVideoConfig();
  const th = useTheme();
  const t = frame / fps;
  const chunks = useMemo(() => buildChunks(words, cfg), [words, cfg]);
  const chunk = chunks.find((c) => t >= c.start - 0.06 && t < c.end);
  if (!chunk) return null;

  const enter = interpolate(t, [chunk.start - 0.06, chunk.start + 0.12], [0, 1], {...clamp, easing: easeOut});
  const y = (cfg.y ?? 0.8) * height;

  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: y, display: 'flex', justifyContent: 'center', transform: 'translateY(-50%)'}}>
      <div
        style={{
          display: 'flex', flexDirection: 'row', direction: 'rtl', gap: 16, alignItems: 'baseline',
          padding: '14px 34px 18px',
          borderRadius: 14,
          background: 'linear-gradient(270deg, rgba(14,14,16,0.88) 0%, rgba(14,14,16,0.82) 70%, rgba(14,14,16,0.55) 100%)',
          boxShadow: '0 10px 30px rgba(0,0,0,0.35)',
          transform: `scale(${0.92 + 0.08 * enter})`,
          opacity: enter,
          maxWidth: 960,
        }}
      >
        {chunk.words.map((w, i) => {
          const ws = w.startMs / 1000;
          const p = interpolate(t, [ws - 0.08, ws + 0.1], [0, 1], {...clamp, easing: easeOut});
          return (
            <span
              key={i}
              style={{
                fontFamily: th.font, fontWeight: 800, fontSize: 60, lineHeight: 1.15,
                color: w.gold ? th.gold : '#ffffff',
                opacity: p,
                transform: `translateY(${(1 - p) * 10}px)`,
                display: 'inline-block',
                textShadow: '0 2px 8px rgba(0,0,0,0.35)',
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    </div>
  );
};
