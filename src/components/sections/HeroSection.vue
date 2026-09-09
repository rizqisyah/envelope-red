<script setup lang="ts">
// Figma Frame 253 band "hero", y 0–701. Coords are band-local design px.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/hero'
import maskPlate from '../../assets/hero/parts/2896-929.webp'

const { el, shown } = useReveal(0.15)
const { isGroomFirst, parsedOverride, customHeroPhoto, fotoMempelaiTransform } = useWedding()

const skipLayers = computed(() => (customHeroPhoto.value ? ['2852:231'] : []))

const heroHeading = computed(() => {
  return (
    parsedOverride.value?.words?.hero_title ||
    parsedOverride.value?.words?.hero_heading ||
    (isGroomFirst.value ? 'Groom Bride' : 'Bride Groom')
  )
})

const photoStyle = computed(() => {
  const t = fotoMempelaiTransform.value
  return {
    objectPosition: `${t.x}% ${t.y}%`,
    transformOrigin: `${t.x}% ${t.y}%`,
    transform: `scale(${t.scale})`,
  }
})

const maskStyle = computed(() => ({
  WebkitMaskImage: `url('${maskPlate}')`,
  maskImage: `url('${maskPlate}')`,
  WebkitMaskSize: '100% 100%',
  maskSize: '100% 100%',
  WebkitMaskRepeat: 'no-repeat',
  maskRepeat: 'no-repeat',
}))
</script>

<template>
  <section :ref="el" class="band hero" :class="{ 'is-in': shown }" aria-labelledby="hero-heading">
    <BandArt :layers="LAYERS" :skip="skipLayers" :shown="shown" />

    <!-- Custom Hero Photo (foto setelah buka undangan) -->
    <div
      v-if="customHeroPhoto"
      class="hero__photo-wrapper"
      :class="{ 'is-in': shown }"
      :style="maskStyle"
    >
      <img
        class="hero__photo"
        :src="customHeroPhoto"
        alt="Foto Mempelai"
        loading="eager"
        decoding="async"
        :style="photoStyle"
      />
    </div>

    <!-- 2854:620 — Charoly Demo 48/70, #d0cb84. -->
    <p class="hero__and">and</p>
    <!--
      2852:235 — BusinessPenmanshipW00-Bold 40/34, #d0cb84.
      The design's own words: the couple's names have their own bands further down, and
      this is the sheet's title, not a name slot.
    -->
    <h2 id="hero-heading" class="hero__title">{{ heroHeading }}</h2>
  </section>
</template>

<style scoped>
.hero {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * NO text-transform. Charoly Demo draws its lowercase as plain capitals and its
 * uppercase as swash capitals — the render's "AND" over a swash A is what the design's
 * lowercase string produces.
 */
.hero__and {
  --delay: 60ms;
  left: calc(154 * var(--px));
  top: calc(67 * var(--px));
  width: calc(68 * var(--px));
  font-family: var(--font-display);
  font-size: calc(48 * var(--px));
  line-height: calc(70 * var(--px));
  color: var(--gold-muted);
}

.hero__title {
  --delay: 180ms;
  left: calc(44 * var(--px));
  top: calc(125 * var(--px));
  width: calc(288 * var(--px));
  font-family: var(--font-script);
  font-size: calc(40 * var(--px));
  font-weight: 700;
  line-height: calc(34 * var(--px));
  color: var(--gold-muted);
}

.hero__photo-wrapper {
  position: absolute;
  z-index: 72;
  left: calc(50 * var(--px));
  top: calc(203 * var(--px));
  width: calc(268 * var(--px));
  height: calc(311 * var(--px));
  overflow: hidden;
  pointer-events: none;
  visibility: hidden;
  will-change: transform, opacity;
}

.hero__photo-wrapper.is-in {
  visibility: visible;
  animation: hero-photo-in 2700ms cubic-bezier(0.16, 1, 0.28, 1) backwards;
  animation-delay: 440ms;
}

.hero__photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease, object-position 0.3s ease;
}

@keyframes hero-photo-in {
  from {
    opacity: 0;
    transform: translate3d(0, calc(44 * var(--px)), 0) scale(0.86);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hero__photo-wrapper {
    visibility: visible;
    animation: none;
  }
}
</style>
