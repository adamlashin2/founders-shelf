"""Find layouts that don't fit, from real DOM geometry. Usage: layoutaudit.py <tag> [light|dark]"""
import asyncio, json, sys
from playwright.async_api import async_playwright
TAG = sys.argv[1]; SCHEME = sys.argv[2] if len(sys.argv) > 2 else 'dark'
ROUTES = ['home', 'figures', 'library', 'history', 'search', 'settings', 'p/napoleon', 'p/steve-jobs', 'l/favs', 'l/speeches', 'l/letters', 'l/shelf-military', 'l/continue', 'system']
SIZES = [(393, 852), (834, 1194), (1440, 900)]
JS = r"""() => {
  const W=innerWidth, H=innerHeight, out=[];
  const page=[...document.querySelectorAll('#view .page')].pop(); if(!page) return ['no page'];
  const scrollers=el=>{ for(let p=el.parentElement;p&&p!==page;p=p.parentElement){ const c=getComputedStyle(p); if(/(auto|scroll)/.test(c.overflowX)&&p.scrollWidth>p.clientWidth+2) return true; } return false; };
  const name=el=>{ let n=el.tagName.toLowerCase(); if(el.id) n+='#'+el.id; if(el.className&&typeof el.className==='string') n+='.'+el.className.trim().split(/\s+/).slice(0,2).join('.'); const t=(el.textContent||'').trim().slice(0,28); return n+(t?` "${t}"`:''); };
  const vis=el=>{ const c=getComputedStyle(el); return c.visibility!=='hidden'&&c.display!=='none'&&+c.opacity>0.05; };
  const all=[...page.querySelectorAll('*')].filter(el=>{ const r=el.getBoundingClientRect(); return r.width>0&&r.height>0&&vis(el); });
  // 1 horizontal overflow
  all.forEach(el=>{ const r=el.getBoundingClientRect(); if((r.right>W+1||r.left<-1)&&!scrollers(el)&&!el.closest('.fxbg,.hxbg,.nbg,.qstack,.cloud')) out.push(`overflow x ${Math.round(r.left)}..${Math.round(r.right)} ${name(el)}`); });
  // 2 clipped text (no ellipsis intended)
  all.filter(el=>el.children.length===0&&(el.textContent||'').trim().length>2).forEach(el=>{ const c=getComputedStyle(el);
    if(el.scrollWidth>el.clientWidth+2&&c.textOverflow!=='ellipsis'&&c.overflow!=='visible'&&!el.closest('.trunc,.clamp2')) out.push(`clipped text ${name(el)}`); });
  // 3 overlapping tap targets
  const taps=all.filter(el=>el.matches('button,a,[role=button]')&&!el.closest('.hxrow,.qstack'));
  for(let i=0;i<taps.length;i++) for(let j=i+1;j<taps.length;j++){ const a=taps[i],b=taps[j]; if(a.contains(b)||b.contains(a)) continue;
    const r=a.getBoundingClientRect(), s=b.getBoundingClientRect(); const ox=Math.min(r.right,s.right)-Math.max(r.left,s.left), oy=Math.min(r.bottom,s.bottom)-Math.max(r.top,s.top);
    if(ox>4&&oy>4) out.push(`overlap ${name(a)}  ×  ${name(b)}`); }
  // 4 small targets
  taps.forEach(el=>{ const r=el.getBoundingClientRect(); if((r.width<30||r.height<30)&&r.top<H&&r.bottom>0) out.push(`small target ${Math.round(r.width)}x${Math.round(r.height)} ${name(el)}`); });
  // 5 fixed chrome vs page header
  const chrome=[...document.querySelectorAll('#nshdr .nsb,#tabbar,#mini')].filter(e=>e.getBoundingClientRect().width&&vis(e));
  all.filter(el=>el.matches('h1,h2,button,.t-page')&&el.getBoundingClientRect().top<200).forEach(el=>{ const r=el.getBoundingClientRect();
    chrome.forEach(c=>{ if(c.contains(el)) return; const s=c.getBoundingClientRect(); if(Math.min(r.right,s.right)-Math.max(r.left,s.left)>4&&Math.min(r.bottom,s.bottom)-Math.max(r.top,s.top)>4) out.push(`under chrome ${name(el)} × ${name(c)}`); }); });
  return [...new Set(out)];
}"""
END = r"""() => { const page=[...document.querySelectorAll('#view .page')].pop(); page.scrollTop=page.scrollHeight; return new Promise(r=>setTimeout(()=>{
  const bar=[...document.querySelectorAll('#tabbar,#mini')].filter(e=>e.getBoundingClientRect().height&&getComputedStyle(e).visibility!=='hidden').map(e=>e.getBoundingClientRect().top);
  const top=bar.length?Math.min(...bar):innerHeight; const els=[...page.querySelectorAll('button,p,h2,.row,.pcard,.artifact-card,.gplay,.sdisc')].filter(e=>e.getBoundingClientRect().height);
  const last=els.sort((a,b)=>b.getBoundingClientRect().bottom-a.getBoundingClientRect().bottom)[0];
  r(last&&last.getBoundingClientRect().bottom>top+2?`end hidden under bar: ${Math.round(last.getBoundingClientRect().bottom-top)}pt (${(last.className||'').toString().slice(0,30)})`:'');},350)); }"""


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:/Users/adaml/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe')
        report = {}
        for w, h in SIZES:
            c = await b.new_context(viewport={'width': w, 'height': h}, color_scheme=SCHEME); pg = await c.new_page()
            await pg.goto(f'http://localhost:8123/?v={TAG}#/home'); await pg.wait_for_timeout(1200)
            await pg.evaluate("""()=>{ ['napoleon','steve-jobs'].forEach((s,i)=>{ const p=BYSLUG[s]; const e=p.episodes[0]; store.set('t.'+epKey(p,e),Date.now()-i*36e5); store.set('pos.'+epKey(p,e),900); }); store.set('favs',['Napoleon','Steve Jobs']); store.set('last',{slug:'napoleon',i:0,k:'bio'}); }""")
            for r in ROUTES:
                await pg.goto(f'http://localhost:8123/?v={TAG}#/{r}'); await pg.reload(); await pg.wait_for_timeout(1200)
                issues = await pg.evaluate(JS)
                end = await pg.evaluate(END)
                if end: issues.append(end)
                if issues: report[f'{w} {r}'] = issues
            await c.close()
        await b.close()
    n = 0
    for k, v in report.items():
        print(f'== {k} ({len(v)})')
        for x in v[:12]: print('   ', x)
        n += len(v)
    print('TOTAL', n)
    json.dump(report, open(f'D:/tmp/oa/shots/layout-{TAG}.json', 'w'), indent=1)


asyncio.run(main())
