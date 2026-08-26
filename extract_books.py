#!/usr/bin/env python3
"""Pull each episode's description from the official feed and extract the BOOK
it is built on. Founders episodes are 'what I learned from reading <book> by <author>',
so the book is the real distinction between two episodes about the same person.
Only factual metadata (book title, author) is stored - never the description text."""
import json, io, re, sys, urllib.request, xml.etree.ElementTree as ET
from html import unescape

FEED = "https://feeds.megaphone.fm/DSLLC6297708582"
UA = {"User-Agent": "Mozilla/5.0"}

def fetch():
    req = urllib.request.Request(FEED, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as r:
        root = ET.fromstring(r.read())
    out = {}
    for it in root.find("channel").findall("item"):
        title = (it.findtext("title") or "").strip()
        desc = unescape(it.findtext("description") or "")
        desc = re.sub(r"<[^>]+>", " ", desc)
        desc = re.sub(r"\s+", " ", desc).strip()
        m = re.match(r"#\s*(\d+)", title)
        key = int(m.group(1)) if m else title
        out[key] = {"title": title, "desc": desc}
    return out

# "what I learned from reading X by Y" and its many variants. Order matters:
# the with-author forms run first so the author is captured when it is present.
# An author is a run of capitalised name-words, optionally joined by "and"/"&".
# Bounding it this tightly matters: a loose class runs straight past the author
# into the show-notes boilerplate that follows ("Ashlee Vance The conventional
# wisdom of the time said to take...").
AUTH = r"((?:[A-Z][\w’'\-\.]*)(?:\s+(?:and\s+|&\s+)?[A-Z][\w’'\-\.]*){0,3})"

PATTS = [
    r"what I learned (?:from|by)\s+(?:re-?reading\s+|reading\s+)?(.{4,140}?)\s+by\s+" + AUTH,
    r"this episode is what I learned by reading\s+(.{4,140}?)\s+by\s+" + AUTH,
    r"(?:reading|read)\s+(?:the book\s+)?[“\"](.{4,140}?)[”\"]\s*by\s+" + AUTH,
    # no author named
    r"what I learned (?:from|by)\s+(?:re-?reading\s+|reading\s+)?(.{4,140}?)\s*(?:\.|-{3,}|—{2})",
    r"(?:reading|read)\s+(?:the book\s+)?[“\"](.{4,140}?)[”\"]",
]
# episodes built on a body of work rather than one book
SPECIAL = [
    (r"shareholder letters", "Shareholder Letters"),
    (r"company-building principles", "Company-building principles"),
]

# Typos in the feed's own descriptions. Only obvious misspellings of real book
# titles are corrected here — never a rewording.
FIXES = {
    "Inside Steve's Brian": "Inside Steve's Brain",
}


def clean_author(a):
    """Authors are 'First Last', sometimes with an initial, sometimes two joined by
    'and'. Anything beyond that shape is the next sentence bleeding in, so cut it."""
    w = [x for x in re.split(r"\s+", a.strip(" ,:;")) if x]
    if not w:
        return ""
    # An initial is a short token ending in a period ("D."). A longer token ending
    # in a period is a surname at a sentence end ("Cain."), not an initial.
    is_initial = lambda x: len(x) <= 2 and x.endswith(".")
    take = 2
    if len(w) > 1 and is_initial(w[1]):         # "John D. Rockefeller"
        take = 3
    out = w[:take]
    if len(w) > take and w[take].lower() in ("and", "&"):
        out += w[take:take + 3]
    return " ".join(out).strip(" .,:;&")


def find_book(desc):
    d = desc.replace("’", "'")
    for p in PATTS:
        m = re.search(p, d, re.I)
        if m:
            book = m.group(1).strip(" .,:;—-“”\"")
            author = ""
            if m.lastindex and m.lastindex >= 2 and m.group(2):
                author = clean_author(m.group(2))
            book = re.sub(r"^(the book|his book|her book)\s+", "", book, flags=re.I)
            # the feed occasionally drops the space before "by", gluing the author
            # onto the last word of the title ("...Creation of Appleby Michael Moritz")
            g = re.match(r"^(.*?[a-z])by\s+" + AUTH + r"\s*$", book)
            if g:
                book, author = g.group(1).strip(), g.group(2).strip()
            book = book.strip(" .,:;—-“”\"")
            # a captured "book" that is really a trailing clause is not a title
            if 3 < len(book) < 140 and not re.match(r"^(this|that|it|he|she|they)\b", book, re.I):
                return FIXES.get(book, book), author
    for pat, label in SPECIAL:
        if re.search(pat, d, re.I):
            return label, ""
    return "", ""

if __name__ == "__main__":
    feed = fetch()
    data = json.load(io.open("app/episodes.json", encoding="utf-8"))
    hit = miss = 0
    misses = []
    for p in data["people"]:
        for e in p["episodes"]:
            key = e["n"] if e["n"] is not None else e["full_title"]
            src = feed.get(key)
            if not src:
                e["book"], e["author"] = "", ""
                miss += 1; misses.append((p["name"], e["n"], "NO FEED MATCH"))
                continue
            b, a = find_book(src["desc"])
            e["book"], e["author"] = b, a
            if b: hit += 1
            else:
                miss += 1; misses.append((p["name"], e["n"], src["desc"][:90]))
    json.dump(data, io.open("app/episodes.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"book found: {hit}   no book: {miss}\n")
    for name, n, d in misses[:40]:
        print(f"  {name:26s} #{str(n):5s} {d}")
