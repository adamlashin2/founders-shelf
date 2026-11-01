"""Blankness analysis of a recorded walk: per step, how much of the screen goes empty
(flat tiles) mid-transition beyond the start/end levels. Usage: python blankness.py <pkl>"""
import base64, io, pickle, sys
import numpy as np
from PIL import Image
d = pickle.load(open(sys.argv[1], 'rb'))
fr, marks = d['frames'], d['marks']
def blank(img):
    a = np.asarray(img.convert('L').resize((130, 280)), dtype=float)
    t = a[:280 // 10 * 10, :130 // 10 * 10].reshape(28, 10, 13, 10).std(axis=(1, 3))
    return (t < 2.5).mean(), a.mean()
B = [blank(Image.open(io.BytesIO(base64.b64decode(x)))) for _, x in fr]
ts = [t for t, _ in fr]
marks = marks + [('end', len(fr))]
for (name, i0), (_, i1) in zip(marks, marks[1:]):
    if i1 - i0 < 3: print(f'{name:22s} (few frames: {i1-i0})'); continue
    seg = B[max(i0 - 1, 0):i1]
    s, e = seg[0][0], seg[-1][0]
    peak = max(b for b, _ in seg); k = [b for b, _ in seg].index(peak)
    lum = [l for _, l in seg]; dip = min(seg[0][1], seg[-1][1]) - min(lum)
    excess = peak - max(s, e)
    dur = ts[min(i0 + k, len(ts)-1)] - ts[i0]
    flag = 'FLASH' if excess > 0.06 or dip > 8 else ''
    print(f'{name:22s} frames {i1-i0:3d}  blank start {s:.2f} end {e:.2f} peak {peak:.2f} (+{excess:.2f} @ {dur*1000:.0f}ms)  lum dip {dip:4.1f}  {flag}')
