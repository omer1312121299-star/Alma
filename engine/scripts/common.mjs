import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {selectComposition} from '@remotion/renderer';

const CANDIDATES = [
  process.env.REMOTION_BROWSER,
  '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell',
  '/opt/pw-browsers/headless_shell_as_downloaded/chrome-headless-shell',
];
export const browserExecutable = CANDIDATES.find((p) => p && fs.existsSync(p)) ?? null;

export const args = (() => {
  const a = process.argv.slice(2);
  const out = {_: []};
  for (let i = 0; i < a.length; i++) {
    if (a[i].startsWith('--')) {
      const k = a[i].slice(2);
      const v = a[i + 1] && !a[i + 1].startsWith('--') ? a[++i] : true;
      out[k] = v;
    } else out._.push(a[i]);
  }
  return out;
})();

export async function prepare(project) {
  const root = path.resolve(import.meta.dirname, '..');
  if (!fs.existsSync(path.join(root, 'public/projects', project, 'video.json'))) {
    throw new Error(`No public/projects/${project}/video.json`);
  }
  const serveUrl = await bundle({entryPoint: path.join(root, 'src/index.ts'), publicDir: path.join(root, 'public')});
  const inputProps = {project};
  const composition = await selectComposition({serveUrl, id: 'Reel', inputProps, browserExecutable,
    chromiumOptions: {gl: 'swangle'}});
  return {root, serveUrl, inputProps, composition};
}
