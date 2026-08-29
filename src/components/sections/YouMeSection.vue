<script setup lang="ts">
// Figma Frame 253 band "youme", y 5132–5281. Coords are band-local design px.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/youme'

const { el, shown } = useReveal(0.15)
const { videoPrewed } = useWedding()

const youtubeId = computed(() => {
  if (!videoPrewed.value) return null
  const match = videoPrewed.value.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^&]{11})/)
  return match ? match[1] : null
})

const skipLayers = computed(() => {
  return videoPrewed.value ? ['2883:366'] : []
})
</script>

<template>
  <section v-if="videoPrewed" :ref="el" class="band youme" :class="{ 'is-in': shown }">
    <BandArt :layers="LAYERS" :skip="skipLayers" :shown="shown" />
    
    <!-- Video Player Container (matches 2883:366) -->
    <div v-if="videoPrewed && shown" class="youme__video-container">
      <iframe
        v-if="youtubeId"
        :src="`https://www.youtube.com/embed/${youtubeId}?autoplay=1&mute=1&loop=1&playlist=${youtubeId}&controls=0`"
        frameborder="0"
        allow="autoplay; encrypted-media"
        allowfullscreen
        class="youme__video"
      ></iframe>
      <video
        v-else
        :src="videoPrewed"
        autoplay
        muted
        loop
        playsinline
        class="youme__video"
      ></video>
    </div>

    <!-- 2883:367 — Alex Brush 48/38, #a25959. The design's own line, not couple data. -->
    <p class="youme__line">You, Me &amp; Forever</p>
  </section>
</template>

<style scoped>
.youme {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.youme__video-container {
  /* Position matching layer 2883:366 */
  position: absolute;
  z-index: 185;
  left: calc(77 * var(--px));
  top: calc(34 * var(--px));
  width: calc(228 * var(--px));
  height: calc(154 * var(--px));
  border-radius: 50%;
  overflow: hidden;
  /* Add slight delay for animation if needed */
  --delay: 300ms;
}

.youme__video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  pointer-events: none; /* Prevent accidental clicks inside if it's purely decorative */
}

.youme__line {
  /*
   * 210 wide against Figma's 198, kept centred on the node's own 191. Alex Brush sets
   * "You, Me &" at 199 design px here — a pixel over the box — so the ampersand fell to
   * the second line and the render's two lines came out as "You, Me" / "& Forever".
   */
  left: calc(86 * var(--px));
  top: calc(0 * var(--px));
  width: calc(210 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(48 * var(--px));
  line-height: calc(38 * var(--px));
  color: var(--rose);
}
</style>
