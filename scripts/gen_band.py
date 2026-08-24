#!/usr/bin/env python3
"""Generate one placement table per band of the body frame.

Which frame it reads is env-driven, because every template cuts different frames:

    BODY_FRAME=244 BODY_H=9866 python3 scripts/gen_band.py

Same job the cover's `coverLayers.ts` does, done for all bands at once.
Two things make this more than a coordinate dump:

1. Figma's reported bounds and the size it actually exports disagree in both
   directions -- see "exported bounds are not node bounds" in SLICING.md. Every
   layer is reconciled per axis against the real export, then template-matched
   against the 1x frame render, and the match wins wherever it fires.

2. Bands overlap. `section` in frame<N>-zorder.json is derived from heading
   positions, so hero's art runs to y 978 while quote starts at 709. A band's
   height is therefore the distance to the NEXT band's top, not the extent of
   its own children -- children that overrun simply paint past the boundary,
   which is what the design does anyway. `z` stays the global Figma child order
   so cross-band stacking survives the split.

    python3 scripts/gen_band.py            # every band
    python3 scripts/gen_band.py hero quote # just these

Writes src/lib/bands/<section>.ts and prints a per-band summary.
"""
import hashlib
import json
import os
import pathlib
import sys

from PIL import Image

FRAME = os.environ.get("BODY_FRAME", "")
if not FRAME:
    sys.exit("set BODY_FRAME=<body frame number, e.g. 244>")

os.environ.setdefault("LOCATE_REF", f".figma-tmp/exports{FRAME}/frame{FRAME}-full.png")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import locate  # noqa: E402  -- must follow the LOCATE_REF default above

FRAME_W = int(os.environ.get("FRAME_W", "375"))
# The sheet height is the one number no default can guess -- it is per design.
FRAME_H = int(os.environ.get("BODY_H", "0"))
if not FRAME_H:
    sys.exit("set BODY_H=<body frame height in design px>")
SCALE = 2
GOOD_ERR = 40.0  # locate.py: above this an asset is not visible at that spot
# A full-width rescue is a search over the whole frame, so it will always find SOME
# least-bad spot. Overriding the clip rule on that needs locate.py's stronger bar --
# "under ~15 is a real match" -- or it moves layers the clip rule had right. At 40 it
# took hero from 4.32 to 9.20 and quote from 4.00 to 8.83.
SURE_ERR = 15.0
# A node whose reported box barely overlaps the frame is a rotated or mirrored copy whose
# bounds are fiction -- Figma still exported pixels for it, so it renders SOMEWHERE. The
# clip rule cannot help (the export was not clipped, so neither reconcile branch fires)
# and `locate` never fires either, because a hint outside the frame has nothing to match.
# Below this fraction on-frame, search the full width at the reported y instead.
ON_FRAME_MIN = 0.25
OUT_DIR = pathlib.Path("src/lib/bands")

# Rotated nodes whose reported bounds are fiction AND which no position in the frame
# matches. They are buried in the design, so drawing them anywhere paints an artifact
# the render does not have -- 2712:161 put a dark moss mound across the Wedding Gift
# heading. Every other off-frame node is merely occluded, which is not the same thing:
# dropping those wholesale took the sheet from 8.97 to 13.43 mean abs delta.
#
# Measured one at a time, not as a set. All four moss mounds share the same rotated
# 475x159.65 source (c2a52e8a), but the fourth, 2706:144, is genuinely visible:
# dropping it took akad from 7.62 to 8.58 and the sheet from 8.15 to 8.24, so it stays.
# Add to this list only with a before/after delta for that node alone.
PAINTS_NOTHING = {"2878:299", "2899:222"}  # measured one at a time; see SLICING.md

