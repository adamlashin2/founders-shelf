# The Greats — design system

**Authority: the Notensprung design system** (Adam, 2026-11-08: "take the design system from my Notensprung… use it as the
authoritative"). Its source is Notensprung's founding reference, the invite screen (left phone of Pinterest pin
1085789791447549624, `D:/Notensprung/design/refs/invite/`). Notensprung's own rules apply here: `D:/Notensprung/AGENTS.md`,
`D:/Notensprung/ai/design/SYSTEM.md`, `D:/Notensprung/ai/design/CORRECTIONS.md`.

## Where the values come from
- `python tools/ns_tokens.py` reads `D:/Notensprung/app/src/design/invite.tokens.json` (measured by Notensprung's
  `tools/measure_invite.py`) and the `--ns-*` theme variables of `D:/Notensprung/app/src/index.css`, and writes them into
  `app/index.html` between the `NS-TOKENS` markers. Never edit that block by hand; re-run the script.
- The "SYSTEM: Notensprung" CSS layer in `app/index.html` only maps those variables onto The Greats' elements.

## The vocabulary (from Notensprung)
- Surface = glass card, radius 31, translucent white, blur 24 + saturate 150, no borders.
- Round button = 43 pt glass circle. The phone header is exactly two of them on every screen, at the measured positions:
  left = menu (back on pushed screens), right = search ("…" on a figure). No per-screen header buttons.
- Primary action = the white pill with the green label (#3ea133). Filters = the segmented capsule; selected = white pill.
- Tags/meta = the small capsule (25.3 pt). Badges and the only accent = green (#14b604).
- Tab bar = the founding segmented control: 353.2 × 53.07 capsule, sliding white pill (0.96 of a slot), icons only, current
  icon green, no "+". Sheets = the system sheet, radius 38.
- Type = SF: info 15.71 (60 %), segment 13.99, section labels = the host line (13.47 / 500, lavender), body 14.44.
- Photo screens (Home hero, figure page, Now Playing) stay dark in both themes (Notensprung `.ns-force-dark`); text on a
  photo is always white.

## Exceptions (decided per element, as in Notensprung SYSTEM.md → Exceptions)
| Where | Kept | Why / who |
|---|---|---|
| Page and hero titles | Instrument Serif, never small, never lowercased | Adam 2026-11-01: serif for the bigger text |
| Dark theme ground + inks | Apple dark system colours: ground #000, label #fff, secondary rgb(235 235 245 / .6), capsule #48484a | Adam 2026-11-08: "proper darkmode instead of a greenish color" |

## Checks
- `D:/tmp/oa/tools/layoutaudit.py` (overflow, clipped text, overlapping targets, content under the bar) at 393 / 834 / 1440.
- Flash walk, human walk (incl. quit + relaunch resume), playback / swipe / modal / scrub / push-pop suites.
