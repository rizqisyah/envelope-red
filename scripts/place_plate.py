#!/usr/bin/env python3
"""Find where ONE layer belongs when it is far from where the tables put it.

solve_alpha.py refines a layer inside a +/-40px window, which is the right window for a
layer the clip rule nearly had. It is useless for the class of layer this file exists
for: a rotated or off-frame node whose reported bounds are outright fiction, sitting
hundreds of pixels from its true home. locate.py cannot help either -- it matches raw
RGB, so a plate authored to be SCREENED (a light leak, a lace overlay) has nothing to
lock onto, and every such plate scores over 80 wherever you put it.

The fix is to search wide under the SAME compositing model solve_alpha scores with:
every other layer painted at its solved opacity and blend mode, the CSS ground plates
underneath, live copy masked out, and the candidate composited through its own trial
alpha and blend. Then a plate that only makes sense screened is scored screened.

    BODY_FRAME=253 BODY_H=7979 python3 scripts/place_plate.py 2877:263 2894:882

Prints the best (x, y, alpha, mode) per node with its score against the score where the
table has it now. Nothing is written -- put what it finds in gen_band.py's PIN_X/PIN_Y
(and NO_SOLVE, so the refiner does not walk it back) once you have looked at the crop.

Y_SPAN bounds the vertical search around the layer's own band; widen it for a node that
has no business being in the band Figma filed it under.
"""
import os
import sys

from PIL import Image, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solve_alpha as S  # noqa: E402  -- reuses its ground, mask, blend and paste

Image.MAX_IMAGE_PIXELS = None

# How far above and below the layer's own band to look. The plates this is for are
# filed one band away from where they paint, not across the whole sheet.
Y_SPAN = int(os.environ.get("Y_SPAN", "900"))
# Coarse pass, then two refinements. The coarse step has to be smaller than the smallest
# feature that identifies the plate, or the search steps straight over the true minimum.
STEPS = (8, 2, 1)