# Layers where the clip rule is right and the search is wrong. A layer buried under
# most of its band scores badly WHERE IT BELONGS, so the search wanders off to open
# ground and wins on points while being visibly wrong. 2695:182 is hero's 375x516
# backdrop: the search moved it 479px down and took hero 4.32 -> 9.20, quote
# 4.00 -> 8.83 and invite 3.97 -> 6.53 with it. Same evidence bar as PAINTS_NOTHING.
# 2699:207/208 (groom) and 2699:249/250 (bride) are the same trap in the first branch:
# four 484x175 #f3ece2 rectangles blurred to 375x375, the white haze that mutes the hedge
# behind each portrait. A cream blob matches cream anywhere, so locate.py scored under
# GOOD_ERR 200px too low and the haze landed below the hedge instead of over it -- the
# hedge rendered at full saturation and the portraits lost their halo.
# 2712:127 is akad's lone rose, the same trap: it reports 62,4189, tucked into the left
# dome cluster where 2706:155/152 cover most of it, so it scores badly WHERE IT BELONGS
# and the search moved it to 90,4345 -- bare lattice inside the arch, where the render
# shows nothing but the "Akad Nikah" backdrop. Cropping the render at both spots settles
# it: the rose is at 62,4189 and 90,4345 is empty.
TRUST_CLIP = {}  # per-design; see SLICING.md for how these are measured

# The clip rule guesses WHICH edge cut an export, and for a node that bleeds past both
# it guesses wrong. 2712:333 reports x 175 w 268 and exports 175 wide, so the rule reads
# it as right-clipped and pins it to 375-175=200 -- stacking it on top of its own mirror
# and leaving the frame's left third bare. It is the left half of the pair: the render
# has a full-height vine curtain at x 0 and locate.py picks x 0 over x 200.
# 2695:181 is hero's bush cluster, the left half of a pair sharing one 224x149 source.
# It reports x 197 and exports 197 wide -- both-edges-bleed again, so the clip rule read
# it as right-clipped and pinned it to 375-197=178, stacking it on its twin 2695:180 at
# x 176 and leaving the frame's left third bare under the urns. 197 wide means x 0.
# 2712:162 is resepsi's fountain: it reports x 310 and exports its full 249 wide, so
# neither reconcile branch fires and the fiction stands -- the fountain hangs half off
# the right edge instead of sitting centred in the pond. locate.py puts it at x 61,
# err 7.32, well inside the "under ~15 is a real match" bar.
# 2706:153 is akad's right dome rose cluster. It reports x 363 and exports its full 77
# wide -- neither reconcile branch fires -- so it hangs 12px onto the right edge while the
# render has it tucked against the dome at x 286. Same overlap trap as 2712:169: it sits
# under 2706:157 and 2706:156, so locate.py only scores 60 there and the search never
# fires. Offline composite over rows 140-360, x 230-375: 6.358 at the reported 363,
# 2.582 at 286 (measured after 2706:157's PIN_Y below, which overlaps it).
# 2877:255 / 2877:256 are the mirrored fan pair behind the "Love brought us here"
# medallion. Both report y 3348 (inside the gallery band) and export 280x280 unclipped,
# so neither reconcile branch fires and the fiction stands -- they render as a pair of
# arcs across the linen card that the design does not have. A full-frame template match
# puts them 280px higher, straddling the groom/gallery boundary: 2877:255 at 0,3068
# (err 5.56) and its mirror at 156,3068 (err 15.50), which is the pair across the frame.
# 2858:262 is the right-hand curtain of the groom band's mirrored pair. Its reported x is
# 450 -- fully off-frame -- so the off-frame rescue above fires and finds x 23, stacking
# it on top of its own mirror (2858:266, at x 0) and leaving the frame's right third bare.
# The pair meets in the middle: 375 - 264 = 111, which scores 18.11 against 26.77 at 23.
PIN_X = {"2877:255": 0, "2877:256": 156, "2858:262": 111}

# Same class of failure, but the y is wrong too, so PIN_X alone cannot fix it. Both of
# Frame 253's entries are the fan pair above -- their y is 280px out as well as their x,
# which is why neither PIN alone would do. A layer earns a place here only when a
# full-frame template match disagrees with its reported bounds AND scores low enough to
# be believed (locate.py: "under ~15 is a real match"); an occluded layer scoring badly
# where it belongs is not evidence of anything.
PIN_Y = {"2877:255": 3068, "2877:256": 3068}


