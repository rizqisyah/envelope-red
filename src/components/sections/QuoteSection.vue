<script setup lang="ts">
// Figma Frame 253 band "quote", y 701–1010. Coords are band-local design px.
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/quote'

const { el, shown } = useReveal(0.15)
const { quoteVerse, quoteArabic, quoteText } = useWedding()
</script>

<template>
  <section :ref="el" class="band quote" :class="{ 'is-in': shown }" aria-labelledby="quote-verse">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2852:280 — BusinessPenmanshipW00-Bold 20/48, #fffedf. -->
    <p id="quote-verse" class="quote__verse">{{ quoteVerse }}</p>
    <!--
      2852:282 — 10/14, #fffedf. ONE Figma text node holding the verse, a blank line and
      the translation. They are two fields in the API and two writing directions, so they
      are two elements here, stacked in the node's own box.
    -->
    <div class="quote__block">
      <p class="quote__arabic" dir="rtl" lang="ar">{{ quoteArabic }}</p>
      <p class="quote__translation">&ldquo;{{ quoteText }}&rdquo;</p>
    </div>
  </section>
</template>

<style scoped>
.quote {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.quote__verse {
  --delay: 120ms;
  left: calc(95 * var(--px));
  top: calc(45 * var(--px));
  width: calc(185 * var(--px));
  font-family: var(--font-script);
  font-weight: 700;
  font-size: calc(20 * var(--px));
  line-height: calc(48 * var(--px));
  color: var(--cream-text);
}

.quote__block {
  --delay: 300ms;
  display: flex;
  flex-direction: column;
  gap: calc(14 * var(--px));
  left: calc(110 * var(--px));
  top: calc(103 * var(--px));
  width: calc(155 * var(--px));
  color: var(--cream-text);
}

/*
 * `dir="rtl"` rather than trusting the bidi algorithm on a bare string, and Amiri
 * rather than the Playfair Figma reports — Playfair has no Arabic coverage at all, so
 * the design is showing Figma's own fallback, not the face the node names.
 */
.quote__arabic {
  font-family: var(--font-arabic);
  font-size: calc(10 * var(--px));
  /*
   * The node's own 14, not the 18 Amiri wants. Amiri stacks the harakat higher than the
   * face Figma fell back to, so 18 pushed the verse's three lines 12px taller and shoved
   * the translation below it down by the same amount. Overflow stays visible, so the
   * marks are tight rather than clipped — which is how the render has them.
   */
  line-height: calc(14 * var(--px));
}

.quote__translation {
  font-family: var(--font-verse);
  font-size: calc(10 * var(--px));
  line-height: calc(14 * var(--px));
}
</style>
