# Experience map — walking The Greats as a listener (2026-11-01)

Each row: what a person does → what a high-taste iOS app does (Apple Music / Apple Podcasts / Apple Books
standard) → what The Greats did → status. Rows marked FIX are this pass; LATER are queued with references.

## Everywhere
| Action | Expected | Was | Status |
|---|---|---|---|
| Images appear | fade in once decoded, no pop or grey flash | pop in | FIX |
| A screen appears | content settles in (short fade/rise, staggered by section) | everything snaps in at once | FIX |
| Floating chrome (tab bar, mini player, header, sidebar, buttons on photos) | frosted: heavy blur, real tint — what's behind is soft colour, never readable | translucent, content legible through it; sidebar opaque | FIX |
| Press anything | immediate press-down feedback, spring release | partial | FIX (audit) |
| Scroll a page | frosted header bar fades in with the inline title as the large title leaves | title floats over content | FIX |

## Home
| Action | Expected | Was | Status |
|---|---|---|---|
| Look at "Choose a great" cards | name sits on a soft blur over the portrait | blur removed (plain gradient) | FIX |
| Tap a great | the card zooms into the figure page; back zooms into the card | zoom removed by Codex — plain slide | FIX |
| Star a great | star fills with a small spring bounce, stays in place | page morph | FIX |
| Look at "New books" | real, distinct book covers (the actual books) | thumbnail rows of the figure's portrait | FIX |
| Tap a book | plays it; mini player springs up | ok | — |

## Figure page
| Action | Expected | Was | Status |
|---|---|---|---|
| Books row | real covers, each distinct | the same portrait on every book | FIX |
| Back | zoom back into the card it came from | slide | FIX |

## Now Playing
| Action | Expected | Was | Status |
|---|---|---|---|
| Drag the playhead | seek anywhere, 1:1 with the finger | jumped to the end (bar shrank to 36 px — class clash) | FIXED |
| Tap the artwork or title | go to that figure's page | nothing | FIX |
| Tap the figure name | go to the figure | nothing | FIX |
| Artwork | the real book cover for books | figure portrait | FIX |
| Read along | transcript / subtitles | missing | LATER (Layer 5) |

## Mini player
| Action | Expected | Was | Status |
|---|---|---|---|
| Tap | Now Playing opens, artwork grows from the mini art | card slides up | FIX |
| Play/pause | icon morphs | swaps | FIX |

## Layer 5 (queued, reference-first)
Real letters (voice), richer book pages, read-along transcript, edits gallery, photo gallery per figure, header + logo.
