#!/usr/bin/env python3
"""Fetch one real portrait per figure from the Wikipedia REST API into app/assets/people/."""
import json, os, sys, time, urllib.request, urllib.parse

WIKI = {
 "Alexander the Great": "Alexander the Great",
 "Napoleon": "Napoleon",
 "Elon Musk": "Elon Musk",
 "Jeff Bezos": "Jeff Bezos",
 "Bill Gates": "Bill Gates",
 "Jensen Huang": "Jensen Huang",
 "Mark Zuckerberg": "Mark Zuckerberg",
 "Steve Jobs": "Steve Jobs",
 "John D. Rockefeller": "John D. Rockefeller",
 "Andrew Carnegie": "Andrew Carnegie",
 "Henry Ford": "Henry Ford",
 "Nikola Tesla": "Nikola Tesla",
 "J. Robert Oppenheimer": "J. Robert Oppenheimer",
 "Claude Shannon": "Claude Shannon",
 "Vannevar Bush": "Vannevar Bush",
 "Alfred Lee Loomis": "Alfred Lee Loomis",
 "Kelly Johnson - Skunk Works": "Kelly Johnson (engineer)",
 "Edwin Land - Polaroid": "Edwin H. Land",
 "Ed Catmull - Pixar": "Edwin Catmull",
 "Demis Hassabis - DeepMind": "Demis Hassabis",
 "Bill Walsh": "Bill Walsh (American football coach)",
 "Jim Simons": "Jim Simons",
 "Intel - Noyce Grove Shockley": "Robert Noyce",
 "Winston Churchill": "Winston Churchill",
 "Charles de Gaulle": "Charles de Gaulle",
 "Peter Thiel": "Peter Thiel",
 "Cornelius Vanderbilt": "Cornelius Vanderbilt",
 "J.P. Morgan": "J. P. Morgan",
 "The Rothschilds": "Mayer Amschel Rothschild",
 "Jacob Fugger": "Jakob Fugger",
 "James J. Hill": "James J. Hill",
}

def slug(name):
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")

os.makedirs("app/assets/people", exist_ok=True)
UA = {"User-Agent": "FoundersShelf/1.0 (personal study app)"}
manifest, missing = {}, []
for person, page in WIKI.items():
    fn = f"app/assets/people/{slug(person)}.jpg"
    if os.path.exists(fn) and os.path.getsize(fn) > 5000:
        manifest[person] = f"assets/people/{slug(person)}.jpg"
        print(f"have {person}")
        continue
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(page.replace(" ", "_"))
    ok = False
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=UA)
            data = json.load(urllib.request.urlopen(req, timeout=30))
            thumb = (data.get("thumbnail") or {}).get("source")
            if not thumb:
                break
            req2 = urllib.request.Request(thumb, headers=UA)
            with urllib.request.urlopen(req2, timeout=60) as r, open(fn, "wb") as f:
                f.write(r.read())
            manifest[person] = f"assets/people/{slug(person)}.jpg"
            print(f"ok  {person} <- {page}")
            ok = True
            break
        except Exception as e:
            print(f"  retry {attempt+1} {person}: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    if not ok:
        missing.append(person)
    time.sleep(0.5)

with open("app/portraits.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=1)
print(f"\n{len(manifest)} portraits, missing: {missing}")
