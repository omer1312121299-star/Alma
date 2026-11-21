#!/usr/bin/env bash
# Synthesizes the engine's royalty-free SFX into engine/public/sfx (no downloads needed).
set -e
OUT="${1:-engine/public/sfx}"; mkdir -p "$OUT"
# whoosh: pink noise, band-pass sweeping up, fast attack / slow release
ffmpeg -v error -y -f lavfi -i "anoisesrc=color=pink:duration=0.7:amplitude=0.9" \
  -af "highpass=f=300,lowpass=f=5000,afade=t=in:st=0:d=0.28:curve=exp,afade=t=out:st=0.3:d=0.4:curve=exp,aecho=0.6:0.5:40:0.3,volume=1.4" \
  -ar 44100 -ac 2 "$OUT/whoosh.wav"
# pop: short sine with pitch drop + click
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.9*sin(2*PI*(900-700*t/0.12)*t)*exp(-t*28)':d=0.25:s=44100" \
  -af "volume=1.2" -ac 2 "$OUT/pop.wav"
# tick: tiny UI tick (for typing / counters)
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.7*sin(2*PI*2200*t)*exp(-t*90)':d=0.06:s=44100" -ac 2 "$OUT/tick.wav"
echo "sfx -> $OUT"; ls -la "$OUT"
