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
import { assets } from '../../lib/bandAssets'

const { el, shown } = useReveal(0.15)
const { groom, bride, isGroomFirst } = useWedding()

const person = computed(() => (isGroomFirst.value ? bride.value : groom.value))

const fullName = computed(() => {
  if (person.value?.name?.trim()) return person.value.name.trim()
  return isGroomFirst.value ? 'Ayilhah Shella Pratni' : 'Septian Ahmad Satya'
})

const callName = computed(() => {
  if (person.value?.nickname?.trim()) return person.value.nickname.trim()
  if (person.value?.name?.trim()) return person.value.name.trim().split(' ')[0]
  return isGroomFirst.value ? 'Ayilhah' : 'Ahmad'
})

const fallbackParents = computed(() =>
  isGroomFirst.value
    ? 'Putri Pertama dari Bapak Heri\n& Ibu Sofie'
    : 'Putra Pertama dari Bapak Heri\n& Ibu Sofie',
)

const parents = computed(() => parentLine(person.value) || fallbackParents.value)

// Layer 2858:254 is the portrait photo plate in Slot 2 (w: 309, h: 247).
const layers = computed(() => {
  const photoSrc = isGroomFirst.value
    ? (bride.value?.photo_url || assets['bride/parts/2856-648.webp'])
    : (groom.value?.photo_url || assets['groom/parts/2858-254.webp'])

  return LAYERS.map((l) => (l.id === '2858:254' ? { ...l, src: photoSrc } : l))
})
</script>

<template>
  <section :ref="el" class="band groom" :class="{ 'is-in': shown }" aria-labelledby="groom-name">
    <BandArt :layers="layers" :shown="shown" />

    <!-- 2858:235 — Charoly Demo 64/38, #d0cb84. -->
    <p class="groom__and">And</p>
    <!-- 2896:939 — Roben Elegante Script 20/38, #d0cb84. -->
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

/* 2852:571 — Roben Elegante Script 32/38, the design's own face. */
.groom__call {
  --delay: 80ms;
  left: calc(84 * var(--px));
  top: calc(712 * var(--px));
  width: calc(202 * var(--px));
  font-family: var(--font-name);
  font-size: calc(32 * var(--px));
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
