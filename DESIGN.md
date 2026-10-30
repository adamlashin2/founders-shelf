# The Greats — design system

**Direction (2026-10-30, revised): monochrome editorial.** Per-figure colour was removed at Adam's request ("not a colouring
festival"). One neutral ground, black-and-white portraits, Instrument Serif for names and titles, SF Pro for everything you operate,
white pills for primary actions. App icon: the glass laurel.

## Components and the reference each is built from
Pinterest brief "The Greats · components" (`D:/tmp/oa/sheets5`, picks in `pick.jpg`). Concept shots have no fixed scale, so
structure and proportions come from the reference; type sizes stay on the Apple HIG scale below.

| Component | Reference |
|---|---|
| Person page, phone — inset portrait card, name bottom-left, quote, stats, full-width white pill | `1121959326098177962` "Jane Mayhem" |
| Person page, desktop — portrait card left, huge serif name, bio, Books shelf | `1028509633628855309` "Mark Twain" |
| Book jackets — a generated cover per Founders episode (No., serif title, author, spine light, progress) | Twain "Books" row |
| Now Playing — Now Playing / Up Next tabs, square art, % complete, −30 / play / +15 | `526991593901020783` dark audiobook player |
| Playback speed chips (outlined selection) | `142215300727898240` |
| Library — Currently playing card with % chip, Recents | `526991593901020783` Library |
| Editorial nav rows — big label, `[count]`, arrow | `4611615768377300032` |
| Home — search, "Popular this week" portrait cards with overlaid title | `4610841701090354752` "Discover" |
| Figure cards with overlaid name | `1045116657290183465`, `1121959326098177962` |

---|---|---|
| Ground | each screen sits on its figure's hue: radial top `hsl(h, s·100%, 30%)` over `hsl(h, s·90%, 17%) → 8% → 5%` | C refs: art hue at L .31 → .17 (pins 60, 65, 71) |
| Ground family | ember 16/.47 · umber 19/.29 · bronze 33/.50 · amber 31/.70 · sage 147/.14 · moss 99/.40 · graphite 220/.06 · crimson 1/.55 · azure 207/.45 · sand 29/.20 (hue / sat) | median border colour of each reference, `palette.py` |
| Assignment | per shelf subset, rotating within a shelf so neighbours differ → `app/palette.json` | |
| Morph | `--gh/--gs` are registered `@property` numbers, so the ground animates between figures (0.9 s spring) | |
| Glass | the ground desaturated and lifted: `hsl(h, s·35%, 80%) @ 12%`, blur 30, saturate 1.4 | C: panel S .10–.16 vs ground S .35–.6 |
| Portraits | duotone: photo luminosity over `hsl(h, s·85%, 46%)` (`.toned`) | B: tonal poster portraits (pins 21, 37, 56) |
| Display type | Instrument Serif (OFL, self-hosted): page titles 44/46, figure names 56/56 (96 desktop), sections 28/32, card names 22/24 | B: serif display names |
| UI type | SF Pro, Apple HIG iOS table (below) | |
| Accent | ivory `#F3EDE4` pills on tinted grounds (replaces the red, which fought every ground) | B: white chips |

---


One system for every screen, phone and desktop. Every value has a source; nothing is picked by eye.
The live, rendered version is in the app: **Library → ⚙ → Design system** (`#/system`).

## Sources

| What | Source |
|---|---|
| Type sizes, leading, weights | Apple HIG *Typography*, iOS "Large (default)" Dynamic Type table (developer.apple.com HIG data, fetched 2026-10-30) |
| Tracking per size | Apple HIG SF Pro tracking table (same fetch) |
| Colour, radii, component sizes | Measured by script from real iOS 26 / iPadOS 26 Apple Music screenshots on Pinterest: Home `739434832610073940`, artist page `1091911872195345882`, iPad Replay `898890406989751969`, iPhone Replay `1046946244644498781` |
| Library / Settings / Search patterns | Apple Music Library `769834130101817658`, Apple Games Library `832954893623780849`, Apple Music Search `4591138481938600000` |
| Motion | Apple *Designing Fluid Interfaces*: default spring damping 1.0 / response 0.4 s; sheets 0.8 / 0.3 s; momentum projection `v/1000·d/(1−d)`, d = 0.998 |
| Spring runtime | Motion `motion@11.11.13` (jsDelivr, pinned) |
| Page morphs | View Transitions API (card → page zoom, push / pop), capped at 900 ms, skipped when hidden or reduced-motion |

## Motion (measured, 2026-10-30)

