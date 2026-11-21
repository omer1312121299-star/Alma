// ============================================================================
//  Alma Reel spec — the single JSON file that fully describes a video.
//  Every time value is in SECONDS on the master timeline (= voice-over time).
//  Paths are relative to engine/public (e.g. "projects/gazi-demo/media/x.jpg").
// ============================================================================

export type Transition =
  | 'cut'        // hard cut
  | 'glitch'     // horizontal slice displacement + RGB split (the signature look)
  | 'zoom'       // punch-in: incoming scales 1.25 -> 1 with blur
  | 'whip'       // fast horizontal slide with motion blur
  | 'flash'      // white flash
  | 'fade'       // cross-dissolve
  | 'blur';      // blur dissolve

export type Camera = { t: number; x: number; y: number; zoom: number }; // t = seconds from scene start; x,y = 0..1 image coords of frame center

export interface Pin {
  name: string;
  sub?: string;          // e.g. "3 דק' הליכה"
  x: number; y: number;  // 0..1 image coords
  at: number;            // absolute seconds when it pops in
  activeFrom?: number;   // absolute seconds: highlighted gold
  activeTo?: number;
  icon?: 'pin' | 'metro' | 'none';
  latin?: boolean;       // serif latin label (e.g. "Gazi Boulevard")
  until?: number;        // absolute seconds when it disappears
  offset?: [number, number]; // px shift of the label card relative to the pin point (de-clutter)
}

export interface SceneBase {
  from: number; to: number;
  transition?: Transition;       // how this scene ENTERS
  transitionDur?: number;        // seconds, default 0.35
  grade?: 'none' | 'warm' | 'cool' | 'dark' | 'night';
  badge?: string;                // small top-right tag, e.g. "הדמיה"
}

export interface MediaScene extends SceneBase {
  type: 'media';
  src: string;                   // image or video (.mp4/.mov/.webm)
  move?: 'in' | 'out' | 'left' | 'right' | 'up' | 'down' | 'none'; // Ken Burns direction
  amount?: number;               // ken burns strength, default 0.12
  focus?: [number, number];      // 0..1 focal point for cover crop
  startFrom?: number;            // for video: seconds offset into clip
  blurBg?: boolean;              // fit inside with blurred fill (for landscape sources)
}

export interface MapScene extends SceneBase {
  type: 'map';
  src: string; width: number; height: number;   // image + its pixel size
  camera: Camera[];
  pins?: Pin[];
  route?: { from: string; to: string; at: number; dur?: number }[]; // animated dashed line between pins (by name)
  title?: { text: string; at: number; to?: number }; // big intro title (e.g. "טסתי לאתונה")
}

export interface PolaroidScene extends SceneBase {
  type: 'polaroid';
  src: string; bg?: string;      // photo in a white frame over blurred bg
  caption?: string;
  rotate?: number;
}

export interface SplitScene extends SceneBase {
  type: 'split';
  top: string; bottom: string;   // two images/videos stacked
}

export interface ColorScene extends SceneBase {
  type: 'color';
  color?: string; src?: string;  // solid or blurred-dark image background (for text-only beats)
}

export type Scene = MediaScene | MapScene | PolaroidScene | SplitScene | ColorScene;

// ---------------------------------------------------------------- overlays
export interface OverlayBase { from: number; to: number }

export interface StatRingOverlay extends OverlayBase {
  type: 'statRing';
  value: number; countFrom?: number; suffix?: string; decimals?: number;
  segments?: number; segmentLabels?: string[];
  headline?: string; footnote?: string;
  lines?: { text: string; at: number; color?: 'gold' | 'white'; size?: number }[];
  dim?: number;                  // darken background 0..1
}

export interface HeadlineOverlay extends OverlayBase {
  type: 'headline';
  lines: { text: string; at: number; size?: number; color?: 'gold' | 'white'; weight?: number }[];
  y?: number;                    // 0..1 vertical anchor (top of block)
  scrim?: boolean;
}

export interface StickerOverlay extends OverlayBase {
  type: 'sticker';
  text: string; sub?: string; chip?: string; chipAt?: number;
  x?: number; y?: number; rotate?: number; size?: number;
  style?: 'gold' | 'cream' | 'dark';
}

export interface StepsOverlay extends OverlayBase {
  type: 'steps';
  steps: string[];
  activeAt: number[];            // absolute seconds when each step becomes active
}

export interface SoldGridOverlay extends OverlayBase {
  type: 'soldGrid';
  cols: number; rows: number;
  sold: number[];                // indices that flip to sold
  soldLabel?: string;            // "נמכרה"
  startAt: number; stagger?: number;
}

export interface PriceOverlay extends OverlayBase {
  type: 'price';
  question?: string; value: number; prefix?: string; suffix?: string;
  valueAt: number; y?: number;
}

export interface CommentCtaOverlay extends OverlayBase {
  type: 'commentCta';
  title: string; titleAt?: number;
  sub?: string; subAt?: number;
  typed: string; typeAt: number; heartAt?: number;
}

export interface EndCardOverlay extends OverlayBase {
  type: 'endCard';
  logoTop?: string; title: string; subtitle?: string; credit?: string;
  disclaimer?: string; attribution?: string;
}

export interface TextOverlay extends OverlayBase {
  type: 'text';
  text: string; x?: number; y?: number; size?: number; color?: 'gold' | 'white' | 'cream';
  box?: boolean;
}

export type Overlay =
  | StatRingOverlay | HeadlineOverlay | StickerOverlay | StepsOverlay
  | SoldGridOverlay | PriceOverlay | CommentCtaOverlay | EndCardOverlay | TextOverlay;

// ---------------------------------------------------------------- captions
export interface CaptionWord { text: string; startMs: number; endMs: number }

export interface CaptionsConfig {
  src: string;                   // captions.json (from tools/transcribe.py)
  highlight?: string[];          // words painted gold (match ignores punctuation)
  fixes?: Record<string, string>;// ASR corrections: {"סוכרת": "שוכרת"}
  maxWords?: number;             // words per caption chunk (default 3)
  hide?: [number, number][];     // time ranges with no captions (graphics beats)
  y?: number;                    // 0..1 vertical center (default 0.80)
  stripPunctuation?: boolean;    // remove . , (keeps ! ?)  default true
}

export interface AudioConfig {
  voice?: string; voiceVolume?: number;
  music?: string; musicVolume?: number;   // auto-ducked under the voice
  sfx?: boolean;                          // whoosh on transitions, pop on stickers
  sfxVolume?: number;
}

export interface Theme {
  gold: string; goldLight: string; cream: string; ink: string;
  font: string; serif: string;
}

export interface ReelSpec {
  meta: { title: string; fps?: number; width?: number; height?: number; duration: number };
  theme?: Partial<Theme>;
  audio?: AudioConfig;
  captions?: CaptionsConfig;
  scenes: Scene[];
  overlays?: Overlay[];
  fx?: { grain?: number; vignette?: number };
}
