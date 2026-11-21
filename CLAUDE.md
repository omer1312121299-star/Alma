# Alma — AI video studio (Hebrew real-estate reels, 9:16)

The user (Alma Group, Hebrew speaker) makes short vertical reels in the style of
`reference/gazi-boulevard-original.mov`: first-person Hebrew voice-over, word-by-word gold/white
captions, satellite maps with walking-distance pins, AI renders tagged "הדמיה", a yield ring,
stickers, "sold" grid, price reveal, and a "write X in the comments" CTA.
Reply to the user in Hebrew. Read these first:
- `docs/01-reverse-engineering.md` — the shot list, script formula, and design system of the reference
- `docs/02-production-workflow.md` — the production pipeline and the "change request → which field" table

## Layout
```
engine/                      Remotion 4 project (React → MP4). Code = reusable components only.
  src/types.ts               ★ THE SPEC SCHEMA. Every field of video.json is documented here.
  src/Reel.tsx               master composition: scenes → overlays → captions → fx → audio
  src/scenes/                media (Ken Burns, video), map (camera keyframes + pins + routes), polaroid, split, color
  src/overlays/OverlayView.tsx  statRing, headline, sticker, steps, soldGrid, price, commentCta, endCard, text
  src/components/Captions.tsx   word-synced chunks, gold highlight, hide ranges, ASR fixes
  public/projects/<name>/    ONE FOLDER PER VIDEO: video.json, captions.json, media/, audio/
  public/fonts, fx, sfx      Heebo + Cormorant, grain tiles, synthesized whoosh/pop/tick
  scripts/render.mjs         full or partial render       scripts/still.mjs  QA frames
tools/
  transcribe.py              Hebrew ASR → word timestamps (ivrit-ai whisper-large-v3-turbo-ct2)
  satellite_map.py           real Sentinel-2 satellite crop for any lat/lon + pin coordinates
  animate_image.py           image → AI video clip (Wan 2.2 HF space; needs ZeroGPU quota)
  contact_sheet.py           tile stills / video frames into one QA image
  make_sfx.sh                regenerate SFX
reference/                   the original reel being emulated
```

## Setup in a fresh container
```bash
cd engine && npm install                       # remotion 4.0.539, react 19
pip install faster-whisper rasterio gradio_client
export HF_HUB_DISABLE_XET=1                    # Xet CDN is blocked; plain HF download works
```
Rendering uses the preinstalled Chromium headless shell (auto-detected in `scripts/common.mjs`; never run
`remotion browser ensure`). The demo media is in git; `out/` and `node_modules/` are not.

## Core commands
```bash
python3 -I tools/transcribe.py <audio> engine/public/projects/<p>/captions.json --prompt "place names"
python3 -I tools/satellite_map.py --lat .. --lon .. --width-km 4.6 --height-km 8.2 --scale 2.4 \
    --out engine/public/projects/<p>/media/map-close.jpg --place "name=lat,lon" ...
cd engine && node scripts/still.mjs <p> 3 9.5 22 40      # renders out/stills/<p>_<sec>.jpg at 0.5 scale
python3 -I ../tools/contact_sheet.py out/sheet.jpg out/stills/<p>_*.jpg    # then Read the sheet
node scripts/render.mjs <p> [--from 30 --to 40] [--out out/x.mp4]          # ~full render 1080x1920
npx tsc --noEmit                                          # after any code change
```

## How to handle a change request
1. Find the beat in `captions.json` (word times) → the scene/overlay whose `from/to` covers it.
2. Edit `video.json` only (schema in `src/types.ts`). Keep scenes contiguous: scene[i].to == scene[i+1].from.
   Cut ON a word start. Pins/overlays use absolute seconds; map `camera[].t` is seconds from scene start.
3. Render stills at the changed seconds, build a contact sheet, LOOK at it, fix, then render the video.
4. New graphic type? Add the interface to `types.ts`, the component to `OverlayView.tsx`, typecheck.
5. Report what changed + send the MP4 (SendUserFile). Commit project + code changes to the dev branch.

## Style rules (from the reference — keep them)
- Gold `#D4AF6A`, cream `#F2EDE4`, ink `#111214`; Heebo 800–900 for Hebrew, Cormorant for Latin names.
- Captions ≤2–3 words, bottom ~79%, gold for keywords/numbers, hidden while big graphics are on screen.
- A shot every ~2s; long shots must move (map camera / pins / text). Every spoken number appears on screen.
- "הדמיה" badge on every rendering/AI visual. End card always has the legal disclaimer
  (renders illustrative, yield before tax, not an offer). Don't invent financial figures — ask.
- Credit sources: Unsplash photos, "Copernicus Sentinel-2" for maps, CC-BY music in the end card.

## Known environment limits (cloud container)
- Reachable: npm, PyPI, huggingface.co (credential injected), the Wan2.2 HF space, Unsplash (MCP), AWS S3
  (`sentinel-cogs` bucket). NOT reachable: Google/ESRI/OSM tiles, Overpass, ElevenLabs, Microsoft TTS.
- TTS: no Hebrew TTS host is reachable by default. Ask the user to record (best) or to provide an
  ElevenLabs key via `request_credential` (host api.elevenlabs.io).
- faster-whisper + this PyAV: pass audio as a numpy array (transcribe.py already does).
- ZeroGPU quota for Wan2.2 may be exhausted ("exceeded your ZeroGPU runs limit") — tell the user; fall
  back to Ken Burns on stills.
- Remotion license: free for individuals / companies ≤3 employees; larger companies need a Remotion
  company license (remotion.pro).
