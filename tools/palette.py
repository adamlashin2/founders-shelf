#!/usr/bin/env python3
"""One tonal ground per figure (DESIGN.md, "Art-tinted editorial").

The grounds are not picked by eye: they are the median border colours of the
Pinterest references that define the direction (brief 26bfecc6), as hue +
saturation. The app renders each at its own lightness ramp, so only hue and
saturation are stored. Each shelf owns a subset; figures inside a shelf take
turns through it so neighbours never share a ground.
Writes app/data/palette.json: { name: [hue, sat] }.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repo root (scripts live in tools/)
G = {  # pin -> measured border median
    "ember":   (16, .47),   # 60  #753e2a
    "umber":   (19, .29),   # 65  #412d24
    "bronze":  (33, .50),   # 71  #422e16
    "amber":   (31, .70),   # 61  #ab5d0a (sat capped for dark grounds)
    "sage":    (147, .14),  # 26  #48534d (sat doubled to survive darkening)
    "moss":    (99, .40),   # 33  #36631e
    "graphite":(220, .06),  # 21  #555555
    "crimson": (1, .55),    # 22  #d53a38
    "azure":   (207, .45),  # 62  #4e94cf
    "sand":    (29, .20),   # 74  #8b7663
}
SHELF = {"business": ["ember", "azure", "bronze", "sage", "crimson", "sand"],
         "military": ["crimson", "umber", "graphite", "bronze"],
         "science":  ["azure", "sage", "graphite", "moss"],
         "money":    ["bronze", "amber", "moss", "umber"],
         "systems":  ["graphite", "sage", "azure", "ember"]}

src = (ROOT / "app/index.html").read_text(encoding="utf8")
cats = dict(re.findall(r'"([^"]+)":\{cat:"(\w+)"', src))
order = json.loads((ROOT / "app/data/episodes.json").read_text(encoding="utf8"))["people"]
seen, out = {}, {}
for p in order:
    c = cats.get(p["name"], "business"); n = seen.get(c, 0); seen[c] = n + 1
    g = SHELF[c][n % len(SHELF[c])]; out[p["name"]] = list(G[g]) + [g]
    print(f'{p["name"]:32s} {c:9s} {g}')
(ROOT / "app/data/palette.json").write_text(json.dumps(out, indent=1), encoding="utf8")
