<script setup lang="ts">
// Figma Frame 253 band "groom", y 2226–3143. Coords are band-local design px.
// The band opens with the divider between the two portraits — "And / Better together"
// belongs to this band in the Figma child order, not to bride's.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { parentLine } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/groom'

const { el, shown } = useReveal(0.15)
const { groom } = useWedding()

const fullName = computed(() => groom.value?.name?.trim() || 'Septian Ahmad Satya')
const callName = computed(() => groom.value?.nickname?.trim() || 'Ahmad')
const parents = computed(() => parentLine(groom.value) || 'Putra Pertama dari Bapak Heri\n& Ibu Sofie')
</script>

<template>
  <section :ref="el" class="band groom" :class="{ 'is-in': shown }" aria-labelledby="groom-name">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2858:235 — Charoly Demo 64/38, #d0cb84. -->
    <p class="groom__and">And</p>
    <!-- 2896:939 — Roben Elegante 20/38, #d0cb84. SUB: Sacramento. -->
    <p class="groom__together">Better together</p>

    <!-- 2852:571 — Roben Elegante 32/38, #d0cb84. -->
    <h2 id="groom-name" class="groom__call">{{ callName }}</h2>
    <!-- 2852:572 — Playfair Display SC 20/38, #d0cb84. -->
    <p class="groom__full">{{ fullName }}</p>
    <!-- 2852:573 — Ovo 15/22, #d0cb84. -->
    <p class="groom__parents">{{ parents }}</p>
  </section>
</template>

<style scoped>
.groom {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * NO text-transform. Charoly Demo draws its lowercase as plain capitals and its
 * uppercase as swash capitals, so the design's "And" is what produces the render's
 * swash A over plain nd — uppercasing swashes every letter and they collide.
 */
.groom__and {
  --delay: 60ms;
  left: calc(74 * var(--px));
  top: calc(0 * var(--px));
  width: calc(220 * var(--px));
  font-family: var(--font-display);
  font-size: calc(64 * var(--px));
  line-height: calc(38 * var(--px));
  color: var(--gold-muted);
}

/* Figma authors this box 406 wide starting at x -112, i.e. centred on the frame. */
.groom__together {
  --delay: 180ms;
  left: calc(-112 * var(--px));
  top: calc(99 * var(--px));
  width: calc(406 * var(--px));
  font-family: var(--font-name);
  font-size: calc(20 * var(--px));
  line-height: calc(38 * var(--px));
  color: var(--gold-muted);
}

/*
 * 38, not Figma's 32. Great Vibes sets 1.7x narrower than Roben Elegante, but it is also
 * a tall connecting script where Roben Elegante is wide and short — matching the width
 * would put a 60px-tall name in a 40px gap above the full name below it. 38 closes most
 * of the gap without the collision. Revert to 32 with the real face.
 */
.groom__call {
  --delay: 80ms;
  left: calc(84 * var(--px));
  top: calc(712 * var(--px));
  width: calc(202 * var(--px));
  font-family: var(--font-name);
  font-size: calc(38 * var(--px));
  font-weight: 400;
  line-height: calc(38 * var(--px));
  color: var(--gold-muted);
}

.groom__full {
  --delay: 200ms;
  left: calc(29 * var(--px));
  top: calc(752 * var(--px));
  width: calc(321 * var(--px));
  font-family: var(--font-caps);
  font-size: calc(20 * var(--px));
  line-height: calc(38 * var(--px));
  color: var(--gold-muted);
}

.groom__parents {
  --delay: 320ms;
  left: calc(25 * var(--px));
  top: calc(791 * var(--px));
  width: calc(321 * var(--px));
  font-family: var(--font-parent);
  font-size: calc(15 * var(--px));
  line-height: calc(22 * var(--px));
  white-space: pre-line;
  color: var(--gold-muted);
}
</style>
