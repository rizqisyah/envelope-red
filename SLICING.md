# Slicing notes — template 5

Both frames are sliced. This file carries the method the earlier templates arrived at
plus this template's own measurements. Keep the traps — every one of them cost real
time to find.

`../slicing-wedding-template-4` is the finished reference implementation. Read its
`SLICING.md` and its `src/components/sections/*.vue` when a rule here needs an example.

## What this repo already has

| Path | What it is |
|---|---|
| `src/App.vue` | Desktop split layout (left panel + 430px column), cover→body reveal |
| `src/components/cover/CoverSection.vue` | **Sliced** from Frame 254. Layer table in `src/lib/coverLayers.ts` |
| `src/components/invite/InviteBody.vue` | **Placeholder.** The sheet: declares `--px` and lists the bands |
| `src/components/invite/BandArt.vue` | Renders a `BandLayer[]` table with per-layer entrances. Design-agnostic |
| `src/lib/bandLayer.ts` / `bandAssets.ts` | The layer type, and the glob that turns `src/assets/<band>/parts/*.webp` into urls |
| `src/lib/api.ts` / `composables/useWedding.ts` | Live data + `DESIGN_MODE`. Every band's copy is data-driven |
| `src/composables/useReveal.ts` / `useFitText.ts` / `usePreloadAssets.ts` | Scroll reveal, text fitting, asset preload (glob-driven, no edit needed) |
| `src/style/tokens.css` | Colour + font tokens. Sampled off Frame 254; `--body-h` still to come |
| `scripts/` | The slicing toolchain, below |

Dev server runs on **5178** (template-4 is on 5176) so both can run side by side.

## The frames

| Frame | Node | Size | State |
|---|---|---|---|
| 254 — cover | `2852:577` | 375 x 725 | sliced → `src/components/cover/CoverSection.vue` |
| 253 — body | `2852:202` | 375 x 7979 | sliced → `src/components/sections/*.vue` |

`.figma-ref/frame254-raw.json` is the cover's full child list with a verdict per node;
`-assets.json` is the four layers that survived. For the body, `frame253-zorder.json`
is every node in global paint order with its band, `-assets.json` the 148 sliced
sprites, and `-alpha/-place/-blend.json` the three solved properties (below). Work from
those rather than re-querying Figma.

## The body frame's bands

Frame 253's 268 nodes are cut into 14 bands. Band tops are derived by `gen_band.py` from
the nodes assigned to each; the assignment itself is a y-range table in
`scripts/build_refs.py`, because Figma has no section marker to read.

| band | y | band | y |
|---|---|---|---|
| hero | 0 | acara (akad + resepsi) | 4265 |
| quote | 701 | youme | 5132 |
| invite | 1010 | gift | 5281 |
| bride | 1491 | rsvp | 6024 |
| groom (opens with the divider) | 2226 | wish | 6414 |
| gallery | 3143 | closing | 7082 |
| theday | 3795 | footer | 7631 |

Akad and Resepsi are ONE band: the design draws them inside a single floral arch whose
layers cross both cards, and splitting it would put half that arch in each band's
coordinate space for no gain. The "And / Better together" divider is the head of `groom`
for the same reason.

**The first band starts at 0, not at its first child.** Frame 253's first child sits at
y 67; honouring that would open a 67px gap above the sheet. `band_tops()` clamps it.

**Round the tops, then derive the heights.** Rounding a top and its height independently
leaves a 1px seam wherever both round the same way, and the sheet ends up short of
`--body-h`. `sheet-shot.mjs` prints the built sheet height — it must equal 7979 exactly.

## Palette (sampled off Frame 254's own fills)

| Token | Value | Where |
|---|---|---|
| `--wine` / `--paper` | `#530915` | `Rectangle 124`, the plate the whole cover sits on |
| `--gold-bright` | `#eed891` | couple name, "Click to open..." |
| `--gold-pale` | `#e8e4a9` | "The Wedding Of" |
| `--gold-muted` | `#d0cb84` | guest block |

