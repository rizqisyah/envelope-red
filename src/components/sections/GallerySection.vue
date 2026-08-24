<script setup lang="ts">
// Figma Frame 253 band "gallery", y 3143–3795. Coords are band-local design px.
//
// 2875:228 ("prewed") is the design's own couple photo, sitting in an aperture cut
// through the linen card. It is skipped whenever the API has a gallery, and the live
// photos are drawn into the same rectangle instead.
import { computed, ref, watch } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/gallery'

const { el, shown } = useReveal(0.15)
const { gallery } = useWedding()

const PLATE_PHOTO = '2875:228'
// 2875:232/233/234 — the three dots. Live state, so they are drawn rather than pasted.
const PLATE_DOTS = ['2875:232', '2875:233', '2875:234']

const photos = computed(() =>
  (gallery.value as any[])
    .map((g) => ({ src: g.image_url as string, caption: (g.caption as string) || '' }))
    .filter((p) => p.src),
)

const active = ref(0)
watch(photos, () => (active.value = 0))

const skip = computed(() =>
  photos.value.length ? [PLATE_PHOTO, ...PLATE_DOTS] : PLATE_DOTS,
)

/*
 * Frame 253 draws three dots, so the design fallback keeps three: a single dot under a
 * card that cannot be swiped reads as a rendering bug, and the row is part of the
 * design's layout. With live photos the count follows the list, capped at the five the
 * row has space for.
 */
const DESIGN_DOTS = 3
const dotCount = computed(() =>
  photos.value.length ? Math.min(photos.value.length, 5) : DESIGN_DOTS,
)

/* Touch only: the card is 167px wide on a phone, so arrows would cover the photo. */
let startX = 0
const onStart = (e: TouchEvent) => (startX = e.touches[0].clientX)
const onEnd = (e: TouchEvent) => {
  const dx = e.changedTouches[0].clientX - startX
  if (Math.abs(dx) < 30 || !photos.value.length) return
  const n = photos.value.length
  active.value = (active.value + (dx < 0 ? 1 : n - 1)) % n
}
</script>

<template>
  <section
    :ref="el"
    class="band gallery"
    :class="{ 'is-in': shown }"
    aria-labelledby="gallery-heading"
  >
    <BandArt :layers="LAYERS" :skip="skip" :shown="shown" />

    <!-- The aperture in the linen card, in band-local design px. -->
    <img
      v-if="photos.length"
      class="gallery__photo"
      :src="photos[active].src"
      :alt="photos[active].caption || 'Foto mempelai'"
      width="167"
      height="98"
      loading="lazy"
      decoding="async"
      @touchstart.passive="onStart"
      @touchend.passive="onEnd"
    />

    <!-- 2875:227 — Playfair Display SC 13/38, #000000. -->
    <p class="gallery__kicker">A glimpse of us</p>
    <!-- 2875:230 / 2875:231 — Alex Brush 64 and 55, both /38, #9a1010. -->
    <h2 id="gallery-heading" class="gallery__timeless">Timeless</h2>
    <p class="gallery__memories" aria-hidden="true">Memories</p>

    <div class="gallery__dots" role="tablist" aria-label="Foto">
      <button
        v-for="i in dotCount"
        :key="i"
        type="button"
        role="tab"
        class="gallery__dot"
        :class="{ 'is-active': i - 1 === active }"
        :aria-selected="i - 1 === active"
        :aria-label="`Foto ${i}`"
        @click="active = i - 1"
      ></button>
    </div>

    <!-- 2883:363 — Playfair Display SC 10/38, #000000. -->
    <p class="gallery__swipe">Swipe for more</p>
  </section>
</template>

<style scoped>
.gallery {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.gallery__photo {
  /* 2875:228's own z, so the linen card's shading still paints over the photo edges. */
  z-index: 38;
  left: calc(104 * var(--px));
  top: calc(361 * var(--px));
  width: calc(167 * var(--px));
  height: calc(98 * var(--px));
  object-fit: cover;
}

.gallery__kicker {
  --delay: 60ms;
  left: calc(130 * var(--px));
  top: calc(239 * var(--px));
  width: calc(115 * var(--px));
  font-family: var(--font-caps);
  font-size: calc(13 * var(--px));
  line-height: calc(38 * var(--px));
  letter-spacing: 0.06em;
  color: #000;
}

.gallery__timeless,
.gallery__memories {
  font-family: var(--font-heading);
  font-weight: 400;
  line-height: calc(38 * var(--px));
  color: var(--crimson);
}

.gallery__timeless {
  --delay: 160ms;
  left: calc(83 * var(--px));
  top: calc(336 * var(--px));
  width: calc(198 * var(--px));
  font-size: calc(64 * var(--px));
}

.gallery__memories {
  --delay: 260ms;
  left: calc(81 * var(--px));
  top: calc(445 * var(--px));
  width: calc(198 * var(--px));
  font-size: calc(55 * var(--px));
}

/* 2875:232-234: three 9px dots, 23px apart, centred on the card. */
.gallery__dots {
  --delay: 360ms;
  display: flex;
  gap: calc(14 * var(--px));
  left: calc(160 * var(--px));
  top: calc(489 * var(--px));
}

.gallery__dot {
  width: calc(9 * var(--px));
  height: calc(9 * var(--px));
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: #a9a2a2;
  cursor: pointer;
  transition: background 240ms ease, transform 240ms ease;
}

/* The design draws three identical grey dots — it has no active state to copy, so this
   is the quietest one that still reads: the same wine the band's plate is printed on. */
.gallery__dot.is-active {
  background: var(--crimson-deep);
  transform: scale(1.15);
}

.gallery__swipe {
  --delay: 420ms;
  left: calc(130 * var(--px));
  top: calc(487 * var(--px));
  width: calc(115 * var(--px));
  font-family: var(--font-caps);
  font-size: calc(10 * var(--px));
  line-height: calc(38 * var(--px));
  letter-spacing: 0.08em;
  color: #000;
}
</style>
