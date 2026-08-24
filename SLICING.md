# Slicing notes — template 5

Nothing has been sliced yet. This file carries the **method** the earlier templates
arrived at, with every template-specific measurement stripped out. Fill the tables in as
the frames are cut; keep the traps — every one of them cost real time to find.

`../slicing-wedding-template-4` is the finished reference implementation. Read its
`SLICING.md` and its `src/components/sections/*.vue` when a rule here needs an example.

## What this repo already has

| Path | What it is |
|---|---|
| `src/App.vue` | Desktop split layout (left panel + 430px column), cover→body reveal |
| `src/components/cover/CoverSection.vue` | **Placeholder.** Replace with the sliced cover; keep the props and the `open` event |
| `src/components/invite/InviteBody.vue` | **Placeholder.** The sheet: declares `--px` and lists the bands |
| `src/components/invite/BandArt.vue` | Renders a `BandLayer[]` table with per-layer entrances. Design-agnostic |
| `src/lib/bandLayer.ts` / `bandAssets.ts` | The layer type, and the glob that turns `src/assets/<band>/parts/*.webp` into urls |
| `src/lib/api.ts` / `composables/useWedding.ts` | Live data + `DESIGN_MODE`. Every band's copy is data-driven |
| `src/composables/useReveal.ts` / `useFitText.ts` / `usePreloadAssets.ts` | Scroll reveal, text fitting, asset preload (glob-driven, no edit needed) |
| `src/style/tokens.css` | Colour + font tokens. **Placeholders** — resample from the design |
| `scripts/` | The slicing toolchain, below |

Dev server runs on **5178** (template-4 is on 5176) so both can run side by side.

## Fill these in first

1. The two frames (cover + body), their node ids and sizes.
2. `--body-h`, `--frame-w`, `--frame-h` in `tokens.css`.
3. The palette, sampled off the design's own text fills.
4. The font table: which family each node uses, and which are substituted.
5. `.figma-ref/frame<N>-{raw,layout,assets,zorder}.json` — dump these once and work from
   them rather than re-querying Figma.

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
BODY_FRAME=<N> BODY_H=<h> python3 scripts/gen_band.py          # every band
BODY_FRAME=<N> BODY_H=<h> python3 scripts/gen_band.py hero     # just one

npm run dev &                                                  # port 5178
node scripts/shot.mjs 5178                                     # writes .figma-tmp/web-*.png
BAND_REF=<1x body render.png> python3 scripts/band-diff.py <y0> <y1>
LOCATE_REF=<1x frame render.png> python3 scripts/locate.py <asset.webp>
```

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
render (`scripts/merge-plate.py`, `scripts/band-diff.py`), not by eye.

**A flat-colour layer defeats `locate.py`.** Cream matches cream anywhere, so a blurred
single-colour plate scores under `GOOD_ERR` a couple of hundred px from where it belongs.
Those go in `TRUST_CLIP`, which `gen_band.py` honours *before* the first `locate` hit.

**Both-edges-bleed breaks the clip rule.** The rule guesses which edge cut an export; a
node bleeding past both gets pinned to the wrong side and stacks on its own mirror. `PIN_X`.

## Fonts

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

## Deployment

`VITE_DEFAULT_SLUG` must be set per deployment — without it `src/lib/api.ts` falls back to
`demo-envelop`, which is a *different* wedding and will render the wrong couple.

## Band fidelity

Track mean abs delta per band here once the sheet is up. It is a **relative** signal across
bands, not an absolute fidelity score: it carries every deliberate deviation from the render
— substitute fonts, the live countdown where the design bakes a static plate, the live wish
list and gallery where it bakes rasters of mock content.

| band | delta | band | delta |
|---|---|---|---|
| — | — | — | — |
