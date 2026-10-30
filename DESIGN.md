# The Greats — design system

**System v5 (2026-10-31): Adam's two picks become the operating system.** Pins `808888783111165642` (dark journal) and
`355714070590901781` (light assistant), chosen from ~270 Pinterest candidates. Values measured by script from the pin images
(`D:/tmp/oa/ds`), not by eye; the CSS block "SYSTEM v5" in `app/index.html` carries them.

| Token | Value | Measured from |
|---|---|---|
| Ground | `#000`, flat | journal, below the header |
| Panel | `#1c1c1e`, corner 20, gap 8, padding 16 | journal panels (369pt wide, 12pt inset, 19–20pt corner, 7–8pt gap) |
| Inner tile | `#323234`, corner 12, 52pt | journal play tile (51pt) |
| Big card | corner 28 | assistant card (27–28pt) |
| Two-tone text | 24/29, white lead then `#69696b` | assistant headline (24pt, 29pt pitch); journal placeholder `#69696b` |
| Text tabs | 22pt semibold, active white, rest `#69696b` | journal tabs (~23–24pt) |
| Circle button | 48pt, 1px hairline | assistant chips (47–48pt, rim `#e8e8e8` on `#f7f7f7`) |
| Primary | white pill, black text, 44pt | journal "Save Dream" (38pt, raised to the 44pt target) |
| Audio card | play tile + title + time + waveform; progress = clipped white copy of the bars | journal "Audio Record" |

Retired in v5: glass rims, gradient grounds, paper/tape/jacket textures, gold eyebrows, filled chips. Fonts unchanged
(Instrument Serif for names, SF Pro for everything you operate). Small text stays `#8e8e93` rather than the journal's
`#535355`, which fails contrast at 11–13pt.

**Direction (2026-10-30, frontier pass): tactile archival listening room.** The application chrome remains disciplined and
monochrome, while the content is allowed restrained material colour: cloth book jackets, ivory correspondence, broadcast programmes,
and graphite tape. Black-and-white portraits and Instrument Serif carry the editorial voice; SF Pro is reserved for everything the
listener operates. App icon: the glass laurel.

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
| Content-object stacks and quiet archive composition | `832954893628477100` |
| Books as dimensional hero objects | `53198839333782252` |
| Letter and document objects | `539024649169832628` |
| Edit tape vocabulary (reels, label, waveform; used with restraint) | `731272058261128395` |
| Wide desktop listening panel and compact transport | `4608589877548880960`, `415175659384999404` |
| macOS toolbar and card-grid hierarchy | `795589090467224683` |
| Reachable mobile playback hierarchy | `1101341283912421828`, `733101645643367237` |

## Design thesis

The Greats is an archival listening room, not a generic podcast dashboard. Portraits, book jackets, names, and the spoken archive are
the content layer. They carry the emotion. Navigation and playback are the functional layer, so they are the only places that use
glass. Quiet opaque surfaces organize everything else.

- **Signature:** monumental black-and-white portraits paired with editorial serif names.
- **Hierarchy:** one clear subject or action per view; secondary controls stay discoverable without competing.
- **Colour:** graphite, white, and ivory in the shell. Muted oxblood, bottle green, midnight blue, and tobacco appear only where a
  physical archive object would naturally have material colour. Red is reserved for destructive consequences in controls.
- **Adaptation:** compact widths keep reachable bottom navigation and 44-point targets; intermediate widths gain denser grids;
  wide layouts use a bounded 1180-pixel canvas, precise pointer states, and keyboard shortcuts.
- **Materials:** regular glass for floating navigation, playback, and temporary presentation. Content cards remain opaque.
- **Appearance:** dark is an intentional media-room art direction, with explicit increased-contrast, reduced-transparency, and
  reduced-motion variants.


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
| Runtime | Web Animations API plus View Transitions (card → page zoom, push / pop), compositor-driven and skipped for reduced motion |
| Frontier object pass | Pinterest brief `The Greats — tactile archive pass` (`f1a2ef57-0b39-44b9-9067-8557d6d9fa26`); references listed above were interpreted as material and hierarchy cues, not copied layouts |

## Motion (measured, 2026-10-30)

Curves are the ones measured frame-by-frame from Apple screen recordings earlier in this repo (commit `8d7f1ed`):
push = critically damped spring, τ 69 ms, 417 ms, no overshoot; sheet = same spring over 533 ms. All of it runs on the Web
Animations API / View Transitions (compositor-driven), no animation library.

