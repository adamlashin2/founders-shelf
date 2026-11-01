"""Flash detector: walk the app like a listener, record every frame, find flashes.

A flash = a frame that departs sharply from the frames on both sides of it while those
neighbours resemble each other (A->B->A), or a large region that drops to near-blank
and comes back. Each flash is attributed to the action that preceded it.
Usage: python flashwalk.py <tag> [dark|light] [390|1440]
"""
import asyncio, base64, io, json, sys
import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

TAG = sys.argv[1] if len(sys.argv) > 1 else 'walk'
SCHEME = sys.argv[2] if len(sys.argv) > 2 else 'dark'
W = int(sys.argv[3]) if len(sys.argv) > 3 else 390
H = 844 if W < 900 else 900
GPU = ['--ignore-gpu-blocklist', '--enable-gpu-rasterization', '--use-angle=d3d11', '--autoplay-policy=no-user-gesture-required']

STEPS = [
    ('tab -> Greats', "document.querySelector(innerWidth<900?'.tab[data-t=figures]':'#topnav [data-t=figures]').click()"),
    ('tab -> Library', "document.querySelector(innerWidth<900?'.tab[data-t=library]':'#topnav [data-t=library]').click()"),
    ('tab -> Home', "document.querySelector(innerWidth<900?'.tab[data-t=home]':'#topnav [data-t=home]').click()"),
    ('tab -> Greats again', "document.querySelector(innerWidth<900?'.tab[data-t=figures]':'#topnav [data-t=figures]').click()"),
    ('filter War', "document.querySelectorAll('[data-fil]')[2].click()"),
    ('filter All', "document.querySelectorAll('[data-fil]')[0].click()"),
    ('card -> figure', "document.querySelectorAll('.pcard')[1].click()"),
    ('scroll figure', "[...document.querySelectorAll('#view .page')].pop().scrollBy({top:500,behavior:'smooth'})"),
    ('back', "history.back()"),
    ('tab -> Library', "document.querySelector(innerWidth<900?'.tab[data-t=library]':'#topnav [data-t=library]').click()"),
    ('row -> History', "document.querySelector('.er').click()"),
    ('back', "history.back()"),
    ('play book', "playEp(BYSLUG['napoleon'],0,'bio'); document.querySelector('audio').pause()"),
    ('open player', "document.querySelector('#mini .mini-main').click()"),
    ('close player', "document.getElementById('npclose').click()"),
    ('tab -> Home', "document.querySelector(innerWidth<900?'.tab[data-t=home]':'#topnav [data-t=home]').click()"),
    ('scroll home', "[...document.querySelectorAll('#view .page')].pop().scrollBy({top:700,behavior:'smooth'})"),
    ('star a great', "(document.querySelector('.fcfav')||{click(){}}).click()"),
]


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:/Users/adaml/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe', args=GPU)
        ctx = await b.new_context(viewport={'width': W, 'height': H}, color_scheme=SCHEME)
        pg = await ctx.new_page()
        await pg.goto('http://localhost:8123/?v=' + TAG + '#/home')
        await pg.wait_for_timeout(2500)
        cdp = await ctx.new_cdp_session(pg)
        frames = []

        def on_frame(f):
            frames.append((f['metadata']['timestamp'], f['data']))
            asyncio.ensure_future(cdp.send('Page.screencastFrameAck', {'sessionId': f['sessionId']}))
        cdp.on('Page.screencastFrame', on_frame)
        await cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 50, 'maxWidth': 260, 'maxHeight': 560, 'everyNthFrame': 1})
        await pg.wait_for_timeout(400)
        marks = []
        for name, js in STEPS:
            marks.append((name, len(frames)))
            # keep the compositor producing frames so the screencast has dense coverage
            await pg.evaluate("window.__tick=window.__tick||setInterval(()=>{document.documentElement.style.setProperty('--tick',Math.random())},16)")
            await pg.evaluate(js)
            await pg.wait_for_timeout(1300)
        await cdp.send('Page.stopScreencast')
        await b.close()

    import pickle; pickle.dump({'frames':frames,'marks':marks}, open(f'D:/tmp/oa/shots/frames-{TAG}-{SCHEME}-{W}.pkl','wb'))
    imgs = [np.asarray(Image.open(io.BytesIO(base64.b64decode(d))).convert('L').resize((130, 280)), dtype=float) for _, d in frames]
    flashes = []
    for i in range(1, len(imgs) - 1):
        a, b_, c = imgs[i - 1], imgs[i], imgs[i + 1]
        d_ab = np.abs(b_ - a); d_ac = np.abs(c - a).mean(); d_bc = np.abs(c - b_)
        # regions that changed in b and changed BACK in c (A->B->A), large enough to see
        spike = ((d_ab > 40) & (d_bc > 40)).mean()
        dark = (a.mean() - b_.mean() > 12 and c.mean() - b_.mean() > 12)   # whole-screen dip
        if (spike > 0.06 and d_ac < 18) or dark:
            step = max([m for m in marks if m[1] <= i], key=lambda m: m[1], default=('start', 0))[0]
            flashes.append((step, i, round(spike, 3), round(a.mean() - b_.mean(), 1)))
    by = {}
    for f in flashes:
        by.setdefault(f[0], 0); by[f[0]] += 1
    print(f'{TAG} {SCHEME} {W}px: {len(frames)} frames, {len(flashes)} flash frames')
    for step, _ in marks:
        if step in by:
            print(f'   {by[step]:2d}  after "{step}"')
    json.dump({'frames': len(frames), 'flashes': flashes, 'marks': marks}, open(f'D:/tmp/oa/shots/flash-{TAG}-{SCHEME}-{W}.json', 'w'))
    # keep flash frames for inspection
    for k, (step, i, s, dm) in enumerate(flashes[:12]):
        trip = [Image.open(io.BytesIO(base64.b64decode(frames[j][1]))) for j in (i - 1, i, i + 1)]
        row = Image.new('RGB', (sum(t.width for t in trip) + 10, trip[0].height), (255, 0, 255))
        x = 0
        for t in trip:
            row.paste(t, (x, 0)); x += t.width + 5
        row.save(f'D:/tmp/oa/shots/flash-{TAG}-{k:02d}.jpg', quality=80)


asyncio.run(main())