def reconcile(pos, node_size, exp_size, frame_size):
    """Reconcile one axis of a Figma node against the size Figma actually exported."""
    if exp_size > node_size:
        # Export grew: a blur or a rotation widened the render bbox, and Figma
        # grows it around the node's centre, so re-centre rather than pin the corner.
        return round(pos + node_size / 2 - exp_size / 2)
    if exp_size < node_size:
        # Export shrank: Figma clipped it at the frame edge the node bleeds past.
        if pos < 0:
            return 0
        if pos + node_size > frame_size:
            return frame_size - exp_size
    return round(pos)


def _scorer(path):
    """Return (score_fn, asset_w, asset_h) for matching this asset against the render."""
    im = locate.load_asset(path)
    pts = locate.opaque_points(im, 400)
    if not pts:
        return None, 0, 0
    ref = Image.open(locate.REF).convert("RGB")
    rp = ref.load()

    def score(ox, oy):
        if ox < 0 or oy < 0 or ox + im.width > ref.width or oy + im.height > ref.height:
            return float("inf")
        return sum(
            abs(rp[x + ox, y + oy][0] - r)
            + abs(rp[x + ox, y + oy][1] - g)
            + abs(rp[x + ox, y + oy][2] - b)
            for x, y, (r, g, b) in pts
        ) / len(pts)

    return score, im.width, im.height


def rescue(path, hint_y, span=700, step=8):
    """Search the whole frame width for a layer whose reported box is off-frame.

    A node reported wholly outside the 375px frame is rotated, so its bounds are
    fiction -- but Figma still exported pixels for it, which means it renders
    SOMEWHERE. Most are mirrored decorations that land back inside the frame.
    A few are buried under later layers and never show at all; those must be
    dropped, or we paint something the design does not.

    Returns (x, y, err) for the best position within +/-span of the reported y.
    """
    score, aw, ah = _scorer(path)
    if score is None:
        return None
    ref = Image.open(locate.REF)
    im = type("S", (), {"width": aw, "height": ah})

    y_lo = max(0, hint_y - span)
    y_hi = min(ref.height - im.height, hint_y + span)
    x_hi = ref.width - im.width
    if y_hi < y_lo or x_hi < 0:
        return None
    best = min(
        (score(ox, oy), ox, oy)
        for oy in range(y_lo, y_hi + 1, step)
        for ox in range(0, x_hi + 1, step)
    )
    err, bx, by = best
    for oy in range(max(y_lo, by - step), min(y_hi, by + step) + 1):
        for ox in range(max(0, bx - step), min(x_hi, bx + step) + 1):
            sc = score(ox, oy)
            if sc < err:
                err, bx, by = sc, ox, oy
    return bx, by, err


def band_tops(children):
    """Band top = its first child's y; band height runs to the next band's top."""
    firsts = {}
    for c in children:
        s = c["section"]
        firsts[s] = min(firsts.get(s, c["y"]), c["y"])
    ordered = sorted(firsts.items(), key=lambda kv: kv[1])
    # The sheet must start at the frame's top edge. The first band's first child can sit
    # below y0 (Frame 253's does, at 67), and honouring that would open a gap above the
    # first band that the design does not have.
    if ordered:
        ordered[0] = (ordered[0][0], 0)
    # Round the tops FIRST, then derive each height from the next rounded top. Rounding
    # top and height independently leaves a 1px seam between bands wherever both round
    # the same way, and the sheet ends up short of FRAME_H.
    ordered = [(name, round(top)) for name, top in ordered]
    spans = {}
    for i, (name, top) in enumerate(ordered):
        nxt = ordered[i + 1][1] if i + 1 < len(ordered) else FRAME_H
        spans[name] = (top, nxt - top)
    return spans, [name for name, _ in ordered]


