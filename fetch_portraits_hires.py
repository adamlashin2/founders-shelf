#!/usr/bin/env python3
"""Re-fetch portraits at 800px via the MediaWiki action API (pithumbsize allows arbitrary sizes)."""
import json, os, sys, time, urllib.request, urllib.parse
from fetch_portraits import WIKI, slug

UA = {"User-Agent": "FoundersShelf/1.0 (personal study app; contact: local)"}
os.makedirs("app/assets/people", exist_ok=True)
ok, fail = 0, []
for person, page in WIKI.items():
    fn = f"app/assets/people/{slug(person)}.jpg"
    if os.path.exists(fn) and os.path.getsize(fn) > 45000:
        ok += 1
        continue
    try:
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "pageimages",
            "piprop": "thumbnail", "pithumbsize": 800, "redirects": 1,
            "titles": page,
        })
        req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q, headers=UA)
        data = json.load(urllib.request.urlopen(req, timeout=30))
        pages = data["query"]["pages"]
        thumb = None
        for _, pg in pages.items():
            thumb = (pg.get("thumbnail") or {}).get("source")
        if not thumb:
            fail.append(person); continue
        req2 = urllib.request.Request(thumb, headers=UA)
        with urllib.request.urlopen(req2, timeout=60) as r, open(fn, "wb") as f:
            f.write(r.read())
        ok += 1
        print(f"ok {person} ({os.path.getsize(fn)//1024} KB)")
        time.sleep(3)
    except Exception as e:
        fail.append(person)
        print(f"FAIL {person}: {e}", file=sys.stderr)
        time.sleep(3)
print(f"\n{ok} upgraded, failed: {fail}")
