# Verification - liquid-glass-media (uncommitted work)

No typecheck/lint/test tooling exists in this repo (no package.json); none was run or invented.

## Static
- node --check on inline script (the one starting "/* ===="; only 1 inline script found, CDN include is src-based): PASS
- JSON parse manifest/portraits/episodes/media/palette: PASS (all 5)
- Files exist (icon.png, icon-192.png, apple-touch-icon.png, InstrumentSerif Regular/Italic woff2, SF-Pro.woff2): PASS
- All 31 image paths in portraits.json exist: PASS (0 missing)
- py_compile build_media.py grade_portraits.py palette.py: PASS

## Runtime (Playwright Chromium, server on :8123 returned 200)
Console errors, page errors, failed requests, HTTP >=400: NONE (verbatim: none) in either viewport.

| Check | 390x844 | 1440x900 |
|---|---|---|
| /home load, 2.5s | PASS | PASS |
| /figures (h1 "Figures") | PASS | PASS |
| /library ("Library") | PASS | PASS |
| /search ("Search") | PASS | PASS |
| /settings ("Settings") | PASS | PASS |
| /system ("Design System") | PASS | PASS |
| /p/steve-jobs ("Steve Jobs") | PASS | PASS |
| /l/speeches ("Speeches") | PASS | PASS |
| #q "napol" -> #qres children = 2 | PASS | not run (phone only) |
| ?state=player: #np.show, #npspeeds 5 buttons | PASS | PASS |
| closeNP() + 1s, no console error | PASS | PASS |
| #topnav visible | n/a | PASS |

Visual fidelity vs canon not assessed (not requested). Mobile device check: not requested (PWA, no Expo).

## Screenshots (D:\Podcast infrastructure\verification\)
phone-home.png, phone-figures.png, phone-library.png, phone-search.png, phone-settings.png, phone-system.png, phone-p-steve-jobs.png, phone-l-speeches.png, phone-search-napol.png, phone-player.png, desktop-home.png, desktop-home2.png, desktop-player.png

## Verdict
SHIP (no failures). Screenshots were captured but not visually inspected; checks are DOM/console based.
