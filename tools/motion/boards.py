import glob, os
from PIL import Image, ImageDraw
for tag, size, cols in (('light-m', (402, 874), 7), ('dark-m', (402, 874), 7), ('light-d', (1440, 900), 3)):
    fs = sorted(glob.glob(f'D:/tmp/oa/audit/{tag}-*.png'))
    sc = 0.5 if tag.endswith('d') else 0.75
    w, h = int(size[0] * sc), int(size[1] * sc)
    rows = (len(fs) + cols - 1) // cols
    o = Image.new('RGB', (cols * (w + 10), rows * (h + 34)), (230, 230, 230)); d = ImageDraw.Draw(o)
    for i, f in enumerate(fs):
        x = (i % cols) * (w + 10); y = (i // cols) * (h + 34)
        o.paste(Image.open(f).convert('RGB').resize((w, h)), (x, y + 28))
        d.text((x + 4, y + 8), os.path.basename(f).replace(tag + '-', '').replace('.png', ''), fill=(0, 0, 0))
    o.save(f'D:/tmp/oa/audit/board-{tag}.png'); print(tag, len(fs), o.size)
