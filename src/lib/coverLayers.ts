// Generated — do not hand-edit. Figma Frame 254 (2852:577), 375 x 725.
// `z` is Figma child order, which IS the paint order, and the text nodes in
// CoverSection.vue carry their own slots in the same sequence (5..10).
//
// x/y/w/h are NOT Figma's reported bounds for the two rotated nodes. Figma reports a
// rotated node's unrotated box and exports its AABB, so both numbers disagree with the
// render. `2913:3757` matches the re-centre rule; `2854:615` does not — its reported
// bounds lie outright and its position is the template match against
// .figma-tmp/frame254-1x.png (scripts/locate.py, err 17.2).
//
// Four of the frame's eight non-text children are dropped — see
// .figma-ref/frame254-assets.json `dropped` for why.
const modules = import.meta.glob('../assets/opening/parts/*.webp', {
  eager: true,
  import: 'default',
}) as Record<string, string>

const parts = Object.fromEntries(
  Object.entries(modules).map(([path, url]) => [path.split('/').pop()!.replace('.webp', ''), url]),
) as Record<string, string>

export type CoverLayer = {
  z: number
  id: string
  src: string
  x: number
  y: number
  w: number
  h: number
}

export const COVER_LAYERS: CoverLayer[] = [
  { z: 3, id: '2854:610', src: parts['2854-610'], x: 47, y: 222, w: 295, h: 196 },
  { z: 11, id: '2854:614', src: parts['2854-614'], x: 163, y: 332, w: 64, h: 64 },
  { z: 12, id: '2854:615', src: parts['2854-615'], x: 59, y: 344, w: 259, h: 163 },
  { z: 13, id: '2913:3757', src: parts['2913-3757'], x: 153, y: 81, w: 69, h: 68 },
]
