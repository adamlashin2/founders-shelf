"""Fetch the real cover of every book an episode is built on.

Open Library search (CC0 catalogue, Internet Archive) first, Google Books as fallback.
Writes app/assets/books/<slug>.jpg (480 px tall) and app/data/covers.json:
    { "<book title>": "assets/books/<slug>.jpg" }
Run from the repo root:  python tools/fetch_covers.py
"""
import io, json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
APP = ROOT / "app"
OUT = APP / "assets" / "books"
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "TheGreats/1.0 (personal listening app; covers for personal use)"}


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:70]


def clean_title(t):
    # drop subtitles and trailing fragments ("--As Told", "edited") so the search matches the book
    t = re.split(r"\s*[:—–]|--", t)[0]
    return re.sub(r"\b(edited|a selection)\b.*$", "", t, flags=re.I).strip()


def clean_author(a):
    a = (a or "").replace(" and ", ",").split(",")[0].strip()
    return "" if len(a.split()) < 2 or a.lower().startswith("his ") else a


def openlibrary(title, author):
    q = {"title": clean_title(title), "limit": "5", "fields": "cover_i,title,author_name,edition_count"}
    if author:
        q["author"] = author
    data = json.loads(get("https://openlibrary.org/search.json?" + urllib.parse.urlencode(q)))
    docs = [d for d in data.get("docs", []) if d.get("cover_i")]
    if not docs:
        return None
    docs.sort(key=lambda d: -d.get("edition_count", 0))  # the canonical edition, not an obscure one
    return get(f"https://covers.openlibrary.org/b/id/{docs[0]['cover_i']}-L.jpg?default=false")


def openlibrary_q(title, author):
    # looser full-text search: "<short title> <author>" — catches books the field search misses
    q = {"q": (clean_title(title) + " " + (author or "")).strip(), "limit": "8", "fields": "cover_i,title,author_name,edition_count"}
    data = json.loads(get("https://openlibrary.org/search.json?" + urllib.parse.urlencode(q)))
    want = clean_title(title).lower()[:18]
    docs = [d for d in data.get("docs", []) if d.get("cover_i") and want[:12] in d.get("title", "").lower()]
    if not docs:
        return None
    docs.sort(key=lambda d: -d.get("edition_count", 0))
    return get(f"https://covers.openlibrary.org/b/id/{docs[0]['cover_i']}-L.jpg?default=false")


def googlebooks(title, author):
    q = f'intitle:"{clean_title(title)}"' + (f' inauthor:"{author}"' if author else "")
    data = json.loads(get("https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode({"q": q, "maxResults": "5"})))
    for it in data.get("items", []):
        links = it.get("volumeInfo", {}).get("imageLinks", {})
        u = links.get("extraLarge") or links.get("large") or links.get("medium") or links.get("thumbnail")
        if u:
            u = u.replace("http://", "https://").replace("&edge=curl", "").replace("zoom=1", "zoom=3")
            return get(u)
    return None


def usable(raw):
    try:
        im = Image.open(io.BytesIO(raw)).convert("RGB")
    except Exception:
        return None
    w, h = im.size
    if w < 120 or h < 140 or not (1.05 <= h / w <= 1.8):   # portrait covers; tightly cropped scans run ~1.1
        return None
    return im


def main():
    eps = json.loads((APP / "data" / "episodes.json").read_text(encoding="utf-8"))
    books = {}
    for p in eps["people"]:
        for e in p["episodes"]:
            if e.get("book"):
                books.setdefault(e["book"], clean_author(e.get("author")))
    out_map_path = APP / "data" / "covers.json"
    covers = json.loads(out_map_path.read_text(encoding="utf-8")) if out_map_path.exists() else {}
    ok = miss = 0
    for title, author in books.items():
        if title in covers and (APP / covers[title]).exists():
            ok += 1
            continue
        im = None
        for src in (openlibrary, openlibrary_q, googlebooks):
            for a in (author, ""):
                try:
                    raw = src(title, a)
                except Exception:
                    raw = None
                im = raw and usable(raw)
                if im:
                    break
                time.sleep(0.3)
            if im:
                break
        if not im:
            miss += 1
            print("MISS", title, "|", author)
            continue
        im = im.resize((round(480 * im.width / im.height), 480), Image.LANCZOS)
        name = slug(title) + ".jpg"
        im.save(OUT / name, quality=84, optimize=True, progressive=True)
        covers[title] = f"assets/books/{name}"
        ok += 1
        print("ok  ", title)
        time.sleep(0.4)
    out_map_path.write_text(json.dumps(covers, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{ok} covers, {miss} missing -> app/data/covers.json")


if __name__ == "__main__":
    sys.exit(main())
