#!/usr/bin/env python3
"""Build every non-biography shelf (edits, speeches, letters) into app/media/.

Reads media_sources.json:  { person: { kind: [item, ...] } }   where an item is
  { id, title, sub, q | url }           audio pulled with yt-dlp; `q` is a
                                        YouTube search, resolved once and pinned
  { id, title, sub, text:{...}, voice } a public text, cut between two markers
                                        and narrated with edge-tts

Writes app/media/<person>/<kind>/<id>.mp3 (mono 64 kbps) and app/data/media.json.
Already-built files are skipped, so re-running only fetches what is new.
Every resolved source (video id, channel, title, text url) is recorded next to
the item so a bad pick is easy to see and swap.
"""
import asyncio, html, io, json, re, subprocess, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # repo root (scripts live in tools/)
APP = ROOT / "app"
SRC = ROOT / "media_sources.json"
OUT = APP / "data" / "media.json"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126 Safari/537.36"}
SEC_UA = {"User-Agent": "founders-shelf personal research mahmoud.lashin00@gmail.com"}
LIMITS = {"edits": (30, 420), "speeches": (60, 5400)}   # seconds, for search picks

slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def probe_sec(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return round(float(r.stdout.strip() or 0))


# ---------------------------------------------------------------- audio
def fetch_audio(item, kind, dest):
    lo, hi = LIMITS.get(kind, (0, 99999))
    target = item.get("url") or f"ytsearch8:{item['q']}"
    cmd = [sys.executable, "-m", "yt_dlp", target, "--no-playlist", "-q", "--no-warnings",
           "--match-filter", f"duration>={lo} & duration<={hi} & !is_live",
           "--max-downloads", "1", "-f", "bestaudio/best", "-x", "--audio-format", "mp3",
           "--postprocessor-args", "ffmpeg:-ac 1 -b:a 64k",
           "--print", "after_move:%(id)s\t%(channel)s\t%(title)s",
           "-o", str(dest.with_suffix(".%(ext)s"))]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf8", errors="replace")
    line = (r.stdout.strip().splitlines() or [""])[-1]
    if not dest.exists():
        raise RuntimeError(r.stderr.strip()[-300:] or "no result inside the duration window")
    vid, ch, title = (line.split("\t") + ["", "", ""])[:3]
    return {"from": f"https://youtu.be/{vid}" if vid else item.get("url"), "channel": ch, "source_title": title}


# ---------------------------------------------------------------- text
def get(url):
    hdr = SEC_UA if "sec.gov" in url else UA
    return urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=60).read()


def to_text(raw, fmt):
    if fmt == "pdf":
        import pypdf
        return "\n".join(p.extract_text() for p in pypdf.PdfReader(io.BytesIO(raw)).pages)
    t = raw.decode("utf8", errors="replace") if fmt == "txt" else raw.decode("latin1")
    if fmt == "html":
        t = re.sub(r"(?is)<(script|style).*?</\1>", "", t)
        t = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</h\d>|</li>", "\n\n", t)
        t = html.unescape(re.sub(r"<[^>]+>", "", t))
    return t


def clean(t, drop):
    t = t.replace("\r", "")
    for k, v in {"’": "'", "‘": "'", "“": '"', "”": '"', "—": " - ",
                 "\x92": "'", "\x93": '"', "\x94": '"', "\x97": " - ", "�": "'", "--": " - "}.items():
        t = t.replace(k, v)
    t = re.sub(r"\[\d+\]", "", t)               # footnote markers
    t = t.replace("_", "")                      # gutenberg italics
    lines = [l for l in t.split("\n") if not any(re.search(d, l) for d in drop)]
    paras = re.split(r"\n\s*\n", "\n".join(lines))
    paras = [re.sub(r"\s+", " ", p).strip() for p in paras]
    return "\n\n".join(p for p in paras if p and not re.fullmatch(r"\d+|Table of Contents", p))


def build_text(item):
    spec = item["text"]
    t = to_text(get(spec["url"]), spec.get("format", "html"))
    a = t.find(spec["from"])
    if a < 0:
        raise RuntimeError(f"start marker not found: {spec['from']!r}")
    b = t.find(spec["until"], a + len(spec["from"])) if spec.get("until") else len(t)
    if b < 0:
        raise RuntimeError(f"end marker not found: {spec['until']!r}")
    return clean(t[a:b], spec.get("drop", []))


async def narrate(text, voice, dest):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate="-4%").save(str(dest) + ".raw.mp3")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(dest) + ".raw.mp3",
                    "-ac", "1", "-b:a", "64k", str(dest)], check=True)
    Path(str(dest) + ".raw.mp3").unlink()


# ---------------------------------------------------------------- main
def main():
    src = json.loads(SRC.read_text(encoding="utf8"))
    prev = json.loads(OUT.read_text(encoding="utf8")) if OUT.exists() else {"people": {}}
    out = {"people": {}}
    only = sys.argv[1:]                          # optional: person names to (re)build
    for person, kinds in src.items():
        if person.startswith("_"):
            continue
        for kind, its in kinds.items():
            for it in its:
                d = APP / "media" / slug(person) / kind
                d.mkdir(parents=True, exist_ok=True)
                mp3 = d / f"{it['id']}.mp3"
                old = next((x for x in prev["people"].get(person, {}).get(kind, []) if x["id"] == f"{kind}:{it['id']}"), None)
                rec = {"id": f"{kind}:{it['id']}", "title": it["title"], "sub": it.get("sub", ""),
                       "url": f"media/{slug(person)}/{kind}/{it['id']}.mp3"}
                try:
                    if not mp3.exists() and (not only or person in only):
                        if "text" in it:
                            body = build_text(it)
                            (d / f"{it['id']}.txt").write_text(body, encoding="utf8")
                            asyncio.run(narrate(body, it.get("voice", "en-US-AndrewNeural"), mp3))
                            rec["source"] = {"from": it["text"]["url"], "narrated": it.get("voice", "en-US-AndrewNeural"),
                                             "words": len(body.split())}
                        else:
                            rec["source"] = fetch_audio(it, kind, mp3)
                        print(f"  built  {person} / {kind} / {it['id']}", flush=True)
                    elif old:
                        rec["source"] = old.get("source", {})
                    if not mp3.exists():
                        continue
                    rec["sec"] = probe_sec(mp3)
                    out["people"].setdefault(person, {}).setdefault(kind, []).append(rec)
                except Exception as e:
                    print(f"  FAILED {person} / {kind} / {it['id']}: {e}", flush=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf8")
    n = sum(len(v) for k in out["people"].values() for v in k.values())
    print(f"media.json: {n} items across {len(out['people'])} people")


if __name__ == "__main__":
    main()
