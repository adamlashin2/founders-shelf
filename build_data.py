#!/usr/bin/env python3
"""Parse the official Founders feed into app/episodes.json for the shelf app."""
import json, re, sys, urllib.request, xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED = "https://feeds.megaphone.fm/DSLLC6297708582"
UA = {"User-Agent": "Mozilla/5.0"}

CORE = [
 ("Alexander the Great",        [232, 226]),
 ("Napoleon",                   [294, 302, 337]),
 ("Elon Musk",                  [1, 11, 12, 13, 30, 38, 172, 233, 369, 399, 414, 415]),
 ("Jeff Bezos",                 [17, 38, 71, 155, 179, 180, 282, 321, 374, 388]),
 ("Bill Gates",                 [44, 140, 174, 208, 290, 401]),
 ("Jensen Huang",               [376, 403]),
 ("Mark Zuckerberg",            [14]),
 ("Steve Jobs",                 [5, 19, 36, 76, 77, 204, 214, 235, 249, 265, 281, 299, 349, 350, 390, 398, 420]),
 ("John D. Rockefeller",        [16, 148, 247, 248, 254, 307, 324, 359, 368, 405]),
 ("Andrew Carnegie",            [73, 74, 75, 283, 284]),
 ("Henry Ford",                 [9, 26, 80, 118, 190, 266]),
 ("Nikola Tesla",               [83]),
 ("J. Robert Oppenheimer",      [215]),
]
ADJACENT = [
 ("Claude Shannon",             [92, 95, 428]),
 ("Vannevar Bush",              [270, 271]),
 ("Alfred Lee Loomis",          [143]),
 ("Kelly Johnson - Skunk Works",[419]),
 ("Edwin Land - Polaroid",      [40, 132, 133, 134, 263, 264]),
 ("Ed Catmull - Pixar",         [34, 317]),
 ("Demis Hassabis - DeepMind",  [416]),
 ("Bill Walsh",                 [106]),
 ("Jim Simons",                 [108, 387]),
 ("Intel - Noyce Grove Shockley",[8, 159, 165, 166, 356]),
 ("Winston Churchill",          [196, 225, 319, 320]),
 ("Charles de Gaulle",          [224]),
 ("Peter Thiel",                [31, 278, 424]),
 ("Cornelius Vanderbilt",       [54, 55, 341]),
 ("J.P. Morgan",                [139, 142]),
 ("The Rothschilds",            [197, 198]),
 ("Jacob Fugger",               [250]),
 ("James J. Hill",              [96, 371]),
]
UNNUMBERED = {
 "Steve Jobs": ["Steve Jobs  and Edwin Land", "Steve Jobs's Heroes", "Steve Jobs and His Heroes"],
 "Jeff Bezos": ["Jeff Bezos (Insights, Stories, and Secrets)"],
}

def fetch_feed():
    req = urllib.request.Request(FEED, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as r:
        root = ET.fromstring(r.read())
    ns = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}
    eps = []
    for it in root.find("channel").findall("item"):
        title = (it.findtext("title") or "").strip()
        enc = it.find("enclosure")
        if enc is None:
            continue
        m = re.match(r"#\s*(\d+)", title)
        dur = it.findtext("itunes:duration", "0", ns)
        img = it.find("itunes:image", ns)
        pub = it.findtext("pubDate") or ""
        try:
            pub_iso = parsedate_to_datetime(pub).date().isoformat()
        except Exception:
            pub_iso = ""
        eps.append({
            "n": int(m.group(1)) if m else None,
            "title": title,
            "url": enc.get("url"),
            "sec": int(dur) if str(dur).isdigit() else 0,
            "img": img.get("href") if img is not None else None,
            "date": pub_iso,
        })
    return eps

def clean_title(t, person):
    # strip leading "#NNN " and trailing " | Founders" style noise
    t = re.sub(r"^#\s*\d+\s*[:.]?\s*", "", t).strip()
    return t

def build(eps):
    by_n = {e["n"]: e for e in eps if e["n"]}
    by_t = {e["title"].strip(): e for e in eps}
    out = {"people": [], "generated_from": FEED}
    for tier, rows in (("core", CORE), ("adjacent", ADJACENT)):
        for person, nums in rows:
            items = [by_n[n] for n in sorted(set(nums)) if n in by_n]
            items += [by_t[t] for t in UNNUMBERED.get(person, []) if t in by_t]
            items.sort(key=lambda e: (e["n"] is None, e["n"] or 9999))
            if not items:
                print(f"  !! no episodes found for {person}", file=sys.stderr)
                continue
            out["people"].append({
                "name": person,
                "tier": tier,
                "hours": round(sum(e["sec"] for e in items) / 3600, 1),
                "episodes": [{
                    "n": e["n"], "title": clean_title(e["title"], person),
                    "full_title": e["title"], "url": e["url"], "sec": e["sec"],
                    "img": e["img"], "date": e["date"],
                } for e in items],
            })
    return out

if __name__ == "__main__":
    eps = fetch_feed()
    data = build(eps)
    n_eps = sum(len(p["episodes"]) for p in data["people"])
    hrs = sum(p["hours"] for p in data["people"])
    with open("app/episodes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"{len(data['people'])} people, {n_eps} episodes, {hrs:.0f}h -> app/episodes.json")
    # sample artwork URLs so we can verify they are real per-episode art
    for p in data["people"][:3]:
        e = p["episodes"][0]
        print(f"  {p['name']}: #{e['n']} img={str(e['img'])[:90]}")
