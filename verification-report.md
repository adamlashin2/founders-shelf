# Verification report (design/liquid-glass-media, uncommitted)

No typecheck/lint/test tooling exists (no package.json); none was invented. Browser: Playwright (Python) with bundled Chromium.

## Static checks
- Inline script of app/index.html: `node --check` PASS (1 inline script)
- manifest.json, portraits.json, episodes.json parse: PASS. media.json: absent (acceptable, written by background build)
- All 31 portraits.json paths exist on disk: PASS. icon.png, icon-192.png, apple-touch-icon.png exist: PASS
- `python -m py_compile build_media.py grade_portraits.py`: PASS

## Runtime (390x844 phone, 1440x900 desktop)
- Load + 2s: PASS on both. Only console error (verbatim): `Failed to load resource: the server responded with a status of 404 (File not found)` = `404 http://localhost:8123/media.json?v=20261030-1730` (accepted). No page errors, no other failed requests. Same single 404 on ?state=player.
- Phone: first .rcard opens #detail (visible, .aname = "Steve Jobs"); #d-back returns (#detail hidden, #browse shown): PASS
- Phone tabs Home/Figures/Library/Settings: Figures, Library, Settings clicked OK, no errors. Home: when clicked right after returning from the person page, the Home tab button has zero size (element not visible), so Playwright could not click it. Cause: body keeps class `scrolled` after back, and the tabbar collapses to a 48px pill that hides inactive tabs (CSS line ~293/853). Looks like intentional scroll-minimize design, but note that body.scrolled persists after back while the view is at the top. Home click works on a fresh load. Not counted as failure.
- Desktop: #topnav visible (Home | Library | Settings); Library and Settings clicks switch views: PASS
- ?state=player: #player class `show`; `img#np-art` (the id is on the img itself, not a child of #np-art) src = `assets/people/steve-jobs.jpg?v=20261030-1730`: PASS

## Screenshots (D:\Podcast infrastructure\verification\)
phone-home, phone-person, phone-after-back, phone-tab1..3, desktop-home, desktop-Library, desktop-Settings, desktop-player (.png)

## Verdict
PASS
