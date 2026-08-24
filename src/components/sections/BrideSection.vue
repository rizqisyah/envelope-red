<script setup lang="ts">
// Figma Frame 253 band "bride", y 1491–2226. Coords are band-local design px.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { parentLine } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/bride'

const { el, shown } = useReveal(0.15)
const { bride } = useWedding()

// The design prints "Ayilhah / Ayilhah Shella Pratni", so an unconfigured render matches it.
const fullName = computed(() => bride.value?.name?.trim() || 'Ayilhah Shella Pratni')
const callName = computed(() => bride.value?.nickname?.trim() || 'Ayilhah')
const parents = computed(() => parentLine(bride.value) || 'Putri Pertama dari Bapak Heri\n& Ibu Sofie')
</script>

<template>
  <section :ref="el" class="band bride" :class="{ 'is-in': shown }" aria-labelledby="bride-name">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2852:245 — Roben Elegante 32/38, #d0cb84. SUB: Sacramento. -->
    <h2 id="bride-name" class="bride__call">{{ callName }}</h2>
    <!-- 2852:246 — Playfair Display SC 20/38, #d0cb84. -->
    <p class="bride__full">{{ fullName }}</p>
    <!-- 2852:247 — Ovo 15/22, #d0cb84. Figma authors the break before "& Ibu". -->
    <p class="bride__parents">{{ parents }}</p>
  </section>
</template>

<style scoped>
.bride {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * 38, not Figma's 32. Great Vibes sets 1.7x narrower than Roben Elegante, but it is also
 * a tall connecting script where Roben Elegante is wide and short — matching the width
 * would put a 60px-tall name in a 40px gap above the full name below it. 38 closes most
 * of the gap without the collision. Revert to 32 with the real face.
 */
.bride__call {
  --delay: 80ms;
  left: calc(83 * var(--px));
  top: calc(497 * var(--px));
  width: calc(202 * var(--px));
  font-family: var(--font-name);
  font-size: calc(38 * var(--px));
  font-weight: 400;
  line-height: calc(38 * var(--px));
  color: var(--gold-muted);
}

.bride__full {
  --delay: 200ms;
  left: calc(29 * var(--px));
  top: calc(537 * var(--px));
  width: calc(321 * var(--px));
  font-family: var(--font-caps);
  font-size: calc(20 * var(--px));
  line-height: calc(38 * var(--px));
  color: var(--gold-muted);
}

/* `pre-line` carries the API's own newline, and the design fallback's, into the box. */
.bride__parents {
  --delay: 320ms;
  left: calc(25 * var(--px));
  top: calc(576 * var(--px));
  width: calc(321 * var(--px));
  font-family: var(--font-parent);
  font-size: calc(15 * var(--px));
  line-height: calc(22 * var(--px));
  white-space: pre-line;
  color: var(--gold-muted);
}
</style>
