import React from 'react';
import {CalculateMetadataFunction, Composition, staticFile} from 'remotion';
import {Reel, ReelProps} from './Reel';
import type {CaptionWord, ReelSpec} from './types';

// The composition receives only `project` (folder name under public/projects).
// Spec + captions are fetched at render time, so editing JSON never requires code changes.
const calculateMetadata: CalculateMetadataFunction<ReelProps> = async ({props}) => {
  const base = `projects/${props.project}`;
  const spec: ReelSpec = await fetch(staticFile(`${base}/video.json`)).then((r) => r.json());
  let words: CaptionWord[] = [];
  if (spec.captions?.src) {
    words = await fetch(staticFile(spec.captions.src)).then((r) => r.json());
  }
  const fps = spec.meta.fps ?? 30;
  return {
    durationInFrames: Math.round(spec.meta.duration * fps),
    fps,
    width: spec.meta.width ?? 1080,
    height: spec.meta.height ?? 1920,
    props: {...props, spec, words},
  };
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Reel"
    component={Reel}
    defaultProps={{project: 'gazi-demo'} as ReelProps}
    calculateMetadata={calculateMetadata}
    durationInFrames={300}
    fps={30}
    width={1080}
    height={1920}
  />
);
