#!/usr/bin/env python3
"""QA: tile images (or video frames) into one sheet.  contact_sheet.py out.jpg img1 img2 ...  |  --video v.mp4 --times 1,2,3"""
import sys, subprocess, tempfile, os
from PIL import Image, ImageDraw
args = sys.argv[1:]
out = args.pop(0)
files = []
if args and args[0] == "--video":
    v, times = args[1], [float(x) for x in args[3].split(",")]
    td = tempfile.mkdtemp()
    for t in times:
        f = os.path.join(td, f"{t:07.2f}.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", v, "-frames:v", "1", "-vf", "scale=360:-1", f], check=True)
        files.append((f, f"{t:.1f}s"))
else:
    files = [(f, os.path.basename(f).rsplit("_", 1)[-1].replace(".jpg", "s")) for f in args]
ims = [(Image.open(f).convert("RGB"), lab) for f, lab in files]
w = 360; ims = [(im.resize((w, int(im.height * w / im.width))), lab) for im, lab in ims]
h = ims[0][0].height; cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * w + (cols - 1) * 6, rows * h + (rows - 1) * 6), "white")
for i, (im, lab) in enumerate(ims):
    x, y = (i % cols) * (w + 6), (i // cols) * (h + 6)
    sheet.paste(im, (x, y)); d = ImageDraw.Draw(sheet); d.rectangle((x, y, x + 70, y + 26), fill="black"); d.text((x + 6, y + 6), lab, fill="white")
sheet.save(out, quality=88); print(out, sheet.size)
