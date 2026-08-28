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

const step = (d: number) => {
  const n = photos.value.length
  if (n) active.value = (active.value + d + n) % n
}

/*
 * Swipe is touch only — the card is 167px wide on a phone, so arrows would cover the
 * photo. Tapping it opens the preview, which is the only way a mouse gets through.
 */
const SWIPE_PX = 30
let startX = 0
// A touch that moved far enough to count as a swipe still fires `click` afterwards.
// Without this the card would advance twice per swipe.
let swiped = false
const onStart = (e: TouchEvent) => (startX = e.touches[0].clientX)
const onEnd = (e: TouchEvent) => {
  const dx = e.changedTouches[0].clientX - startX
  swiped = Math.abs(dx) >= SWIPE_PX
  if (swiped) step(dx < 0 ? 1 : -1)
}
const onClick = () => {
  if (swiped) swiped = false
  else dlg.value?.showModal()
}

/*
 * Preview is a native <dialog>: it brings its own backdrop, top layer, Esc-to-close and
 * focus trap, so none of that is written here. Teleported to <body> because a child of
 * `.band` is absolutely positioned and faded by the shared band rules.
 */
const dlg = ref<HTMLDialogElement | null>(null)
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
    <button
      v-if="photos.length"
      type="button"
      class="gallery__photo"
      :aria-label="`Foto ${active + 1} dari ${photos.length} — ketuk untuk foto berikutnya`"
      @click="onClick"
      @touchstart.passive="onStart"
      @touchend.passive="onEnd"
    >
      <img
        :src="photos[active].src"
        :alt="photos[active].caption || 'Foto mempelai'"
        width="167"
        height="98"
        loading="lazy"
        decoding="async"
      />
    </button>

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

  <Teleport to="body">
    <dialog v-if="photos.length" ref="dlg" class="preview" @click.self="dlg?.close()">
      <img
        class="preview__img"
        :src="photos[active].src"
        :alt="photos[active].caption || 'Foto mempelai'"
        @touchstart.passive="onStart"
        @touchend.passive="onEnd"
      />
      <p v-if="photos[active].caption" class="preview__caption">{{ photos[active].caption }}</p>
      <button type="button" class="preview__close" aria-label="Tutup" @click="dlg?.close()">
        &times;
      </button>
    </dialog>
  </Teleport>
</template>

<style scoped>
.gallery {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.gallery__photo {
  /* 2875:228's own z, so the linen card's shading still paints over the photo edges. */
  z-index: 38;
  /* Waits for the linen card it is cut into: BandArt starts layer i at 440 + i*150ms
     and 2875:226 is index 2, so 740ms. */
  --delay: 1400ms;
  left: calc(104 * var(--px));
  top: calc(361 * var(--px));
  width: calc(167 * var(--px));
  height: calc(98 * var(--px));
  padding: 0;
  border: 0;
  background: none;
  cursor: pointer;
}

.gallery__photo img {
  display: block;
  width: 100%;
  height: 100%;
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

/*
 * Plain units, not `--px`: that variable is a container-query length declared on the
 * sheet element, and this dialog is teleported to <body>, outside it.
 */
.preview {
  width: 100vw;
  max-width: 100vw;
  height: 100dvh;
  max-height: 100dvh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1.5rem;
  border: 0;
  background: transparent;
}

.preview::backdrop {
  background: rgb(40 6 10 / 0.92);
}

.preview__img {
  max-width: 100%;
  max-height: 78dvh;
  object-fit: contain;
  border-radius: 4px;
}

.preview__caption {
  max-width: 100%;
  font-family: var(--font-caps);
  font-size: 0.75rem;
  text-align: center;
  color: #f2e6e6;
}

.preview__close {
  position: absolute;
  top: 0.75rem;
  right: 1rem;
  width: 2.25rem;
  height: 2.25rem;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: rgb(255 255 255 / 0.14);
  color: #fff;
  font-size: 1.375rem;
  line-height: 1;
  cursor: pointer;
}
</style>