def main():
    # scripts/solve_alpha.py's output: the opacity Figma's MCP never reports, and the
    # residual offset the clip/re-centre/locate chain could not reach. Both are optional
    # -- an unsolved frame just generates at full opacity and no nudge.
    alpha_path = pathlib.Path(f".figma-ref/frame{FRAME}-alpha.json")
    place_path = pathlib.Path(f".figma-ref/frame{FRAME}-place.json")
    blend_path = pathlib.Path(f".figma-ref/frame{FRAME}-blend.json")
    ALPHA = json.load(alpha_path.open()) if alpha_path.exists() else {}
    PLACE = json.load(place_path.open()) if place_path.exists() else {}
    BLEND = json.load(blend_path.open()) if blend_path.exists() else {}

    zorder = json.load(open(f".figma-ref/frame{FRAME}-zorder.json"))
    children = zorder["children"] if isinstance(zorder, dict) else zorder
    assets = json.load(open(f".figma-ref/frame{FRAME}-assets.json"))["nodes"]

    # A sprite used by more than one node cannot be template-matched: every copy scores
    # the same at every other copy's slot, and `locate` happily reports card 1's plate at
    # card 2's position. The gift band's three identical account plates lost their first
    # card entirely to this. Their reported bounds are already right -- trust them.
    # Keyed on the file's BYTES, not its path: Figma exports each node separately, so the
    # gift band's three identical plates are three different .webp files with identical
    # content. Hashing is what actually finds them.
    used = {}
    for nid, a in assets.items():
        f = pathlib.Path("src/assets/" + a["asset"])
        if f.exists():
            used.setdefault(hashlib.md5(f.read_bytes()).hexdigest(), []).append(nid)
    twins = {nid for ids in used.values() if len(ids) > 1 for nid in ids}

    spans, order = band_tops(children)
    wanted = sys.argv[1:] or order
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for name in wanted:
        if name not in spans:
            print(f"!! no such band: {name}")
            continue
        top, height = spans[name]
        rows, matched, dropped = [], 0, []

        for c in children:
            if c["section"] != name:
                continue
            if c["id"] in PAINTS_NOTHING:
                dropped.append(f"{c['id']} (z{c['z']}, buried in the design)")
                continue
            a = assets.get(c["id"])
            if not a:
                continue  # TEXT, dropped empty, or a group we walked into
            path = f"src/assets/{a['asset']}"
            if not pathlib.Path(path).exists():
                print(f"!! missing asset for {c['id']}: {path}")
                continue
            im = Image.open(path)
            scale = a.get("assetScale", SCALE)
            w, h = im.width // scale, im.height // scale

            # Fraction of the NODE that overlaps the frame -- against c["w"], never the
            # export width. A blurred or rotated node exports far wider than it claims,
            # and dividing by that understated every such node into a false rescue: the
            # gift band went 5.4 -> 25.3 the one time this read `w`.
            on_frame = max(0.0, min(c["x"] + c["w"], FRAME_W) - max(c["x"], 0)) / max(1.0, c["w"])
            found, err = (None, None)
            if c["id"] not in twins:
                found, err = locate.locate(path, max(0, round(c["x"])), max(0, round(c["y"])))
            if found and found[4] < GOOD_ERR and c["id"] not in TRUST_CLIP:
                x, y = found[0], found[1]
                matched += 1
            elif on_frame < ON_FRAME_MIN and c["id"] not in TRUST_CLIP and c["id"] not in twins:
                # Taken unconditionally, unlike the rescue below: where the reported box
                # puts this layer it is invisible, so ANY match inside the frame is better
                # evidence than bounds that place it off the edge. The error is still
                # meaningless on an occluded layer -- the groom arch's floral scores 78
                # where it belongs, the same as its visible twin in the bride band.
                hit = rescue(path, max(0, round(c["y"])), span=60, step=4)
                if hit:
                    x, y = hit[0], hit[1]
                    matched += 1
                else:
                    x = reconcile(c["x"], c["w"], w, FRAME_W)
                    y = reconcile(c["y"], c["h"], h, FRAME_H)
            elif w < round(c["w"]) or h < round(c["h"]):
                # Figma clipped this export, which means the node bleeds off an edge --
                # and a bleeding node in this file is usually a rotated one, whose
                # reported position is fiction. The clip rule can only guess which edge
                # cut it; the render knows. 2699:284 sat 202px low until this ran.
                cx = reconcile(c["x"], c["w"], w, FRAME_W)
                cy = reconcile(c["y"], c["h"], h, FRAME_H)
                hit = rescue(path, max(0, round(c["y"])))
                score, _, _ = _scorer(path)
                clip_err = score(cx, cy) if score else float("inf")
                # A full-width search always finds SOME least-bad spot, and for a big
                # mostly-transparent layer that spot is often nowhere near the truth.
                # It has to beat where the clip rule already put it, clearly.
                if (
                    hit
                    and c["id"] not in TRUST_CLIP
                    and hit[2] < SURE_ERR
                    and hit[2] < clip_err - 3
                ):
                    x, y = hit[0], hit[1]
                    matched += 1
                else:
                    # A high error here means occluded OR absent -- locate.py cannot tell
                    # them apart, and guessing "absent" and dropping the layer measurably
                    # hurt the render. Fall through to the clip rule; only the layers in
                    # PAINTS_NOTHING below are actually dropped.
                    x = reconcile(c["x"], c["w"], w, FRAME_W)
                    y = reconcile(c["y"], c["h"], h, FRAME_H)
            else:
                x = reconcile(c["x"], c["w"], w, FRAME_W)
                y = reconcile(c["y"], c["h"], h, FRAME_H)
            x, y = PLACE.get(c["id"], (x, y))
            # PIN_X/PIN_Y last: they are hand-measured against the render, so they beat
            # both the reconcile chain and the solver's own search.
            x = PIN_X.get(c["id"], x)
            y = PIN_Y.get(c["id"], y)
            rows.append((c["z"], c["id"], a["asset"], x, y - top, w, h,
                         ALPHA.get(c["id"], 1.0), BLEND.get(c["id"], "normal")))

        rows.sort(key=lambda r: r[0])
        if not rows:
            # A text-only band (invite, divider) has no placement table to generate;
            # an empty module would just be an unused import.
            print(f"{name:10} y {top:5}..{top + height:5} h {height:5}  text-only, no table")
            (OUT_DIR / f"{name}.ts").unlink(missing_ok=True)
            continue
        body = f"""// Generated by scripts/gen_band.py — do not hand-edit.
// Figma Frame {FRAME} band "{name}": y {top}..{top + height}, height {height} design px.
// x/y are band-local design px; `z` is the GLOBAL Figma child order, so layers still
// stack correctly against the bands above and below this one.
//
// Positions are NOT Figma's reported bounds — see "exported bounds are not node bounds"
// in SLICING.md. Regenerate rather than nudging numbers by hand.
import type {{ BandLayer }} from '../bandLayer'

export const BAND_TOP = {top}
export const BAND_HEIGHT = {height}

export const LAYERS: BandLayer[] = [
"""
        for z, nid, asset, x, y, w, h, alpha, mode in rows:
            extra = "" if alpha == 1.0 else f", a: {alpha}"
            extra += "" if mode == "normal" else f", b: '{mode}'"
            body += (
                f"  {{ z: {z}, id: '{nid}', src: assets['{asset}'],"
                f" x: {x}, y: {y}, w: {w}, h: {h}{extra} }},\n"
            )
        body += "]\n"

        header = """import { assets } from '../bandAssets'

"""
        (OUT_DIR / f"{name}.ts").write_text(header + body)
        print(f"{name:10} y {top:5}..{top + height:5} h {height:5}  {len(rows):3} layers  {matched:3} matched")
        for d in dropped:
            print(f"           dropped: {d}")


if __name__ == "__main__":
    main()
