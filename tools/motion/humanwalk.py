"""Use the app like a person on a phone: touch, scroll, play, quit, relaunch. Records video + numbers.
Usage: python humanwalk.py <tag> [light|dark]"""
import asyncio, sys, json
from playwright.async_api import async_playwright
TAG = sys.argv[1]; SCHEME = sys.argv[2] if len(sys.argv) > 2 else 'light'
URL = 'http://localhost:8123/?v=' + TAG
EXE = r'C:/Users/adaml/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe'
log = []


def note(*a):
    s = ' '.join(str(x) for x in a); log.append(s); print(s)


async def swipe(pg, x, y0, y1, steps=14):
    await pg.mouse.move(x, y0); await pg.mouse.down()
    for k in range(1, steps + 1):
        await pg.mouse.move(x, y0 + (y1 - y0) * k / steps); await pg.wait_for_timeout(16)
    await pg.mouse.up()


async def scroll(pg, dy, times=6):
    for _ in range(times):
        await pg.mouse.wheel(0, dy / times); await pg.wait_for_timeout(60)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=EXE, args=['--autoplay-policy=no-user-gesture-required'])
        ctx = await b.new_context(viewport={'width': 393, 'height': 852}, device_scale_factor=2, has_touch=True, is_mobile=False,
                                  color_scheme=SCHEME, record_video_dir=f'D:/tmp/oa/walk/{TAG}', record_video_size={'width': 393, 'height': 852})
        pg = await ctx.new_page(); errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto(URL + '#/home'); await pg.wait_for_timeout(2500)
        await pg.mouse.move(200, 500)
        note('1 home: scroll down and back'); await scroll(pg, 1600, 10); await pg.wait_for_timeout(700); await scroll(pg, -1600, 10); await pg.wait_for_timeout(600)
        note('2 tap first post image')
        el = await pg.query_selector('.invc')
        if el: await el.tap(); await pg.wait_for_timeout(1200)
        note('   route', await pg.evaluate('location.hash'))
        await scroll(pg, 900, 8); await pg.wait_for_timeout(600)
        note('3 tap Play on figure page')
        await pg.tap('.fx .seg [data-a=play]'); await pg.wait_for_timeout(1800)
        await pg.evaluate("document.querySelector('audio').currentTime=125"); await pg.wait_for_timeout(5200)
        t1 = await pg.evaluate("document.querySelector('audio').currentTime")
        note('   playing at', round(t1, 1))
        note('4 close player, go back home')
        await pg.tap('#npclose'); await pg.wait_for_timeout(900)
        await pg.evaluate('history.back()'); await pg.wait_for_timeout(1200)
        note('5 tap a cloud avatar')
        el = await pg.query_selector('.hxav')
        if el: await el.tap(); await pg.wait_for_timeout(1300)
        note('   route', await pg.evaluate('location.hash'))
        await pg.evaluate('history.back()'); await pg.wait_for_timeout(1100)
        t2 = await pg.evaluate("document.querySelector('audio').currentTime")
        note('6 "quit" the app while playing at', round(t2, 1))
        await pg.close(); pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))   # quit + relaunch: a new page, same storage
        await pg.goto(URL + '#/home'); await pg.wait_for_timeout(2500)
        st = await pg.evaluate("""({src:audio.src, ct:audio.currentTime, saved:cur?store.get('pos.'+epKey(cur.p,curEp()),0):null,
          mini:document.getElementById('minit')?.textContent})""")
        note('7 relaunched:', json.dumps(st))
        await pg.tap('#mini .mini-main'); await pg.wait_for_timeout(1500)
        npel = await pg.evaluate("document.getElementById('tel')?.textContent")
        note('   Now Playing shows', npel)
        await pg.tap('#npplay'); await pg.wait_for_timeout(1500)
        t3 = await pg.evaluate("document.querySelector('audio').currentTime")
        note('8 after pressing play it is at', round(t3, 1), '(should be ~', round(t2, 1), ')')
        await pg.tap('#npclose'); await pg.wait_for_timeout(800)
        note('9 Greats tab, filter, card, edge swipe back')
        await pg.tap('.tab[data-t=figures]'); await pg.wait_for_timeout(1000)
        await pg.tap('[data-fil]:nth-child(3)'); await pg.wait_for_timeout(900)
        el = await pg.query_selector('.pcard'); await el.tap(); await pg.wait_for_timeout(1300)
        await swipe(pg, 4, 400, 400)  # no-op vertical; then horizontal edge swipe
        await pg.mouse.move(3, 420); await pg.mouse.down()
        for k in range(1, 20): await pg.mouse.move(3 + k * 16, 420); await pg.wait_for_timeout(16)
        await pg.mouse.up(); await pg.wait_for_timeout(1000)
        note('   after swipe', await pg.evaluate('location.hash'))
        note('10 History, Library, scroll each')
        for t in ('history', 'library'):
            await pg.evaluate(f"go('{t}')"); await pg.wait_for_timeout(1000); await scroll(pg, 1200, 8); await pg.wait_for_timeout(500)
        note('errors', errs)
        await ctx.close(); await b.close()
    json.dump(log, open(f'D:/tmp/oa/walk/{TAG}/log.json', 'w'))


asyncio.run(main())
