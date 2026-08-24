<script setup lang="ts">
// The invitation sheet: Figma Frame 253, 375 x 7979.
// One component per band of the body frame, in Figma order; each band positions its own
// children relative to its own top, so inserting a band never renumbers the others.
// Band map and asset inventory: ../../../SLICING.md
import HeroSection from '../sections/HeroSection.vue'
import QuoteSection from '../sections/QuoteSection.vue'
import InviteSection from '../sections/InviteSection.vue'
import BrideSection from '../sections/BrideSection.vue'
import GroomSection from '../sections/GroomSection.vue'
import GallerySection from '../sections/GallerySection.vue'
import TheDaySection from '../sections/TheDaySection.vue'
import AcaraSection from '../sections/AcaraSection.vue'
import YouMeSection from '../sections/YouMeSection.vue'
import GiftSection from '../sections/GiftSection.vue'
import RsvpSection from '../sections/RsvpSection.vue'
import WishSection from '../sections/WishSection.vue'
import ClosingSection from '../sections/ClosingSection.vue'
import FooterSection from '../sections/FooterSection.vue'
</script>

<template>
  <div class="sheet">
    <!--
      2854:633 — the wine plate. Flat #530915 across 383 x 3888 at y -7, so it is a
      positioned block rather than a 7762px-tall asset. z 2 in the global child order:
      above the cream ground below, under every band's art.
    -->
    <div class="sheet__wine" aria-hidden="true"></div>

    <HeroSection />
    <QuoteSection />
    <InviteSection />
    <BrideSection />
    <GroomSection />
    <GallerySection />
    <TheDaySection />
    <AcaraSection />
    <YouMeSection />
    <GiftSection />
    <RsvpSection />
    <WishSection />
    <ClosingSection />
    <FooterSection />
  </div>
</template>

<style scoped>
/*
 * One design pixel = 1cqw / 3.75, the same unit CoverSection uses. Declared once here
 * so every band inherits it and can place children in raw Figma coordinates.
 */
.sheet {
  container-type: inline-size;
  position: relative;
  /*
   * Full-bleed: the sheet fills its column edge to edge. The cap lives on
   * `.desktop-right-column` instead — capping it here would leave gutters either side
   * of the art between --card-max and the 768px breakpoint.
   */
  width: 100%;
  overflow: hidden;
  /*
   * 2852:203 — Frame 253's base plate, one flat colour across 375 x 8023, so it is this
   * background rather than a 15958px-tall asset.
   */
  background: #f7f8ee;
}

.sheet > * {
  --px: 0.26667cqw;
}

/* Bleeds 4px past each edge in Figma; full width here, which is the same result. */
.sheet__wine {
  position: absolute;
  z-index: 2;
  top: 0;
  left: 0;
  width: 100%;
  height: calc(3881 * var(--px));
  background: #530915;
}
</style>
