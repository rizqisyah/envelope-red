<script setup lang="ts">
// Figma Frame 253 band "closing", y 7082–7631. Coords are band-local design px.
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/closing'

const { el, shown } = useReveal(0.15)

// Figma authors this break. `&#10;` in the template is folded to a space by the
// HTML parser, so the string comes from here and the box sets `white-space: pre-line`.
const LINE = 'Where \nlove becomes \nhome.'
</script>

<template>
  <section :ref="el" class="band closing" :class="{ 'is-in': shown }">
    <BandArt :layers="LAYERS" :shown="shown" />
    <!-- 2896:935 — Alex Brush 14/12. Figma authors both breaks. -->
    <p class="closing__line">{{ LINE }}</p>
  </section>
</template>

<style scoped>
.closing {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.closing__line {
  /*
   * Waits for the plaque 2894:908 it prints on: BandArt starts layer i at 440 + i*150ms
   * and the plaque is index 8, so 1640ms.
   */
  --delay: 2200ms;
  left: calc(234 * var(--px));
  top: calc(73 * var(--px));
  width: calc(59 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(14 * var(--px));
  line-height: calc(12 * var(--px));
  white-space: pre-line;
  /*
   * NOT the #ffffff the text dump reports. The render prints this line in a dusty rose
   * on a #e5e4df plaque — white would be all but invisible there — and the live shot
   * reaches full coverage on the same glyphs, so the render's darkest ink IS the fill.
   */
  color: #cfaeae;
}
</style>
