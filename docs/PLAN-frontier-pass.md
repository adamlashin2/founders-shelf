# Frontier pass — plan (2026-10-31)

Built from a scripted audit of build 20261031-0900 (real playback in Chromium, screenshots of every surface,
light + dark, 390 px + 1440 px). Each item has a check that proves it fixed.

## Layer 1 — Liquid Glass, heavily frosted
Today: the floating bars are a murky grey tint; content shows through as legible text (tab bar over card names).
1. Source 4–6 high-taste frosted-glass references (Pinterest, blessed glass pins first).
2. Measure them by script: blur radius (edge spread through the glass), tint alpha (luminance of the same background
   inside vs outside the glass), rim highlight. Use those numbers; one `--glass-*` token set for light and dark.
3. Apply to every glass surface: tab pill, search circle, mini player, sidebar, top header, toast, buttons on photos,
   sheets/modals, tab lens.
Check: text under the tab bar is unreadable (blurred); the measured tint/blur match the refs within 10 %.

## Layer 2 — Header and identity
4. Header: iOS 26 scroll-edge header — large title at rest; on scroll a frosted bar with the inline title, logo mark and
   actions (settings/search). References from the frontier Pinterest pass.
5. Logo: generate candidates with Codex image generation (codex-image-gen skill), fed with the approved references and
   the Instrument Serif wordmark; pick, export as app icon (192/512/apple-touch) + header mark; manifest updated.
Check: header present and frosted on every top-level page in both appearances; icon files load (200) and manifest valid.

## Layer 3 — Glitches
6. Modal text invisible in dark (Ionic sets its own text colour): modals inherit the app's label colours.
7. Desktop Now Playing misplaced/overlapping the sidebar: centred modal, correct size, readable.
8. Black focus ring on close buttons: focus ring only for keyboard (`:focus-visible`), styled to the system.
9. Now Playing artwork double frame (cover inside a grey box): one clean artwork.
10. Home "Shelves" rendered as giant segment tabs: proper shelf cards.
11. Content under the tab bar: bottom scroll-edge fade so nothing collides with the bar.
12. Re-run the full sweep; anything new found here joins this list.
Check: screenshot audit shows none of the above; contrast of modal text ≥ 4.5:1 measured from pixels.

## Layer 4 — Playback, done properly
13. Resume plays from 0:00 for ~200 ms then jumps: seek before playing (on loadedmetadata).
14. Next at the end of a figure's list does nothing: continue into Up Next (next figure / next in queue), or say so.
15. Real queue: "Play Next" / "Add to Up Next" on episodes; Up Next shows and edits the queue; autoplay follows it.
16. Phone mini player: play/pause + skip forward 30 (Apple Podcasts), tap opens Now Playing.
17. Lock screen / control centre: `setPositionState`, seek handlers with the same 15/30 intervals.
18. Loading and error states: buffering indicator; failed episode shows a message and a retry.
19. Keyboard: Space play/pause, ←/→ seek, ⇧← / ⇧→ previous/next.
20. Mark as played / unplayed from the episode menu.
Check: playback audit script re-run — every row passes, resume first sample == saved position.

## Ship
21. Full regression (routes × appearances × sizes, navigation, swipe, modals, playback), commit, push, deploy
    gh-pages, confirm live version.txt.