`--paper` is the wine, not a cream — it is the ground for `<body>`, the desktop column
and `.cover`, and any other value flashes at every seam on a full-bleed design.

## Fonts

| Figma face | Token | Shipping as |
|---|---|---|
| Charoly Demo | `--font-display` | **the real file**, self-hosted from `src/assets/fonts/`. Demo cut, personal-use only |
| BusinessPenmanshipW00-Bold | `--font-script` | **SUB** — Playball. No webfont and no file |
| Ibarra Real Nova Medium Italic | `--font-serif` | fontsource, as authored |
| Jost | `--font-sans` | fontsource, as authored |

Playball's compensation lives on `.cover__eyebrow`: **size up** 20 → 23 and `left`
53 → 51. Playball sets *narrower* than the penmanship, which is the opposite of the way
these substitutions usually go — do not assume the sign. Retiring the substitute means
reverting both numbers, not just the family.

## The thing that will bite you: exported bounds are not node bounds

Figma's reported node bounds and the size it actually exports disagree in two directions:

- **Clipped.** Figma clips every export to the frame. A node that bleeds off an edge comes
  back narrower than it claims — its true x is 0, not the negative number it reports.
- **Expanded.** A rotated node, or one with a blur, exports a bbox *larger* than the node.
  Figma grows it around the node's centre, so re-centre it: `x = fx + fw/2 − exportW/2`.
- **Reported bounds can lie outright.** A rotated node can report an x past the right edge
  and still render visibly somewhere else entirely.

So placement tables are **generated, not hand-written**. Every position is either a
template match against the Figma render (`scripts/locate.py`, err < 40 = real match) or
derived from the clip/expansion rule. Regenerate rather than nudging numbers by hand.

## Toolchain

```sh
python3 scripts/flatten_frame.py <raw node json> <flat json>   # once per Figma re-dump
python3 scripts/build_refs.py                               # zorder + assets + webp
BODY_FRAME=253 BODY_H=7979 python3 scripts/gen_band.py         # every band
BODY_FRAME=253 BODY_H=7979 python3 scripts/gen_band.py hero    # just one
BODY_FRAME=253 BODY_H=7979 python3 scripts/solve_alpha.py      # opacity/blend/position

npm run dev &                                                  # port 5178
node scripts/sheet-shot.mjs 5178                               # 1:1 sheet shot
BODY_FRAME=253 python3 scripts/sheet-score.py                  # every band, one pass
BAND_REF=<1x body render.png> python3 scripts/band-diff.py <y0> <y1>   # one band, 3-up
LOCATE_REF=<1x frame render.png> python3 scripts/locate.py <asset.webp>
node scripts/shot.mjs 5178                                     # eyeball at 3 viewports
```

The loop is: `gen_band` (raw geometry) → `solve_alpha` (refine) → `gen_band` (bake) →
`sheet-shot` → `sheet-score`. `solve_alpha` persists ABSOLUTE positions, so running it
again after a regenerate refines the previous pass instead of doubling it. Two passes
converge; a third moves nothing.

## Figma's MCP does not report opacity or blendMode

`get_node` and `get_design_context` return bounds, fills and type — and nothing else.
Every export therefore comes back at full strength and stacked normally, which is wrong
for two whole classes of layer in this file:

- **Light-leak plates.** `2877:258` and `2894:882` (both "Pngtree shadow overlay window")
  are near-black rasters with light streaks, authored to be SCREENED over the band.
  Stacked normally they are a grey slab across everything.
- **Faded texture.** Several lace and glitter plates run at a fraction of full opacity.

`scripts/solve_alpha.py` recovers all three properties — opacity, blend mode and a
residual position — by compositing the band offline and scoring it against the render.
Two things make that composite match what the browser paints, and both were bugs first:

- **Bands overlap**, so the window is filled from EVERY band's table in global `z`
  order, not just this band's own layers.
- **The sheet's ground is two CSS plates**, not one (`GROUND` in the script). They are
  in `InviteBody.vue` rather than any band table, so the solver has to paint them itself.

