<script setup lang="ts">
// Figma Frame 253 band "invite", y 1010–1491. Coords are band-local design px.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/invite'

const { el, shown } = useReveal(0.15)
const { groom, bride, coupleNickname } = useWedding()

/*
 * 2857:227 / 2857:228 are the two-letter monogram on the oval frame — the design sets
 * "a" and "S" in two different scripts, which is why they are two nodes rather than one
 * string. They follow the couple, so they are derived rather than printed.
 */
const initials = computed(() => {
  const g = groom.value?.name || ''
  const b = bride.value?.name || ''
  /*
   * The first letter is LOWERCASED. Charoly Demo draws its lowercase as plain capitals
   * and its uppercase as swash capitals, and the design's node holds a lowercase "a" —
   * feeding it "Ahmad"[0] renders the swash instead, a letter twice the size that fills
   * the oval and buries the S behind it. The second letter stays as it comes: Figma's is
   * an uppercase S in Bibliophile Script.
   */
  if (g && b) return [g[0].toLowerCase(), b[0]]
  const parts = coupleNickname.value.split(/\s*[&+]\s*|\s+dan\s+/i)
  return parts.length > 1 ? [parts[0][0].toLowerCase(), parts[1][0]] : ['a', 'S']
})

// Figma authors this break. `&#10;` in the template is folded to a space by the
// HTML parser, so the string comes from here and the box sets `white-space: pre-line`.
const KICKER = 'Wedding\ninvitation'
</script>

<template>
  <section :ref="el" class="band invite" :class="{ 'is-in': shown }" aria-labelledby="invite-kicker">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!--
      2858:263 — Charoly Demo 24/28, #000000. Figma authors the break before "invitation".
      The inner span carries the tilt: the band's reveal animates `transform` on every
      direct child and lands on `none`, so a rotation set there would be wiped the moment
      the band arrives.
    -->
    <h2 id="invite-kicker" class="invite__kicker"><span>{{ KICKER }}</span></h2>

    <!-- 2857:227 Charoly Demo 75/38 and 2857:228 Bibliophile Script 64/38, both #702029. -->
    <p class="invite__mono invite__mono--first">{{ initials[0] }}</p>
    <p class="invite__mono invite__mono--second">{{ initials[1] }}</p>
  </section>
</template>

<style scoped>
.invite {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * NO text-transform. Charoly Demo draws its lowercase as plain capitals and its
 * uppercase as swash capitals — the render's plain "WEDDING" over a swash W is what
 * the design's mixed-case string produces.
 */
.invite__kicker {
  /*
   * Waits for the lace card it prints on. BandArt starts layer i at 440 + i*150ms;
   * 2854:627 is index 3, so 890ms, and its 2700ms ease is ~85% landed 600ms later.
   * Anything shorter and the words arrive on bare velvet before the card does.
   */
  --delay: 1500ms;
  /*
   * The quote band's swan pair (2854:637, z 65) hangs down over this card, and in the
   * design the birds sit IN FRONT of the kicker. Live copy defaults to z 900 — above
   * every plate — so this one node drops back between the lace card it prints on
   * (2854:627, z 60) and the swans.
   */
  z-index: 64;
  /*
   * The node is rotated and Figma's MCP does not report rotation, so both the angle and
   * the position are SWEPT against the render — the live shot cropped to the lace card,
   * (85,1050)-(205,1150), scored the same way as a band. Fitting the ink's principal
   * axis was tried first and answered 20.9 degrees, which is wrong: the axis of a
   * two-line block is pulled toward the block's own diagonal, not the baseline. The
   * sweep is unambiguous — 21 deg scores 22.65, 27 deg 19.72, 33 deg 18.06, 36 deg back
   * up to 20.09 — and 33 is also what the design reads as by eye.
   *
   * Its reported box (100.64, 1053.65, 123x39) is the UNROTATED one and lands nowhere
   * near the ink, so `left`/`top` are swept too rather than derived from it.
   */
  left: calc(77 * var(--px));
  top: calc(70 * var(--px));
  width: calc(123 * var(--px));
  font-family: var(--font-display);
  font-size: calc(24 * var(--px));
  font-weight: 400;
  line-height: calc(28 * var(--px));
  white-space: pre-line;
  color: #000;
}

.invite__kicker span {
  display: block;
  transform: rotate(33deg);
}

.invite__mono {
  /* Same rule against the oval frame 2856:643 — index 9, so it starts at 1790ms. */
  --delay: 2400ms;
  width: calc(82 * var(--px));
  line-height: calc(38 * var(--px));
  color: var(--wine-soft);
}

.invite__mono--first {
  left: calc(220 * var(--px));
  top: calc(259 * var(--px));
  font-family: var(--font-display);
  font-size: calc(75 * var(--px));
}

/* 2857:228 — Bibliophile Script Bold 64/38, the design's own face. */
.invite__mono--second {
  --delay: 2520ms;
  left: calc(216 * var(--px));
  top: calc(292 * var(--px));
  font-family: var(--font-monogram);
  font-weight: 700;
  font-size: calc(64 * var(--px));
}
</style>
