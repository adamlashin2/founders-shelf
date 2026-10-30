# Verification - app/index.html (branch design/liquid-glass-media)

## Static checks
- typecheck / lint / tests: N/A (single-file PWA, inline CSS+JS, no build, tests or lint)
- Inline script (starts with "/* ====") extracted, `node --check`: PASS
- Only one <script> tag in the file; Motion CDN tag gone: PASS
- No window.Motion or M.animate references (only comments mention Motion): PASS

## Runtime (Playwright Chromium, 390x844 and 1440x900)
- Load /?v=verify#/home, 2.5s: no console errors, page errors, failed requests or HTTP >=400: PASS (both viewports)
- Routes figures, library, search, settings, system, p/steve-jobs, l/speeches: all rendered non-empty h1 (Figures, Library, Search, Settings, Design System, Steve Jobs, Speeches), 0 new errors: PASS
- Now-playing: #np has .show, transform matrix(1,0,0,1,0,0) (translateY 0); after closeNP() .show removed: PASS
- Sheet: openSheet shows .show; closeSheet removes it: PASS
- openPerson('napoleon') -> route p/napoleon; history.back() -> route figures; no errors: PASS
- No audio playback started.

## Verdict
SHIP
