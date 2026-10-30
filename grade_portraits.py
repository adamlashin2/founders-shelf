#!/usr/bin/env python3
"""Give every figure the same photograph: 3:4, monochrome, low-key.

Originals live in sources/portraits/ (seeded from app/assets/people the first
time, then replaced by hand-picked Pinterest finds via portrait_picks.json).
Graded copies are written over app/assets/people/, the files the app loads.

The grade is the one the kept Pinterest references share (rim-lit portraits on
black): luminance only, 1% autocontrast, an S-curve that crushes the bottom
end, and a radial falloff so every face sits in its own pool of light.
"""
import json, math, shutil, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).parent
SRC = ROOT / "sources" / "portraits"
OUT = ROOT / "app" / "assets" / "people"
PICKS = ROOT / "portrait_picks.json"
W, H = 900, 1200                     # 3:4, enough for a 300pt card at @3x


def curve(x):                         # S-curve on 0..1, crushed toe
    x = max(0.0, (x - 0.04) / 0.96)
    s = x * x * (3 - 2 * x)
    return 0.55 * s + 0.45 * x


LUT = [round(255 * curve(i / 255)) for i in range(256)]


def grade(src, dst, top=0.06):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w / h > W / H:                                 # too wide: centre crop
        nw = round(h * W / H); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:                                             # too tall: keep the head
        nh = round(w * H / W); y = min(h - nh, round(h * top)); im = im.crop((0, y, w, y + nh))
    im = im.resize((W, H), Image.LANCZOS)
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1).point(LUT)
    # radial falloff centred on the upper third, where the face is
    mask = Image.new("L", (W, H))
    px = mask.load()
    cx, cy, R = W / 2, H * 0.38, math.hypot(W / 2, H * 0.62)
    for y in range(H):
        for x in range(0, W):
            d = math.hypot(x - cx, (y - cy) * 0.85) / R
            px[x, y] = round(255 * (1 - 0.55 * min(1, max(0, d - 0.25) / 0.75) ** 1.6))
    g = Image.composite(g, Image.new("L", (W, H), 0), mask)
    g.convert("RGB").save(dst, quality=86, optimize=True, progressive=True)


def main():
    SRC.mkdir(parents=True, exist_ok=True)
    portraits = json.loads((ROOT / "app" / "portraits.json").read_text(encoding="utf8"))
    picks = json.loads(PICKS.read_text(encoding="utf8")) if PICKS.exists() else {}
    for name, rel in portraits.items():
        fname = Path(rel).name
        src = SRC / fname
        if name in picks and Path(picks[name]["file"]).exists():
            shutil.copyfile(picks[name]["file"], src)
        elif not src.exists():
            shutil.copyfile(OUT / fname, src)            # first run: keep the original
        grade(src, OUT / fname, picks.get(name, {}).get("top", 0.06))
        print("graded", name)


if __name__ == "__main__":
    main()
