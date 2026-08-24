<script setup lang="ts">
// Figma Frame 253 band "hero", y 0–701. Coords are band-local design px.
//
// No photo swap here. Frame 253's couple (2852:231) is a Photoroom cutout standing in
// FRONT of the white card, not a portrait sitting in an aperture — there is no hole to
// drop an API photo into, and a rectangular photo pasted over the cutout would cover
// the frame and the florals arranged around it. The gallery band is where a real
// couple's photos go.
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/hero'

const { el, shown } = useReveal(0.15)
</script>

<template>
  <section :ref="el" class="band hero" :class="{ 'is-in': shown }" aria-labelledby="hero-heading">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2854:620 — Charoly Demo 48/70, #d0cb84. -->
    <p class="hero__and">and</p>
    <!--
      2852:235 — BusinessPenmanshipW00-Bold 40/34, #d0cb84. SUB: Playball.
      The design's own words: the couple's names have their own bands further down, and
      this is the sheet's title, not a name slot.
    -->
    <h2 id="hero-heading" class="hero__title">Bride Groom</h2>
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
  /*
   * 48, not Figma's 40. Playball sets 1.30x NARROWER than BusinessPenmanshipW00 on this
   * string (199 design px of ink against the render's 259) but 1.33x TALLER, so matching
   * the width outright would put 36px of glyph in a 21px-tall design line. 1.2 splits it
   * — the same ratio the quote band and the cover both measured for this face pair — and
   * is what to revert to Figma's 40 if the real face is ever licensed.
   */
  font-size: calc(48 * var(--px));
  font-weight: 400;
  line-height: calc(34 * var(--px));
  color: var(--gold-muted);
}
</style>
