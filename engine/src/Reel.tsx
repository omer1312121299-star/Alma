import React, {createContext, useContext} from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {DEFAULT_THEME, loadFonts} from './lib/theme';
import type {CaptionWord, Overlay, ReelSpec, Scene, Theme} from './types';
import {SceneView} from './scenes/SceneView';
import {Captions} from './components/Captions';
import {Grain, Vignette} from './components/Fx';
import {OverlayView} from './overlays/OverlayView';

export type ReelProps = {project: string; spec?: ReelSpec; words?: CaptionWord[]};

// ---- shared context: theme + absolute time offset for nested <Sequence>s
export const ThemeCtx = createContext<Theme>(DEFAULT_THEME);
export const useTheme = () => useContext(ThemeCtx);
const OffsetCtx = createContext(0);
/** absolute timeline seconds, valid inside any <TimeScope> */
export const useT = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return useContext(OffsetCtx) + frame / fps;
};
export const TimeScope: React.FC<{from: number; children: React.ReactNode}> = ({from, children}) => (
  <OffsetCtx.Provider value={from}>{children}</OffsetCtx.Provider>
);

export const DEFAULT_TDUR = 0.35;
const tdurOf = (s: Scene, i: number) =>
  i === 0 || !s.transition || s.transition === 'cut' ? 0 : s.transitionDur ?? DEFAULT_TDUR;

export const Reel: React.FC<ReelProps> = ({spec, words = []}) => {
  loadFonts();
  const {fps} = useVideoConfig();
  if (!spec) return <AbsoluteFill style={{background: '#000'}} />;
  const theme = {...DEFAULT_THEME, ...spec.theme};
  const audio = spec.audio ?? {};

  return (
    <ThemeCtx.Provider value={theme}>
      <AbsoluteFill style={{background: '#000', direction: 'rtl', fontFamily: theme.font}}>
        {/* ---------------- scenes (each starts early by its transition duration) */}
        {spec.scenes.map((s, i) => {
          const td = tdurOf(s, i);
          const start = Math.max(0, s.from - td);
          const dur = Math.max(1, Math.round((s.to - start) * fps));
          return (
            <Sequence key={i} from={Math.round(start * fps)} durationInFrames={dur} name={`${i}:${s.type}`}>
              <TimeScope from={start}>
                <SceneView scene={s} tdur={td} index={i} />
              </TimeScope>
            </Sequence>
          );
        })}

        {/* ---------------- graphics overlays */}
        {(spec.overlays ?? []).map((o: Overlay, i) => (
          <Sequence
            key={'o' + i}
            from={Math.round(o.from * fps)}
            durationInFrames={Math.max(1, Math.round((o.to - o.from) * fps))}
            name={`overlay:${o.type}`}
          >
            <TimeScope from={o.from}>
              <OverlayView overlay={o} />
            </TimeScope>
          </Sequence>
        ))}

        {/* ---------------- captions */}
        {spec.captions && words.length > 0 ? <Captions cfg={spec.captions} words={words} /> : null}

        {/* ---------------- finishing */}
        <Vignette amount={spec.fx?.vignette ?? 0.35} />
        <Grain amount={spec.fx?.grain ?? 0.05} />

        {/* ---------------- audio */}
        {audio.voice ? <Audio src={staticFile(audio.voice)} volume={audio.voiceVolume ?? 1} /> : null}
        {audio.music ? (
          <Audio
            src={staticFile(audio.music)}
            loop
            volume={(f) => duckedVolume(f / fps, words, audio.musicVolume ?? 0.16, !!audio.voice)}
          />
        ) : null}
        {audio.sfx
          ? spec.scenes.map((s, i) =>
              i > 0 && s.transition && s.transition !== 'cut' && s.transition !== 'fade' ? (
                <Sequence key={'sfx' + i} from={Math.max(0, Math.round((s.from - tdurOf(s, i)) * fps))} durationInFrames={Math.round(fps * 0.8)}>
                  <Audio src={staticFile('sfx/whoosh.wav')} volume={audio.sfxVolume ?? 0.35} />
                </Sequence>
              ) : null,
            )
          : null}
        {audio.sfx
          ? (spec.overlays ?? [])
              .filter((o) => o.type === 'sticker')
              .map((o, i) => (
                <Sequence key={'pop' + i} from={Math.round(o.from * fps)} durationInFrames={Math.round(fps * 0.5)}>
                  <Audio src={staticFile('sfx/pop.wav')} volume={(audio.sfxVolume ?? 0.35) * 1.2} />
                </Sequence>
              ))
          : null}
      </AbsoluteFill>
    </ThemeCtx.Provider>
  );
};

/** music volume: dips to 35% while a word is spoken, with soft attack/release */
function duckedVolume(t: number, words: CaptionWord[], base: number, hasVoice: boolean) {
  if (!hasVoice || words.length === 0) return base;
  const ms = t * 1000;
  let near = Infinity;
  for (const w of words) {
    if (ms >= w.startMs - 150 && ms <= w.endMs + 250) return base * 0.35;
    near = Math.min(near, Math.abs(ms - w.startMs), Math.abs(ms - w.endMs));
  }
  const k = Math.min(1, near / 500);
  return base * (0.35 + 0.65 * k);
}
