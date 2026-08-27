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
  if (g && b) return [g[0], b[0]]
  const parts = coupleNickname.value.split(/\s*[&+]\s*|\s+dan\s+/i)
  return parts.length > 1 ? [parts[0][0], parts[1][0]] : ['a', 'S']
})

// Figma authors this break. `&#10;` in the template is folded to a space by the
// HTML parser, so the string comes from here and the box sets `white-space: pre-line`.
const KICKER = 'Wedding\ninvitation'
</script>

<template>
  <section :ref="el" class="band invite" :class="{ 'is-in': shown }" aria-labelledby="invite-kicker">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2858:263 — Charoly Demo 24/28, #000000. Figma authors the break before "invitation". -->
    <h2 id="invite-kicker" class="invite__kicker">{{ KICKER }}</h2>

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
  --delay: 80ms;
  left: calc(101 * var(--px));
  top: calc(44 * var(--px));
  width: calc(123 * var(--px));
  font-family: var(--font-display);
  font-size: calc(24 * var(--px));
  font-weight: 400;
  line-height: calc(28 * var(--px));
  white-space: pre-line;
  color: #000;
}

.invite__mono {
  --delay: 300ms;
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
  --delay: 420ms;
  left: calc(216 * var(--px));
  top: calc(292 * var(--px));
  font-family: var(--font-monogram);
  font-weight: 700;
  font-size: calc(64 * var(--px));
}
</style>
