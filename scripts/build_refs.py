#!/usr/bin/env python3
"""Turn the raw Figma dump of the body frame into the two files gen_band.py reads.

Flattens the node tree to leaves in global paint order, assigns each one a band, and
converts every exported PNG to webp under src/assets/<band>/parts/.

Two things about the flatten are easy to get wrong and both were bugs first:

- Figma's `children` are BOTTOM-FIRST, so a depth-first walk over them is already the
  global paint order. `z` is just the index.
- A GROUP's children report ABSOLUTE (frame-local) coordinates; a FRAME's children report
  coordinates relative to that frame. Only the FRAME case needs the parent offset added.

Band assignment is a y-range table, because Figma has no section marker to read. It is a
HINT -- gen_band.py derives each band's real top from the nodes assigned to it, and a
layer that renders outside its band still lands in the right place, since positions are
absolute within the sheet and no section clips.

    python3 scripts/build_refs.py

Reads .figma-tmp/frame253-flat.json (the flattened dump) and .figma-tmp/parts253/*.png
(one export per node, scale 2). Re-dump those from Figma if the design changes.
"""
import json, os, subprocess
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

FLAT = json.load(open('.figma-tmp/frame253-flat.json'))

# Band tops, in design px. A node lands in the last band whose top is <= its y.
BANDS = [
    ('hero', 0), ('quote', 700), ('invite', 1000), ('bride', 1450), ('groom', 2200),
    ('gallery', 3140), ('theday', 3790), ('acara', 4260), ('youme', 5100),
    ('gift', 5280), ('rsvp', 6020), ('wish', 6410), ('closing', 7080), ('footer', 7600),
]

# The two full-sheet plates are flat colour and 8000px tall — CSS on the sheet, not images.
SHEET_PLATES = {'2852:203', '2854:633'}
# Exports that came back fully transparent.
EMPTY = {'2852:220', '2852:222', '2852:229', '2852:230', '2852:244', '2858:256'}

def section(y):
    name = BANDS[0][0]
    for n, top in BANDS:
        if y >= top:
            name = n
    return name

zorder, nodes = [], {}
for f in FLAT:
    if f['id'] in SHEET_PLATES or f['id'] in EMPTY:
        continue
    sec = section(f['y'])
    row = dict(z=f['z'], id=f['id'], name=f['name'], type=f['type'],
               x=f['x'], y=f['y'], w=f['w'], h=f['h'], section=sec)
    zorder.append(row)
    # TEXT_PATH is lettering bent along a curve — "Love brought us here", "just us!".
    # Nothing in CSS reproduces that, and neither is data-driven, so both ship as art.
    if f['type'] == 'TEXT':
        continue
    src = f".figma-tmp/parts253/{f['id'].replace(':', '-')}.png"
    if not os.path.exists(src):
        print('!! missing export', f['id']); continue
    out_dir = f"src/assets/{sec}/parts"
    os.makedirs(out_dir, exist_ok=True)
    out = f"{out_dir}/{f['id'].replace(':', '-')}.webp"
    subprocess.run(['cwebp', '-quiet', '-q', '88', '-alpha_q', '100', src, '-o', out], check=True)
    nodes[f['id']] = dict(asset=f"{sec}/parts/{f['id'].replace(':', '-')}.webp",
                          figmaName=f['name'], x=f['x'], y=f['y'], w=f['w'], h=f['h'])

json.dump({'frame': '2852:202', 'height': 7979, 'children': zorder},
          open('.figma-ref/frame253-zorder.json', 'w'), indent=1)
json.dump({'frame': '2852:202', 'scale': 2, 'assetDir': 'src/assets/', 'nodes': nodes},
          open('.figma-ref/frame253-assets.json', 'w'), indent=1)

from collections import Counter
c = Counter(r['section'] for r in zorder)
ca = Counter(nodes[i]['asset'].split('/')[0] for i in nodes)
for n, _ in BANDS:
    print(f"{n:9} nodes={c[n]:3}  assets={ca[n]:3}")
print('total assets', len(nodes))