Curves are the ones measured frame-by-frame from Apple screen recordings earlier in this repo (commit `8d7f1ed`):
push = critically damped spring, τ 69 ms, 417 ms, no overshoot; sheet = same spring over 533 ms. All of it runs on the Web
Animations API / View Transitions (compositor-driven), no animation library.

| Motion | What morphs | 90 % | 99 % |
|---|---|---|---|
| Card → figure page | portrait + name (`hero`, `heroname`), page fades 200 ms underneath | — | 417 ms |
| Back | the page's portrait shrinks back into its card | — | 417 ms |
| Open Now Playing | sheet slides up; art grows out of whatever was tapped (mini player art, book jacket, row thumbnail) | 156–168 ms | 326–340 ms |
| Close Now Playing / sheets | slide away on the push curve; drag-to-dismiss uses Apple's momentum projection | 169–181 ms | 291–302 ms |
| Tab switch | none — instant, as on iOS | — | — |
| Press | scale .97 on pointer-down in 100 ms, release on the spring | | |

Sampled per frame in headless Chromium by `D:/tmp/oa/tools/motion_probe.py`. Decorative loops (Now Playing backdrop) pause while hidden.

## Type (iOS Large)

| Style | Size / leading | Weight | Tracking |
|---|---|---|---|
| Display (desktop headline) | 40 / 46 | Bold | +0.37 |
| Large Title | 34 / 41 | Bold | +0.40 |
| Title 1 | 28 / 34 | Bold | +0.38 |
| Title 2 | 22 / 28 | Bold | −0.26 |
| Title 3 | 20 / 25 | Semibold | −0.45 |
| Headline | 17 / 22 | Semibold | −0.43 |
| Body | 17 / 22 | Regular | −0.43 |
| Callout | 16 / 21 | Regular | −0.31 |
| Subhead | 15 / 20 | Regular | −0.23 |
| Footnote | 13 / 18 | Regular | −0.08 |
| Caption 1 | 12 / 16 | Regular | 0 |
| Caption 2 | 11 / 13 | Regular | +0.06 |

Classes: `.t-display .t-large .t-title1 .t-title2 .t-title3 .t-head .t-body .t-callout .t-sub .t-foot .t-cap1 .t-cap2 .t-eyebrow`.

## Colour

| Token | Value | Source |
|---|---|---|
| `--bg` | `#000` | every background probe in the Apple dark refs |
| `--label` | `#fff` | |
| `--label2` | `rgb(142,142,147)` | measured = systemGray |
| `--red` | `rgb(232,66,78)` | measured active tab, iOS 26 Home — the one accent |
| `--glow` | `rgb(208,48,48)` | measured iPad Replay corner glow |
| `--fill` | white @ 10% | measured mini player over black |
| `--fill2` | white @ 17% | measured active tab lozenge |
| `--hair` | white @ 12% | measured Replay card rim |
| `--raised` | `#1c1c1e` | grouped list surface |

## Shape & space

Side margin 18 (phone, measured) / 40 (desktop). Hero card 356×443 r19, ranked card 240×320 r14 (desktop 223×296), tiles r9, grouped lists r18, latest card 356×105 r18. Tab bar 58 tall, search button 60, mini player 43, play circle 61, glass buttons 44 / 36.

## Components

- **Buttons**: `.btn-primary` (white pill), `.btn-tinted` (white@17%), `.btn-red`, `.btn-glass`, `.btn-sm`, `.btn-icon(.sm)` (glass circles), `.btn-play` (61 white circle), `.chip(.on)`, `.textbtn`.
- **Glass** (`.glass`): fill + blur(24) saturate(1.9) + top/bottom specular insets + gradient rim. Floating chrome only, never content.
- **Cards**: `.hero`, `.rcard`, `.tile`, `.pcard`, `.wide` (continue listening), `.cat` (browse tile), `.lcard` (latest).
- **Lists**: `.row` (number or artwork lead, inset separator), `.lnav` (Library nav rows), `.group/.grow` (Settings), `.trow` (tinted gradient rows).
- **Chrome**: large title + collapsing glass nav bar; phone tab bar with travelling highlight + separate search circle; desktop centred glass tab pill; floating transport bar.
- **Sheets**: Now Playing (drag to dismiss with velocity, animated artwork backdrop), Up Next, About, toast.

## Pages

Home · Figures (shelf chips + portrait grid) · Library (nav rows, favourites) · Search (browse shelves + live results) · Person (artist page: hero, latest, Biographies / Speeches / Edits / Letters, About) · Lists (favourites, continue, finished, shelves, kinds) · Settings · Design system · Now Playing · Up Next.