**The gates are deliberately blunt.** A free search over ±40px, nine opacities and five
blend modes can almost always shave a hundredth off a busy band by moving a layer
somewhere visibly wrong. `MOVE_GAIN`, `MIN_GAIN` and `DROP_GAIN` make a change pay for
itself before it is kept, and `MIN_SOLVE` skips anything under 24px — a 9px dot matches
any patch of its own colour, so its Figma bounds are better evidence than any search.
Loosening these was measurably worse: at the original thresholds the solver faded the
"Save the Date" card to 20% and moved the gallery's dark plate 46px left.

**Solve order is position → paint → position → paint.** Paint-first fades a
correctly-shaped layer out of a band because it is in the wrong place; position-first
chases the grey slab a screened plate makes. Both get a second look.

`gen_band.py` reads `.figma-ref/frame<N>-zorder.json` and `-assets.json` and writes
`src/lib/bands/<band>.ts`. Its three exception sets — `PAINTS_NOTHING`, `TRUST_CLIP`,
`PIN_X` — start **empty**; they are per-design and every entry needs a before/after delta
for that node alone. Measure them one at a time: layers that share a source asset look
like a set and usually are not.

## Bands overlap

A band's height is the distance to the **next** band's top, not the extent of its own
children — children that overrun simply paint past the boundary, which is what the design
does. `section` in the zorder dump is derived from heading y positions and is a **hint**,
not verified.

**`z` is the GLOBAL Figma child order.** Every band shares one stacking context, which is
what keeps cross-band layering correct after the split. Do not give a band `z-index` — it
becomes its own context and the global order stops working. Anything a band draws on top
of its art needs its own node's real global z; a z copied from another band puts the
control underneath the art, and it looks like an opacity bug, not a z bug.

## Off-frame nodes: occluded is not absent

Rotated nodes report boxes outside the frame, but Figma still exports pixels for them and
most land back inside as mirrored decorations. `gen_band.py` searches the full frame width
for those (`rescue()`).

When the search *fails*, the layer is either buried under later layers or genuinely
absent, and `locate.py` cannot tell the two apart — it scores over all of a layer's opaque
pixels, so a mostly-buried layer scores badly even where it belongs. **An err above
`GOOD_ERR` on a layer that overlaps its siblings is not evidence of anything.** A failed
search therefore falls back to the clip rule; only `PAINTS_NOTHING` is dropped, and only
for layers that paint an artifact the render does not have.

Settle the ambiguous ones by compositing the band offline and scoring it against the
render (`scripts/solve_band.py`, `scripts/worth.py`, `scripts/band-diff.py`), not by eye.

**A flat-colour layer defeats `locate.py`.** Cream matches cream anywhere, so a blurred
single-colour plate scores under `GOOD_ERR` a couple of hundred px from where it belongs.
Those go in `TRUST_CLIP`, which `gen_band.py` honours *before* the first `locate` hit.

**Both-edges-bleed breaks the clip rule.** The rule guesses which edge cut an export; a
node bleeding past both gets pinned to the wrong side and stacks on its own mirror. `PIN_X`.

## Live text, and what stays as art

Every text node stays **live** so `useWedding()` can drive it — never bake type into an
image to dodge a missing face. Each family is one token in `tokens.css`, so swapping a
substitute for a licensed file means changing one value.

**Retiring a substitute means re-measuring, not just swapping the family.** Substitutes set
a different number of characters per line and their line boxes sit differently, so both the
font-size compensations *and* the positions have to be re-measured by ink box against the
render. Compensations that existed only for a substitute's metrics must be reverted to the
Figma spec at the same time.

Two traps that display faces keep repeating:

- **Do not `text-transform: uppercase` a display face without checking its case pairs.**
  Several of these faces put cap-height alternates on lowercase and swash or fraktur forms
  on the capitals, so uppercasing swaps the whole word onto the wrong set.
- **An authored newline in a Figma string cannot survive `useWedding()`.** Reproduce the
  break with `text-wrap: balance` and a box narrow enough to force the wrap.

