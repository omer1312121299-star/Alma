// Usage: node scripts/still.mjs <project> 1.2 5.5 37 ...   -> out/stills/<project>_<sec>.jpg  (+ contact sheet)
import path from 'node:path';
import fs from 'node:fs';
import {renderStill} from '@remotion/renderer';
import {args, browserExecutable, prepare} from './common.mjs';

const project = args._[0] ?? 'gazi-demo';
const times = args._.slice(1).map(Number);
const {root, serveUrl, inputProps, composition} = await prepare(project);
const dir = path.join(root, 'out', 'stills');
fs.mkdirSync(dir, {recursive: true});
for (const t of times) {
  const frame = Math.min(composition.durationInFrames - 1, Math.round(t * composition.fps));
  const output = path.join(dir, `${project}_${t}.jpg`);
  await renderStill({serveUrl, composition, inputProps, browserExecutable, frame, output, imageFormat: 'jpeg', jpegQuality: 85,
    scale: Number(args.scale ?? 0.5), chromiumOptions: {gl: 'swangle'}});
  console.log(output);
}
