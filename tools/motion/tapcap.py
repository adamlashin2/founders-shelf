"""Frame-capture one interaction. Usage: tapcap.py <tag> <route> <scrollY> <selector> [scheme]"""
import asyncio, base64, io, sys
from PIL import Image, ImageDraw
from playwright.async_api import async_playwright
tag, route, sy, sel = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
scheme = sys.argv[5] if len(sys.argv) > 5 else 'light'


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:/Users/adaml/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe',
                                    args=['--enable-gpu-rasterization', '--ignore-gpu-blocklist'])
        ctx = await b.new_context(viewport={'width': 393, 'height': 852}, color_scheme=scheme, has_touch=True)
        pg = await ctx.new_page()
        await pg.goto(f'http://localhost:8123/?v={tag}#/{route}'); await pg.wait_for_timeout(2200)
        await pg.evaluate(f"[...document.querySelectorAll('#view .page')].pop().scrollTo(0,{sy})"); await pg.wait_for_timeout(700)
        cdp = await ctx.new_cdp_session(pg); frames = []

        def on(f):
            frames.append((f['metadata']['timestamp'], f['data'])); asyncio.ensure_future(cdp.send('Page.screencastFrameAck', {'sessionId': f['sessionId']}))
        cdp.on('Page.screencastFrame', on)
        await cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 60, 'maxWidth': 200, 'maxHeight': 434})
        await pg.evaluate("window.__t=setInterval(()=>document.documentElement.style.setProperty('--tk',Math.random()),16)")
        await pg.wait_for_timeout(200)
        await pg.tap(sel); await pg.wait_for_timeout(1200)
        await cdp.send('Page.stopScreencast'); await b.close()
    t0 = frames[0][0]; pick = []; last = -1
    for t, d in frames:
        ms = int((t - t0) * 1000)
        if ms // 45 != last: pick.append((ms, d)); last = ms // 45
    pick = pick[:26]
    ims = [Image.open(io.BytesIO(base64.b64decode(d))) for _, d in pick]
    w, h = ims[0].size
    o = Image.new('RGB', (13 * (w + 3), 2 * (h + 14)), (255, 0, 255)); dr = ImageDraw.Draw(o)
    for i, (im, (ms, _)) in enumerate(zip(ims, pick)):
        x = (i % 13) * (w + 3); y = (i // 13) * (h + 14); o.paste(im, (x, y + 13)); dr.text((x + 2, y), f'{ms}ms', fill=(0, 0, 0))
    o.save(f'D:/tmp/oa/shots/tap-{tag}.jpg', quality=80); print(len(frames), 'frames')


asyncio.run(main())
