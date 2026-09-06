<script setup lang="ts">
// Figma Frame 253 band "closing", y 7082–7631. Coords are band-local design px.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/closing'

const { el, shown } = useReveal(0.15)
const { customSpousePhoto, spousePhotoTransform } = useWedding()

const skipLayers = computed(() => (customSpousePhoto.value ? ['2894:887'] : []))

const spousePhotoStyle = computed(() => {
  const t = spousePhotoTransform.value
  return {
    objectPosition: `${t.x}% ${t.y}%`,
    transformOrigin: `${t.x}% ${t.y}%`,
    transform: `scale(${t.scale})`,
  }
})

// Figma authors this break. `&#10;` in the template is folded to a space by the
// HTML parser, so the string comes from here and the box sets `white-space: pre-line`.
const LINE = 'Where \nlove becomes \nhome.'
</script>

<template>
  <section :ref="el" class="band closing" :class="{ 'is-in': shown }">
    <BandArt :layers="LAYERS" :skip="skipLayers" :shown="shown" />
    
    <div v-if="customSpousePhoto" class="closing__photo-wrapper" :class="{ 'is-in': shown }">
      <img
        class="closing__photo"
        :src="customSpousePhoto"
        alt="Foto Pasangan"
        loading="lazy"
        decoding="async"
        :style="spousePhotoStyle"
      />
    </div>

    <!-- 2896:935 — Alex Brush 14/12. Figma authors both breaks. -->
    <p class="closing__line">{{ LINE }}</p>
  </section>
</template>

<style scoped>
.closing {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.closing__photo-wrapper {
  position: absolute;
  z-index: 7; /* Place IN FRONT of the mirror frame (2894:886 is z: 6) */
  left: calc(102.5 * var(--px));
  top: calc(233.5 * var(--px));
  width: calc(170 * var(--px));
  height: calc(270 * var(--px));
  border-radius: 50%; /* Perfect oval */
  overflow: hidden;
  visibility: hidden;
  will-change: transform, opacity;
}

.closing__photo-wrapper.is-in {
  visibility: visible;
  /* Entrance animation perfectly in sync with the frame 2894:886 (index 1 in BandArt) 
     Delay: 440 + 1 * 150 = 590ms */
  animation: closing-photo-in 2700ms cubic-bezier(0.16, 1, 0.28, 1) backwards;
  animation-delay: 590ms;
}

.closing__photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@keyframes closing-photo-in {
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
  .closing__photo-wrapper,
  .closing__photo-wrapper.is-in {
    visibility: visible;
    animation: none;
    will-change: auto;
  }
}

.closing__line {
  /*
   * Waits for the plaque 2894:908 it prints on: BandArt starts layer i at 440 + i*150ms
   * and the plaque is index 8, so 1640ms.
   */
  --delay: 2200ms;
  left: calc(234 * var(--px));
  top: calc(73 * var(--px));
  width: calc(59 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(14 * var(--px));
  line-height: calc(12 * var(--px));
  white-space: pre-line;
  /*
   * NOT the #ffffff the text dump reports. The render prints this line in a dusty rose
   * on a #e5e4df plaque — white would be all but invisible there — and the live shot
   * reaches full coverage on the same glyphs, so the render's darkest ink IS the fill.
   */
  color: #cfaeae;
}
</style>
