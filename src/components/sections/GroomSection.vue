<script setup lang="ts">
// Figma Frame 253 band "groom", y 2226–3143. Coords are band-local design px.
// The band opens with the divider between the two portraits — "And / Better together"
// belongs to this band in the Figma child order, not to bride's.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useFitLine } from '../../composables/useFitText'
import { useWedding } from '../../composables/useWedding'
import { parentLine } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/groom'
import { assets } from '../../lib/bandAssets'

const { el, shown } = useReveal(0.15)
const fitCall = useFitLine()
const fitFull = useFitLine()
const { groom, bride, isGroomFirst, parsedOverride, brideTransform, groomTransform } = useWedding()

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
const photoSrc = computed(() => {
  const custom = isGroomFirst.value
    ? (bride.value?.photo_url ||
       parsedOverride.value?.images?.foto_mempelai_wanita ||
       parsedOverride.value?.images?.foto_wanita ||
       parsedOverride.value?.images?.bride)
    : (groom.value?.photo_url ||
       parsedOverride.value?.images?.foto_mempelai_pria ||
       parsedOverride.value?.images?.foto_pria ||
       parsedOverride.value?.images?.groom)

  return custom || (isGroomFirst.value ? assets['bride/parts/2856-648.webp'] : assets['groom/parts/2858-254.webp'])
})

const layers = computed(() => {
  return LAYERS.map((l) =>
    l.id === '2858:254'
      ? {
          ...l,
          src: photoSrc.value,
          mask: assets['groom/parts/2858-254.webp'],
          objectPosition: 'center top',
          // the transform follows the person shown in this slot, not the slot
          zoom: (isGroomFirst.value ? brideTransform.value : groomTransform.value) ?? undefined,
        }
      : l,
  )
})
</script>

<template>
  <section :ref="el" class="band groom" :class="{ 'is-in': shown }" aria-labelledby="groom-name">
    <BandArt :layers="layers" :shown="shown" />

    <!-- 2858:235 — Charoly Demo 64/38, #d0cb84. -->
    <p class="groom__and">And</p>
    <!-- 2896:939 — Roben Elegante Script 20/38, #d0cb84. -->
    <p class="groom__together">Better together</p>

    <!-- One stack, for the same reason as the bride band's: a long name pushes, never overprints. -->
    <div class="band-stack groom__names">
      <!-- 2852:571 — Roben Elegante 32/38, #d0cb84. -->
      <h2 :ref="fitCall" id="groom-name" class="groom__call">{{ callName }}</h2>
      <!-- 2852:572 — Playfair Display SC 20/38, #d0cb84. -->
      <p :ref="fitFull" class="groom__full">{{ fullName }}</p>
      <!-- 2852:573 — Ovo 15/22, #d0cb84. -->
      <p class="groom__parents">{{ parents }}</p>
    </div>
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

/* Spans the frame so each node below keeps its design x as a margin-left. */
.groom__names {
  left: 0;
  top: calc(712 * var(--px));
  width: calc(375 * var(--px));
}

/*
 * 2852:571 — Roben Elegante Script 32/38, the design's own face. Widened from Figma's
 * 84..286 to 25..345 about the same centre, as in the bride band.
 */
.groom__call {
  --delay: 80ms;
  margin-left: calc(25 * var(--px));
  width: calc(320 * var(--px));
  font-family: var(--font-name);
  font-size: calc(32 * var(--px) * var(--fit, 1));
  font-weight: 400;
  line-height: calc(38 * var(--px));
  color: var(--gold-muted);
}

/* 26 + 2 x 6 = the design's 38 line box; see .bride__full. */
.groom__full {
  --delay: 200ms;
  margin-top: calc(2 * var(--px)); /* 752 - 712 - 38 */
  margin-left: calc(29 * var(--px));
  width: calc(321 * var(--px));
  padding-block: calc(6 * var(--px));
  font-family: var(--font-caps);
  font-size: calc(20 * var(--px) * var(--fit, 1));
  line-height: calc(26 * var(--px));
  color: var(--gold-muted);
}

.groom__parents {
  --delay: 320ms;
  margin-top: calc(1 * var(--px)); /* 791 - 752 - 38 */
  margin-left: calc(25 * var(--px));
  width: calc(321 * var(--px));
  font-family: var(--font-parent);
  font-size: calc(15 * var(--px));
  line-height: calc(22 * var(--px));
  white-space: pre-line;
  color: var(--gold-muted);
}
</style>