| Motion | What morphs | 90 % | 99 % |
|---|---|---|---|
| Card → figure page | portrait + name (`hero`, `heroname`), page fades 200 ms underneath | — | 417 ms |
| Back | the page's portrait shrinks back into its card | — | 417 ms |
| Open Now Playing | phone sheet slides up; desktop listening panel resolves in-window; art grows out of the tapped content object | 156–168 ms | 326–340 ms |
| Close Now Playing / sheets | panel/sheet resolves away on the push curve; phone drag-to-dismiss uses Apple's momentum projection | 169–181 ms | 291–302 ms |
| Tab switch | none — instant, as on iOS | — | — |
| Press | scale .97 on pointer-down in 100 ms, release on the spring | | |

Sampled per frame in headless Chromium by `D:/tmp/oa/tools/motion_probe.py`. Decorative loops (Now Playing backdrop) pause while hidden.

## HIG interaction pass (2026-10-30)

The editorial treatment stays custom; navigation, controls, and state follow the Apple interaction model:

- phone controls use at least a 44×44 activation region, including filters, playback speed, sheet controls, and the mini-player;
- the mini-player exposes separate previous, play/pause, next, open-player, and queue actions instead of one compound click target;
- tab scroll position, the figure filter, and the active search query survive destination changes;
- current tabs, filters, favourites, playback speed, sleep state, dialogs, and the scrubber expose names, roles, and values to assistive technology;
- Now Playing and sheets contain keyboard focus, restore focus on dismissal, and retain explicit close buttons alongside drag-to-dismiss;
- empty states explain the state and provide one useful recovery route; startup has honest loading and retry states;
- destructive history clearing is outcome-labeled, unavailable when empty, and requires an explicit cancelable confirmation;
- desktop supports `Command/Control-F` for app search, `Command/Control-,` for settings, `/` for search, Space for playback, and Escape for dismissal/back;
- page zoom is not disabled, Reduce Motion, Reduce Transparency, and Increased Contrast remain supported, and search only auto-focuses for fine-pointer desktop input.

Sources: Apple HIG [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons), [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars), [Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields), [Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio), and [VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover).

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
| `--red` | `#F3EDE4` | legacy token name; the actual interactive accent is ivory |
| `--danger` | `#ff453a` | destructive actions only |
| `--glow` | `rgb(208,48,48)` | measured iPad Replay corner glow |
| `--fill` | white @ 10% | measured mini player over black |
| `--fill2` | white @ 17% | measured active tab lozenge |
| `--hair` | white @ 12% | measured Replay card rim |
| `--raised` | `#1c1c1e` | grouped list surface |

## Shape & space

Side margin 18 (phone), 28 (intermediate), 40 (desktop). Hero card 356×443 r19, ranked card 240×320 r14 (desktop 223×296), tiles r9, grouped lists r18, latest card 356×105 r18. Tab bar 58 tall, search button 60, mini player 50, play circle 61, phone glass buttons 44.

## Components

- **Buttons**: `.btn-primary` (white pill), `.btn-tinted` (white@17%), `.btn-red`, `.btn-glass`, `.btn-sm`, `.btn-icon(.sm)` (glass circles), `.btn-play` (61 white circle), `.chip(.on)`, `.textbtn`.
- **Glass** (`.glass`): fill + blur(24) saturate(1.9) + top/bottom specular insets + gradient rim. Floating chrome only, never content.
- **Cards and objects**: `.hero`, `.rcard`, `.tile`, `.pcard`, `.wide` (continue listening), `.cat` (monochrome browse tile), `.lcard` (latest), tactile book jackets, folded letters, speech programmes, and edit tapes. Each archive kind has a recognisable silhouette before its label is read.
- **Lists**: `.row` (number or artwork lead, inset separator), `.lnav` (Library nav rows), `.group/.grow` (Settings).
- **Chrome**: large title + collapsing glass nav bar; phone tab bar with travelling highlight + separate search circle; bounded desktop toolbar with brand, primary destinations, search, and settings; floating transport bar.
- **Playback presentation**: full-height, reachable Now Playing sheet on phone; wide two-column listening panel on desktop, with the current physical archive object beside title, progress, transport, and speed. The persistent transport hides while the desktop panel is open.
- **Sheets**: mobile Now Playing (drag to dismiss with velocity), Up Next, About, toast. Desktop uses window-appropriate panels rather than phone-shaped presentations.

## Pages

Home · Figures (shelf chips + portrait grid) · Library (nav rows, favourites) · Search (browse shelves + live results) · Person (artist page: hero, latest, Biographies / Speeches / Edits / Letters, About) · Lists (favourites, continue, finished, shelves, kinds) · Settings · Design system · Now Playing · Up Next.
