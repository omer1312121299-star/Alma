#!/usr/bin/env python3
"""
Real satellite imagery for map scenes — free, no API key.
Source: Sentinel-2 L2A true-color (10 m/pixel) from the public AWS bucket `sentinel-cogs`
(Copernicus data, attribution: "Contains modified Copernicus Sentinel data <year>").

Usage:
  python3 -I tools/satellite_map.py --lat 37.978 --lon 23.712 --width-km 9 --height-km 16 \
      --out engine/public/projects/X/media/map.jpg \
      --place "גזי בולווארד=37.9779,23.7112" --place "אקרופוליס=37.9715,23.7257" \
      [--year 2025 --months 6,7,8] [--scale 2]

Writes:
  map.jpg        — north-up satellite crop (graded, upscaled x--scale with Lanczos + unsharp)
  map.json       — {"width","height","places":[{"name","x","y"}]}, x/y normalized 0..1 inside the image,
                   ready to paste into a `map` scene's `pins`.

Needs: pip install rasterio pillow numpy
"""
import argparse, json, math, os, re, sys, urllib.request
import numpy as np

BUCKET = "https://sentinel-cogs.s3.us-west-2.amazonaws.com"
os.environ.setdefault("CURL_CA_BUNDLE", "/root/.ccr/ca-bundle.crt") if os.path.exists("/root/.ccr/ca-bundle.crt") else None
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif")


def utm(lat, lon, zone=None):
    zone = zone or int((lon + 180) / 6) + 1
    a = 6378137.0; f = 1 / 298.257223563; e2 = f * (2 - f); k0 = 0.9996
    lon0 = math.radians((zone - 1) * 6 - 180 + 3); phi = math.radians(lat); lam = math.radians(lon)
    N = a / math.sqrt(1 - e2 * math.sin(phi) ** 2); T = math.tan(phi) ** 2; ep2 = e2 / (1 - e2)
    C = ep2 * math.cos(phi) ** 2; A = math.cos(phi) * (lam - lon0)
    M = a * ((1 - e2 / 4 - 3 * e2 ** 2 / 64 - 5 * e2 ** 3 / 256) * phi
             - (3 * e2 / 8 + 3 * e2 ** 2 / 32 + 45 * e2 ** 3 / 1024) * math.sin(2 * phi)
             + (15 * e2 ** 2 / 256 + 45 * e2 ** 3 / 1024) * math.sin(4 * phi)
             - (35 * e2 ** 3 / 3072) * math.sin(6 * phi))
    E = k0 * N * (A + (1 - T + C) * A ** 3 / 6 + (5 - 18 * T + T * T + 72 * C - 58 * ep2) * A ** 5 / 120) + 500000
    Nn = k0 * (M + N * math.tan(phi) * (A * A / 2 + (5 - T + 9 * C + 4 * C * C) * A ** 4 / 24
                                        + (61 - 58 * T + T * T + 600 * C - 330 * ep2) * A ** 6 / 720))
    if lat < 0:
        Nn += 10000000
    return zone, E, Nn


def mgrs_tile(lat, lon):
    zone, E, N = utm(lat, lon)
    band = "CDEFGHJKLMNPQRSTUVWX"[int((lat + 80) / 8)]
    col = ["ABCDEFGH", "JKLMNPQR", "STUVWXYZ"][(zone - 1) % 3][int(E / 100000) - 1]
    row = "ABCDEFGHJKLMNPQRSTUV"[(int(N / 100000) + (5 if zone % 2 == 0 else 0)) % 20]
    return zone, band, col + row


def http_json(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode()


def find_scene(zone, band, sq, year, months):
    best = None
    for m in months:
        prefix = f"sentinel-s2-l2a-cogs/{zone}/{band}/{sq}/{year}/{m}/"
        xml = http_json(f"{BUCKET}/?list-type=2&delimiter=/&prefix={prefix}")
        for p in re.findall(r"<Prefix>([^<]+/)</Prefix>", xml):
            if p == prefix:
                continue
            name = p.rstrip("/").split("/")[-1]
            try:
                props = json.loads(http_json(f"{BUCKET}/{p}{name}.json"))["properties"]
            except Exception:
                continue
            cc, nd = props.get("eo:cloud_cover", 100), props.get("s2:nodata_pixel_percentage", 100)
            score = cc + nd
            if best is None or score < best[0]:
                best = (score, f"{BUCKET}/{p}TCI.tif", name, cc, nd)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lat", type=float, required=True); ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--width-km", type=float, default=9); ap.add_argument("--height-km", type=float, default=16)
    ap.add_argument("--out", required=True)
    ap.add_argument("--place", action="append", default=[], help='"name=lat,lon"')
    ap.add_argument("--year", type=int, default=2025); ap.add_argument("--months", default="6,7,8")
    ap.add_argument("--scale", type=float, default=2.0, help="upscale factor for output")
    ap.add_argument("--tci", default=None, help="explicit TCI.tif URL (skip search)")
    a = ap.parse_args()

    import rasterio
    from rasterio.windows import from_bounds
    from PIL import Image, ImageFilter, ImageEnhance

    zone, band, sq = mgrs_tile(a.lat, a.lon)
    if a.tci:
        url = a.tci; print("using", url, file=sys.stderr)
    else:
        best = find_scene(zone, band, sq, a.year, [int(x) for x in a.months.split(",")])
        if not best:
            sys.exit("no scene found")
        _, url, name, cc, nd = best
        print(f"scene {name} cloud={cc:.2f}% nodata={nd:.1f}%", file=sys.stderr)

    _, cx, cy = utm(a.lat, a.lon, zone)
    hw, hh = a.width_km * 500, a.height_km * 500
    with rasterio.open("/vsicurl/" + url) as ds:
        win = from_bounds(cx - hw, cy - hh, cx + hw, cy + hh, ds.transform)
        arr = ds.read(window=win, boundless=True, fill_value=0)  # (3,H,W) uint8
    img = Image.fromarray(np.transpose(arr, (1, 2, 0)))
    W, H = img.size
    if a.scale != 1:
        img = img.resize((int(W * a.scale), int(H * a.scale)), Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=90, threshold=2))
    img = ImageEnhance.Contrast(img).enhance(1.12)
    img = ImageEnhance.Color(img).enhance(1.08)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    img.save(a.out, quality=90)

    places = []
    for p in a.place:
        name, ll = p.split("=", 1)
        plat, plon = map(float, ll.split(","))
        _, px, py = utm(plat, plon, zone)
        places.append({"name": name, "x": round((px - (cx - hw)) / (2 * hw), 4),
                       "y": round(((cy + hh) - py) / (2 * hh), 4)})
    meta = {"width": img.size[0], "height": img.size[1], "source": url,
            "attribution": f"Contains modified Copernicus Sentinel data {a.year}", "places": places}
    json.dump(meta, open(os.path.splitext(a.out)[0] + ".json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