Record the license beside every self-hosted `@font-face` in `style.css`. Several of the
faces these templates use are demo cuts that are personal-use only.

**Two exceptions, both `TEXT_PATH`.** "Love brought us here" (`2896:932`) and "just us!"
(`2857:223`) are lettering bent along a curve. Nothing in CSS reproduces that and neither
is data-driven, so both ship as art — the only text in either frame that does.

**Chrome that has to work ships as CSS, not as a raster.** A picture of an input cannot
be typed into and a picture of three wish cards cannot grow with a longer message, so
these are skipped from their band's `LAYERS` and redrawn:

| band | skipped | why |
|---|---|---|
| rsvp | `2852:389`, `2852:387` | the field and Send plates; the other two fields are frames Figma never exported at all |
| wish | `2894:863/872/877`, `2894:880`, `2894:860` | fixed-height card plates, the "Show more" bar, and the send icon |
| gift | `2852:357/358/360`, `2852:333/341` | the copy buttons, and the BCA logos — which are per-account, not per-card |
| gallery | `2875:232/233/234` | the carousel dots, which now carry active state |

**Skipping is per-node and easy to half-do.** A raster left in the table under something
the component also draws is invisible when the two agree and wrong the moment they do
not: the BCA logos would have printed over a Mandiri account number, and the Send plate
sat 71px off the button, only looking right because it landed on the select, which is the
same colour. Whatever a band redraws, skip.

**An icon the design exports is not one to redraw in CSS.** Both button glyphs started as
hand-built shapes — a `box-shadow` double outline and a `clip-path` triangle — and both
are now the exported asset inside a real `<button>`. Less code, and the glyph is Figma's
rather than a guess at it.

The wish list is a flow, not three plates: a live message can be any length, and the
design's own three are already two different heights. The gift and acara bands go the
other way — their art has a fixed number of apertures, so both cap the live list at what
the art can hold (3 accounts, 2 events) rather than painting past the last plate.

**A `Show more` that reveals nothing is worse than no button**, so the wish band's design
fallback carries FOUR wishes. Frame 253 draws three cards and the bar; with only three
fallback wishes the bar would never appear and the band would not match the render.

**An authored newline cannot survive an HTML template either.** `&#10;` in a Vue template
is folded to a space by the parser, so the design's own breaks ("Save the / Date",
"Wedding / invitation", "Where / love becomes / home.") come from a script constant and
the box sets `white-space: pre-line`. This is the same trap as the `useWedding()` one
above, one layer further out.

## Design mode

`DESIGN_MODE` lives in `src/lib/api.ts` — **at the boundary, not in a composable**, because
sections import `submitRsvp` / `submitUcapan` directly and a guard that lived only in
`useWedding` let those POSTs through to production. It is on unless `VITE_LIVE_DATA=1`:
`getHome` is never called, so every band renders the design's own content; the submits
throw; and a wish posted in this state is answered locally so the form still works end to
end.

Design-mode wishes are held in a module ref, **not** in `state.data` — seeding `state.data`
would make `wedding` non-null and every band would abandon its design fallback mid-session.

## Two more that cost real time

**A positioned wrapper eats the coordinate system.** Every band child is
`position: absolute` in design px against the band. Wrapping children in a plain `<div>`
makes that div the containing block, and with no offsets of its own everything inside
lands against a zero-size box — the band renders blank. Use `<template v-for>`.

**Scroll the window, not `.desktop-right-column`,** when screenshotting. That column only
scrolls at >=768px; below that the bands never reveal, which reads as a blank sheet rather
than a scroll bug.

## Still open

Three light-leak/texture plates report positions the render contradicts and no full-frame
match beats err 80, so they sit where the clip rule left them and their bands carry the
difference: `2893:849` (rsvp's diagonal light wash), `2877:263` (the gallery card's
glitter panel) and the oval-and-pearls between the two acara cards. Each needs the offline
composite treatment in "Off-frame nodes" above — score the band with the layer at each
candidate spot, not by eye.

