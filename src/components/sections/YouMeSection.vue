<script setup lang="ts">
// Figma Frame 253 band "youme", y 5132–5281. Coords are band-local design px.
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/youme'

const { el, shown } = useReveal(0.15)
</script>

<template>
  <section :ref="el" class="band youme" :class="{ 'is-in': shown }">
    <BandArt :layers="LAYERS" :shown="shown" />
    <!-- 2883:367 — Alex Brush 48/38, #a25959. The design's own line, not couple data. -->
    <p class="youme__line">You, Me &amp; Forever</p>
  </section>
</template>

<style scoped>
.youme {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.youme__line {
  left: calc(92 * var(--px));
  top: calc(0 * var(--px));
  width: calc(198 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(48 * var(--px));
  line-height: calc(38 * var(--px));
  color: var(--rose);
}
</style>
