#!/usr/bin/env python3
"""
Hebrew voice-over -> word-level captions for the Alma video engine.

Usage:
  HF_HUB_DISABLE_XET=1 python3 -I tools/transcribe.py <audio-or-video> <out captions.json> [--model MODEL]

Output (Remotion "Caption" format, one entry per word):
  [{"text": "טסתי", "startMs": 0, "endMs": 420, "timestampMs": 210, "confidence": 0.98}, ...]

Default model: ivrit-ai/whisper-large-v3-turbo-ct2 (Hebrew fine-tuned Whisper, best open Hebrew ASR).
Runs on CPU (~25s for a 70s clip on 4 cores). Needs: pip install faster-whisper
"""
import argparse, json, os, subprocess, sys, tempfile, wave
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--model", default="ivrit-ai/whisper-large-v3-turbo-ct2")
ap.add_argument("--prompt", default=None, help="initial prompt: names/terms to spell right, e.g. 'גזי בולווארד, טכנופוליס, מונסטיראקי'")
a = ap.parse_args()

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
from faster_whisper import WhisperModel

with tempfile.TemporaryDirectory() as td:
    wav = os.path.join(td, "a.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-ac", "1", "-ar", "16000", wav], check=True)
    wf = wave.open(wav)
    audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768

m = WhisperModel(a.model, device="cpu", compute_type="int8")
segs, _ = m.transcribe(audio, language="he", word_timestamps=True, beam_size=5,
                       initial_prompt=a.prompt, vad_filter=False)
words = []
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}", file=sys.stderr)
    for w in s.words:
        t = w.word.strip()
        if not t:
            continue
        words.append({"text": t, "startMs": round(w.start * 1000), "endMs": round(w.end * 1000),
                      "timestampMs": round((w.start + w.end) * 500), "confidence": round(w.probability, 3)})
# merge split tokens: "8"+"%" -> "8%", "150"+",000" -> "150,000", "מ"+"-20" -> "מ-20"
merged = []
for w in words:
    if merged and w["text"][0] in "%,-" and len(w["text"]) > 0:
        p = merged[-1]
        p["text"] += w["text"]; p["endMs"] = w["endMs"]; p["timestampMs"] = (p["startMs"] + p["endMs"]) // 2
    else:
        merged.append(w)
words = merged
json.dump(words, open(a.out, "w"), ensure_ascii=False, indent=1)
print(f"wrote {len(words)} words -> {a.out}", file=sys.stderr)
