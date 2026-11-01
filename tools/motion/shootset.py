import asyncio, sys
from playwright.async_api import async_playwright
tag=sys.argv[1]; R=sys.argv[2].split(',')
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=r'C:/Users/adaml/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe')
        errs=[]
        for sch,w,h,n in (('light',402,874,'m'),('dark',402,874,'m'),('light',1440,900,'d')):
            c=await b.new_context(viewport={'width':w,'height':h},color_scheme=sch); pg=await c.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('http://localhost:8123/?v='+tag+'#/home'); await pg.wait_for_timeout(1200)
            await pg.evaluate("""()=>{ ['napoleon','steve-jobs','winston-churchill'].forEach((s,i)=>{ const p=BYSLUG[s]; const e=p.episodes[0]; store.set('t.'+epKey(p,e),Date.now()-i*36e5*20); store.set('pos.'+epKey(p,e),900); }); store.set('favs',['Napoleon','Steve Jobs']); }""")
            for r in R:
                await pg.goto(f'http://localhost:8123/?v={tag}#/{r}'); await pg.reload(); await pg.wait_for_timeout(1300)
                await pg.screenshot(path=f'shots/{tag}-{sch}-{n}-{r.replace("/","_")}.png')
                if r=='home' and n=='m':
                    await pg.evaluate("[...document.querySelectorAll('#view .page')].pop().scrollTo(0,330)"); await pg.wait_for_timeout(500)
                    await pg.screenshot(path=f'shots/{tag}-{sch}-{n}-home2.png')
            await c.close()
        print('errors',errs); await b.close()
asyncio.run(main())