def main():
    ref = Image.open(S.REF).convert("RGB")
    alphas = S.json.load(open(S.ALPHA_FILE)) if os.path.exists(S.ALPHA_FILE) else {}
    blends = S.json.load(open(S.BLEND_FILE)) if os.path.exists(S.BLEND_FILE) else {}
    spans = S.band_spans()
    layers = S.all_layers()
    by_id = {r["id"]: r for r in layers}

    # gen_band.py's PAINTS_NOTHING drops a layer from the tables outright, and two of
    # this frame's entries turn out to be the acara band's missing oval-and-pearls -- they
    # measured as invisible only because they were measured where their fictional bounds
    # put them. So fall back to the raw node records, which is exactly the case this
    # script is for.
    zorder = {c["id"]: c for c in
              S.json.load(open(f".figma-ref/frame{S.FRAME}-zorder.json"))["children"]}
    assets = S.json.load(open(f".figma-ref/frame{S.FRAME}-assets.json"))["nodes"]

    for nid in sys.argv[1:]:
        row = by_id.get(nid)
        if not row and nid in zorder and nid in assets:
            c = zorder[nid]
            row = dict(id=nid, asset=assets[nid]["asset"], band=c["section"],
                       x=round(c["x"]), y=round(c["y"]), w=c["w"], h=c["h"])
            print(f"({nid} is not in any band table -- scored from its raw node record)")
        if not row:
            print(f"!! {nid} is in no band table and has no exported asset")
            continue
        band_top, band_h = spans[row["band"]]
        y0 = max(0, band_top - Y_SPAN)
        y1 = min(S.FRAME_H, band_top + band_h + Y_SPAN)
        target = ref.crop((0, y0, S.FRAME_W, y1))
        mask = S.text_mask(y0, y1)
        ground = S.ground_for(y0, y1)
        im = S.load("src/assets/" + row["asset"])

        # Everything else that reaches this window, painted where it currently sits.
        others = [r for r in layers if r["id"] != nid and r["y"] < y1 and r["y"] + r["h"] > y0]
        base = ground.copy()
        for r in others:
            S.paste(base, S.load("src/assets/" + r["asset"]), r["x"], r["y"] - y0,
                    alphas.get(r["id"], 1.0), blends.get(r["id"], "normal"))

        # A candidate pushed off the edge is scored over a sliver of flat ground and wins
        # on points with a perfect 0.000 -- the first run of this put the lace panel at
        # x -286, 20px of it on the frame. The score is a MEAN, so a small window is not
        # self-penalising; the coverage floor is what rules those out.
        MIN_COVER = 0.6
        area = im.width * im.height

        def delta(box):
            """Mean abs delta of `base` against the render over `box`, text masked out."""
            bx0, by0, bx1, by1 = box
            d = ImageChops.difference(target.crop(box), base.crop(box).convert("RGB")).convert("L")
            d.paste(0, (0, 0), mask.crop(box))
            return sum(i * n for i, n in enumerate(d.histogram())) / ((bx1 - bx0) * (by1 - by0))

        def score(x, y, a, mode):
            """How much this layer IMPROVES the composite where it lands. Lower is better.

            Not the absolute error under the layer: that is minimised by parking a plate
            on ground the rest of the band already renders correctly and fading it to
            nothing, which is exactly what the first cut of this returned for all three
            light-leak plates -- 'a0.12 lighten' on empty cream, scoring 0.14. Measuring
            the layer's own contribution instead means an invisible layer scores 0 by
            construction and cannot win, and a layer is only credited where it actually
            explains something the render has and the composite does not.
            """
            bx0, by0 = max(0, x), max(0, y - y0)
            bx1 = min(S.FRAME_W, x + im.width)
            by1 = min(y1 - y0, y - y0 + im.height)
            if bx1 <= bx0 or by1 <= by0:
                return 0.0
            if (bx1 - bx0) * (by1 - by0) < MIN_COVER * area:
                return 0.0
            box = (bx0, by0, bx1, by1)
            canvas = base.crop(box)
            S.paste(canvas, im, x - bx0, y - y0 - by0, a, mode)
            d = ImageChops.difference(target.crop(box), canvas.convert("RGB")).convert("L")
            d.paste(0, (0, 0), mask.crop(box))
            with_it = sum(i * n for i, n in enumerate(d.histogram())) / ((bx1 - bx0) * (by1 - by0))
            return with_it - delta(box)

        now = (row["x"], row["y"], alphas.get(nid, 1.0), blends.get(nid, "normal"))
        best = [score(*now), *now]

        def sweep(xs, ys, a, mode):
            for y in ys:
                for x in xs:
                    s = score(x, y, a, mode)
                    if s < best[0]:
                        best[0], best[1], best[2], best[3], best[4] = s, x, y, a, mode

        # Position first at the paint the tables already hold, then paint at the position
        # that found, then position again. Searching every (x, y, alpha, mode) jointly is
        # the honest formulation and about 40x too slow to run -- and the plates this is
        # for are identified by their SHAPE, which the wrong alpha dims but does not move.
        for n, step in enumerate(STEPS):
            if n == 0:
                xs = range(-im.width + 20, S.FRAME_W - 20, step)
                ys = range(y0, y1 - 20, step)
                # A near-invisible starting alpha makes every position score the same, so
                # the coarse pass runs at full strength whatever the table says.
                sweep(xs, ys, max(now[2], 0.55), now[3])
                sweep(xs, ys, 1.0, "screen")
            else:
                span = STEPS[n - 1] * 3
                xs = range(best[1] - span, best[1] + span + 1, step)
                ys = range(best[2] - span, best[2] + span + 1, step)
                for mode in S.MODES:
                    for a in S.LADDER:
                        if a > 0.0:
                            sweep(xs, ys, a, mode)
        print(f"{nid:12} now  {now[0]},{now[1]} a{now[2]} {now[3]:8} gain {score(*now):+.3f}")
        print(f"{'':12} best {best[1]},{best[2]} a{best[3]} {best[4]:8} gain {best[0]:+.3f}")


main()
