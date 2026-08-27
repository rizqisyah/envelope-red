<script setup lang="ts">
// Figma Frame 253 band "footer", y 7631–7979. Coords are band-local design px.
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/footer'

const { el, shown } = useReveal(0.15)
const { coupleNickname } = useWedding()
</script>

<template>
  <section :ref="el" class="band footer" :class="{ 'is-in': shown }" aria-labelledby="thanks">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2852:381 — Alex Brush 36/28, #9a1010. -->
    <h2 id="thanks" class="footer__thanks">Thank You !</h2>
    <!-- 2852:382 — April Signature 15/19, #7c4a15. -->
    <p class="footer__copy">
      We sincerely thank you for your presence, prayers, and blessings on our special day.
    </p>
    <!-- 2852:380 — Blosta Script 24/28, #ffe7e7. -->
    <p class="footer__couple">{{ coupleNickname }}</p>
    <!-- 2894:912 — Alex Brush 16/28, #ffffff. -->
    <p class="footer__credit">Created by @25ribuaja x Qinvi</p>
  </section>
</template>

<style scoped>
.footer {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.footer__thanks {
  --delay: 60ms;
  left: calc(107 * var(--px));
  top: calc(0 * var(--px));
  width: calc(162 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(36 * var(--px));
  font-weight: 400;
  line-height: calc(28 * var(--px));
  color: var(--crimson);
}

.footer__copy {
  --delay: 180ms;
  left: calc(97 * var(--px));
  top: calc(36 * var(--px));
  width: calc(182 * var(--px));
  font-family: var(--font-closing);
  font-size: calc(15 * var(--px));
  line-height: calc(19 * var(--px));
  color: var(--bronze);
}

.footer__couple {
  --delay: 300ms;
  left: calc(121 * var(--px));
  top: calc(134 * var(--px));
  width: calc(133 * var(--px));
  font-family: var(--font-signature);
  font-size: calc(24 * var(--px));
  line-height: calc(28 * var(--px));
  color: var(--blush);
}

.footer__credit {
  --delay: 420ms;
  left: calc(65 * var(--px));
  top: calc(324 * var(--px));
  width: calc(245 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(16 * var(--px));
  line-height: calc(28 * var(--px));
  color: #fff;
}
</style>