`figma-mcp-go` reports no `opacity` and no `blendMode`, which is why `solve_alpha.py`
exists at all. The official `plugin:figma:figma` server exposes a `use_figma` tool that
runs JavaScript against the file and may be able to read both directly; it needs an OAuth
round trip this session did not have. If it can, one call over 148 node ids replaces the
whole inverse problem with ground truth and `solve_alpha.py` collapses to a position-only
refiner. Worth testing before the next template.

## Deployment

`VITE_DEFAULT_SLUG` must be set per deployment — without it `src/lib/api.ts` falls back to
`demo-envelop`, which is a *different* wedding and will render the wrong couple.

## Band fidelity

Track mean abs delta per band here once the sheet is up. It is a **relative** signal across
bands, not an absolute fidelity score: it carries every deliberate deviation from the render
— substitute fonts, the live countdown where the design bakes a static plate, the live wish
list and gallery where it bakes rasters of mock content.

Cover: `web-mobile.png` vs `.figma-tmp/frame254-1x.png`. Body: `web-sheet-1x.png` vs
`.figma-tmp/exports253/frame253-full.png`, one row per band, from
`BODY_FRAME=253 python3 scripts/sheet-score.py`. Per channel, 0-255, unmasked — so every
band carries its own deliberate deviations: the substitute faces, the live countdown
where the design bakes four zeroes, and the live wish/gallery lists where it bakes
rasters of mock content.

| band | delta | band | delta |
|---|---|---|---|
| cover (Frame 254, below the status bar) | 1.35 | acara | 11.53 |
| hero | 7.97 | youme | 6.34 |
| quote | 12.30 | gift | 4.58 |
| invite | 6.27 | rsvp | 18.42 |
| bride | 3.15 | wish | 16.71 |
| groom | 2.80 | closing | 2.72 |
| gallery | 17.61 | footer | 5.57 |
| theday | 6.96 | **sheet (0–7979)** | **8.54** |

The four worst bands are the four with the most live chrome, and most of their number is
that chrome rather than a placement error:

- **rsvp 18.42** — the design prints a filled-in sample form; the live one shows
  placeholders, which are lighter by design. Its light-leak plate (`2893:849`) is also
  still unplaced: it reports x 457, fully off-frame, and no full-frame match beats err 80.
- **wish 16.71** — three fixed plates in the design against a live list that grows with
  its content, plus the same substitute-italic difference in every card.
- **gallery 17.61** — the linen card's glitter panel (`2877:263`) is the same unplaced
  case as the rsvp plate: reported at y 3822, best full-frame match err 82.
- **quote 12.30 / acara 11.53** — Playball standing in for BusinessPenmanshipW00, and
  Bellefair set against the render's own hinting, over a lot of small copy.

## Cover-specific findings

**Only four of Frame 254's eight non-text children paint anything.** `Rectangle 124` is
flat `#530915` and became a CSS background; `bac 1` is flat white and fully buried under
it; `watermarked_img_...-Photoroom 4` exports 1x1 fully transparent; the iOS status bar
is device chrome. Export first, decide after — the frame's node list is not the layer list.

**This MCP exports nodes unclipped, but not always.** `bac 1` came back 375 wide against
a declared 422, so the clip rule still applies. The two rotated nodes came back *larger*
than declared. `cascac 1` matched the re-centre rule to 1px; `dsvfsb 1` (the calla lily,
~84 degrees) did not — its reported bounds put it 180px below where it renders, exactly
the "bounds lie outright" case. Its position is `locate.py`'s match (err 17.2).

**`pointer-events: none` on `.cover__layer` is load-bearing.** The lily is authored across
the "Click to open..." box and above it in the global z order, so without it the cover
cannot be opened at all — Playwright reports the img intercepting the click.

**A Figma text box shorter than its own line is a fitText trap.** `Ahmad & Salma` is 32px
type in a 27px box. Reproduced literally, `scrollHeight` exceeds `clientHeight` on a
single line and `useFitText` silently shrinks the name to 0.92. Give the rule the full
line-height and pay the 2.5px back through `top`.
