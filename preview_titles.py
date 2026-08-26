#!/usr/bin/env python3
"""Preview every person's shelf as it will render, so mangling is caught before shipping.
Mirrors the epTitle() rule in index.html: strip the subject's name when it leads the
feed title, otherwise leave the title whole; prefer the book the episode is built on."""
import json, io, re, sys

def ep_title(person_name, short_name, title):
    words = short_name.split()
    vars = [person_name, short_name]
    if len(words) == 2:
        vars.append(words[1])
    uniq = sorted({v for v in vars if v and len(v) > 2}, key=len, reverse=True)
    for v in uniq:
        q = re.escape(v)
        m = re.match(r'^' + q + r'\s*\((.+)\)\s*$', title, re.I)
        if m and len(m.group(1)) > 2:
            return m.group(1)
        # Only structural separators. Conjunctions are excluded on purpose:
        # "Steve Jobs and His Heroes" must stay whole, not become "His Heroes".
        m = re.match(r'^' + q + r'\s*(?::|–|—|-)\s*(.+)$', title, re.I)
        if m and len(m.group(1)) > 2:
            return m.group(1)
    return title

d = json.load(io.open("app/episodes.json", encoding="utf-8"))
only = sys.argv[1] if len(sys.argv) > 1 else None
for p in d["people"]:
    if only and only.lower() not in p["name"].lower():
        continue
    short = p["name"].split(" - ")[0]
    print(f"\n=== {p['name']}  ({len(p['episodes'])} episodes)")
    for i, e in enumerate(p["episodes"], 1):
        book = (e.get("book") or "").strip()
        line = book if book else ep_title(p["name"], short, e["title"])
        src = "book" if book else "title"
        auth = e.get("author") or ""
        sub = (auth + "  ") if auth else ""
        print(f"  {i:2d}. {line[:78]:78s} | {src:5s} | {sub}")
