// Usage: node scripts/render.mjs <project> [--out file.mp4] [--from 10 --to 20] [--scale 0.5] [--crf 18]
import path from 'node:path';
import fs from 'node:fs';
import {renderMedia} from '@remotion/renderer';
import {args, browserExecutable, prepare} from './common.mjs';

const project = args._[0] ?? 'gazi-demo';
const {root, serveUrl, inputProps, composition} = await prepare(project);
const fps = composition.fps;
const frameRange = args.from !== undefined
  ? [Math.round(Number(args.from) * fps), Math.min(composition.durationInFrames - 1, Math.round(Number(args.to ?? composition.durationInFrames / fps) * fps) - 1)]
  : undefined;
const out = path.resolve(args.out ?? path.join(root, 'out', `${project}.mp4`));
fs.mkdirSync(path.dirname(out), {recursive: true});
const t0 = Date.now();
let last = -1;
await renderMedia({
  serveUrl, composition, inputProps, browserExecutable,
  codec: 'h264', crf: Number(args.crf ?? 18), pixelFormat: 'yuv420p',
  audioCodec: 'aac', audioBitrate: '192k',
  scale: Number(args.scale ?? 1),
  frameRange,
  concurrency: Number(args.concurrency ?? 4),
  chromiumOptions: {gl: 'swangle'},
  outputLocation: out,
  onProgress: ({progress}) => {
    const p = Math.floor(progress * 20);
    if (p !== last) { last = p; process.stdout.write(`\r${Math.round(progress * 100)}% `); }
  },
});
console.log(`\nrendered ${out} in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
