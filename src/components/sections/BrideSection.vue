<script setup lang="ts">
// Figma Frame 253 band "bride", y 1491–2226. Coords are band-local design px.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { parentLine } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/bride'
import { assets } from '../../lib/bandAssets'

const { el, shown } = useReveal(0.15)
const { bride, groom, isGroomFirst, parsedOverride, brideTransform, groomTransform } = useWedding()

const person = computed(() => (isGroomFirst.value ? groom.value : bride.value))

const fullName = computed(() => {
  if (person.value?.name?.trim()) return person.value.name.trim()
  return isGroomFirst.value ? 'Septian Ahmad Satya' : 'Ayilhah Shella Pratni'
})

const callName = computed(() => {
  if (person.value?.nickname?.trim()) return person.value.nickname.trim()
  if (person.value?.name?.trim()) return person.value.name.trim().split(' ')[0]
  return isGroomFirst.value ? 'Ahmad' : 'Ayilhah'
})

const fallbackParents = computed(() =>
  isGroomFirst.value
    ? 'Putra Pertama dari Bapak Heri\n& Ibu Sofie'
    : 'Putri Pertama dari Bapak Heri\n& Ibu Sofie',
)

const parents = computed(() => parentLine(person.value) || fallbackParents.value)

// Layer 2856:648 is the portrait photo plate in Slot 1 (w: 309, h: 247).
const photoSrc = computed(() => {
  const custom = isGroomFirst.value
    ? (groom.value?.photo_url ||
       parsedOverride.value?.images?.foto_mempelai_pria ||
       parsedOverride.value?.images?.foto_pria ||
       parsedOverride.value?.images?.groom)
    : (bride.value?.photo_url ||
       parsedOverride.value?.images?.foto_mempelai_wanita ||
       parsedOverride.value?.images?.foto_wanita ||
       parsedOverride.value?.images?.bride)

  return custom || (isGroomFirst.value ? assets['groom/parts/2858-254.webp'] : assets['bride/parts/2856-648.webp'])
})

const layers = computed(() => {
  return LAYERS.map((l) =>
    l.id === '2856:648'
      ? {
          ...l,
          src: photoSrc.value,
          mask: assets['bride/parts/2856-648.webp'],
          objectPosition: 'center top',
          // the transform follows the person shown in this slot, not the slot
          zoom: (isGroomFirst.value ? groomTransform.value : brideTransform.value) ?? undefined,
        }
      : l,
  )
})
</script>

<template>
  <section :ref="el" class="band bride" :class="{ 'is-in': shown }" aria-labelledby="bride-name">
    <BandArt :layers="layers" :shown="shown" />

    <!-- 2852:245 — Roben Elegante Script 32/38, #d0cb84. -->
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

/* 2852:245 — Roben Elegante Script 32/38, the design's own face. */
.bride__call {
  --delay: 80ms;
  left: calc(83 * var(--px));
  top: calc(497 * var(--px));
  width: calc(202 * var(--px));
  font-family: var(--font-name);
  font-size: calc(32 * var(--px));
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
