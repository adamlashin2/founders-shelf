import asyncio, json
from playwright.async_api import async_playwright
W=json.load(open('ref/aurora_widths.json'))
for k in ['Search','Invite']: W.pop(k,None)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=r'C:/Users/adaml/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe')
        pg=await b.new_page(); await pg.goto('http://localhost:8123/'); await pg.wait_for_timeout(1500)
        res=await pg.evaluate("""W=>{ const c=document.createElement('canvas').getContext('2d'); const out={};
          for(const [t,w] of Object.entries(W)){ const r=[];
            for(const wt of [400,500,600,700]){ c.font=`${wt} 100px "SF Pro"`; const m=c.measureText(t);
              const ink=m.actualBoundingBoxLeft+m.actualBoundingBoxRight; r.push([wt,+(w/ink*100).toFixed(1)]); }
            out[t]=r; } return out; }""", W)
        for t,r in res.items(): print(f'{t:28s} {W[t]:6.1f}pt  ', '  '.join(f'w{wt}:{s}' for wt,s in r))
        await b.close()
asyncio.run(main())
