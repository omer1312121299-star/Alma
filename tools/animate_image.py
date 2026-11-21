#!/usr/bin/env python3
"""
Image -> short AI video clip (Wan 2.2 image-to-video, Hugging Face ZeroGPU space).
Usage: python3 -I tools/animate_image.py <image> <out.mp4> "<motion prompt>" [--seconds 3] [--steps 6] [--seed 42]
Prompt tips: describe CAMERA + subtle motion, e.g. "slow cinematic push-in, warm evening light, people walking, leaves moving".
The output is 16:9 or matches input aspect; use it as a `media` scene src (engine plays .mp4 natively).
"""
import argparse, shutil
from gradio_client import Client, handle_file
ap = argparse.ArgumentParser()
ap.add_argument("image"); ap.add_argument("out"); ap.add_argument("prompt")
ap.add_argument("--seconds", type=float, default=3.0); ap.add_argument("--steps", type=int, default=6)
ap.add_argument("--seed", type=int, default=42)
a = ap.parse_args()
# hf_token is a placeholder: in this environment the network proxy injects the real Hugging Face credential.
c = Client("https://zerogpu-aoti-wan2-2-fp8da-aoti-faster.hf.space/", verbose=False, token="hf_placeholder_injected_by_proxy")
res = c.predict(handle_file(a.image), a.prompt, a.steps,
                "blurry, distorted, warped faces, text, watermark, low quality, static",
                a.seconds, 1, 1, a.seed, False, api_name="/generate_video")
vid = res[0] if isinstance(res, (list, tuple)) else res
path = vid.get("video") if isinstance(vid, dict) else vid
shutil.copy(path, a.out); print("saved", a.out)
