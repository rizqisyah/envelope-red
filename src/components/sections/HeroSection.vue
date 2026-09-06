<script setup lang="ts">
// Figma Frame 253 band "hero", y 0–701. Coords are band-local design px.
//
// No photo swap here. Frame 253's couple (2852:231) is a Photoroom cutout standing in
// FRONT of the white card, not a portrait sitting in an aperture — there is no hole to
// drop an API photo into, and a rectangular photo pasted over the cutout would cover
// the frame and the florals arranged around it. The gallery band is where a real
// couple's photos go.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/hero'

const { el, shown } = useReveal(0.15)
const { wedding, theme, isGroomFirst } = useWedding()

const customPhoto = computed(() => {
  return (
    wedding.value?.theme_override?.images?.foto_mempelai_setelah_buka ||
    theme.value?.theme_config?.images?.foto_mempelai_setelah_buka ||
    wedding.value?.foto_mempelai_setelah_buka ||
    wedding.value?.image_spouse
  )
})

const heroHeading = computed(() => {
  return (
    wedding.value?.theme_override?.words?.hero_title ||
    wedding.value?.theme_override?.words?.hero_heading ||
    (isGroomFirst.value ? 'Groom Bride' : 'Bride Groom')
  )
})

const skipLayers = computed(() => customPhoto.value ? ['2852:231'] : [])
</script>

<template>
  <section :ref="el" class="band hero" :class="{ 'is-in': shown }" aria-labelledby="hero-heading">
    <BandArt :layers="LAYERS" :skip="skipLayers" :shown="shown" />
    
    <div v-if="customPhoto" class="hero__photo-wrapper" :class="{ 'is-in': shown }">
      <img
        class="hero__photo"
        :src="customPhoto"
        alt="Foto mempelai"
        loading="lazy"
        decoding="async"
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

.hero__photo-wrapper {
  position: absolute;
  z-index: 71; /* Matches the white card (2896:929) so it sits behind the red frame */
  left: calc(50 * var(--px));
  top: calc(203 * var(--px));
  width: calc(268 * var(--px));
  height: calc(311 * var(--px));
  -webkit-mask-image: url('../../assets/hero/parts/2896-929.webp');
  -webkit-mask-size: 100% 100%;
  mask-image: url('../../assets/hero/parts/2896-929.webp');
  mask-size: 100% 100%;
  visibility: hidden;
  will-change: transform, opacity;
}

.hero__photo-wrapper.is-in {
  visibility: visible;
  /* Entrance animation matching the white card (index 1 in BandArt, stagger 150ms -> 440+150 = 590ms) */
  animation: hero-photo-in 2700ms cubic-bezier(0.16, 1, 0.28, 1) backwards;
  animation-delay: 590ms;
}

.hero__photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
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
  .hero__photo-wrapper,
  .hero__photo-wrapper.is-in {
    visibility: visible;
    animation: none;
    will-change: auto;
  }
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
</style>
