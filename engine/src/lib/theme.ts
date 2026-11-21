import {continueRender, delayRender, staticFile} from 'remotion';
import type {Theme} from '../types';

export const DEFAULT_THEME: Theme = {
  gold: '#D4AF6A',        // measured from reference: ~#C9A46A after compression, slightly lifted
  goldLight: '#E8CC8E',
  cream: '#F2EDE4',       // label cards / input box (measured #EFEAE3)
  ink: '#111214',
  font: 'Heebo',
  serif: 'Cormorant Garamond',
};

const FONTS: [string, string, string][] = [
  ['Heebo', '400', 'heebo-hebrew-400-normal.woff2'],
  ['Heebo', '500', 'heebo-hebrew-500-normal.woff2'],
  ['Heebo', '700', 'heebo-hebrew-700-normal.woff2'],
  ['Heebo', '800', 'heebo-hebrew-800-normal.woff2'],
  ['Heebo', '900', 'heebo-hebrew-900-normal.woff2'],
  ['Heebo', '400', 'heebo-latin-400-normal.woff2'],
  ['Heebo', '700', 'heebo-latin-700-normal.woff2'],
  ['Heebo', '800', 'heebo-latin-800-normal.woff2'],
  ['Heebo', '900', 'heebo-latin-900-normal.woff2'],
  ['Cormorant Garamond', '500', 'cormorant-garamond-latin-500-normal.woff2'],
  ['Cormorant Garamond', '600', 'cormorant-garamond-latin-600-normal.woff2'],
];

let loaded = false;
export const loadFonts = () => {
  if (loaded || typeof document === 'undefined') return;
  loaded = true;
  const handle = delayRender('fonts');
  Promise.all(
    FONTS.map(([family, weight, file]) => {
      const f = new FontFace(family, `url(${staticFile('fonts/' + file)}) format('woff2')`, {weight});
      return f.load().then((ff) => (document as any).fonts.add(ff));
    }),
  )
    .then(() => continueRender(handle))
    .catch((e) => {
      console.error(e);
      continueRender(handle);
    });
};
