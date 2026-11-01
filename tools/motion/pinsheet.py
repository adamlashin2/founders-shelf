"""Contact sheet of the candidates in a find_references result file. Usage: pinsheet.py <result.txt> <tag>"""
import json, re, sys
from PIL import Image, ImageDraw

t = open(sys.argv[1], encoding='utf-8').read()
tag = sys.argv[2]
items = re.findall(r'"candidateId":\s*"([^"]+)".*?"pieceLabel":\s*"([^"]+)".*?"query":\s*"([^"]+)".*?"path":\s*"([^"]+)"', t, re.S)
items = [(c, l, q, p.replace('\\\\', '\\')) for c, l, q, p in items]
json.dump(items, open(f'D:/tmp/oa/pin/{tag}.json', 'w'))
W, cells = 230, []
for k, (cid, lab, q, path) in enumerate(items):
    try:
        im = Image.open(path).convert('RGB')
    except Exception:
        continue
    h = min(int(im.height * W / im.width), 460)
    c = im.resize((W, int(im.height * W / im.width))).crop((0, 0, W, h))
    d = ImageDraw.Draw(c); d.rectangle((0, 0, 30, 20), fill=(230, 0, 0)); d.text((4, 4), str(k), fill=(255, 255, 255))
    cells.append(c)
cols = 8
for part in range(0, len(cells), 48):
    ch, rows = cells[part:part + 48], []
    for i in range(0, len(ch), cols):
        g = ch[i:i + cols]; H = max(c.height for c in g)
        r = Image.new('RGB', (cols * (W + 5), H), (60, 60, 60))
        for j, c in enumerate(g): r.paste(c, (j * (W + 5), 0))
        rows.append(r)
    sh = Image.new('RGB', (rows[0].width, sum(r.height + 5 for r in rows)), (60, 60, 60)); y = 0
    for r in rows: sh.paste(r, (0, y)); y += r.height + 5
    sh.thumbnail((1900, 2600)); sh.save(f'D:/tmp/oa/pin/{tag}-s{part // 48}.jpg', quality=80)
print(len(items), 'candidates')
from collections import Counter
print(Counter(q for _, _, q, _ in items))
