<script setup lang="ts">
// Figma Frame 253 band "invite", y 1010–1491. Coords are band-local design px.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/invite'
import { assets } from '../../lib/bandAssets'

const { el, shown } = useReveal(0.15)
const { groom, bride, isGroomFirst, coupleNickname, logoMempelai, gallery } = useWedding()

/*
 * 2857:227 / 2857:228 are the two-letter monogram on the oval frame — the design sets
 * "a" and "S" in two different scripts, which is why they are two nodes rather than one
 * string. They follow the couple, so they are derived rather than printed.
 */
const initials = computed(() => {
  const g = (groom.value?.nickname || groom.value?.name || '').trim()
  const b = (bride.value?.nickname || bride.value?.name || '').trim()
  if (g && b) {
    return isGroomFirst.value
      ? [g[0].toLowerCase(), b[0].toUpperCase()]
      : [b[0].toLowerCase(), g[0].toUpperCase()]
  }
  const parts = coupleNickname.value.split(/\s*[&+]\s*|\s+dan\s+/i)
  return parts.length > 1 ? [parts[0][0].toLowerCase(), parts[1][0].toUpperCase()] : ['a', 'S']
})

const customLogo = computed(() => logoMempelai.value)
const firstGalleryPhoto = computed(() => {
  const arr = gallery.value as any[]
  return (arr && arr.length > 0) ? arr[0].image_url : null
})
const secondGalleryPhoto = computed(() => {
  const arr = gallery.value as any[]
  return (arr && arr.length > 1) ? arr[1].image_url : null
})

const skipLayers = computed(() => {
  const skip = []
  if (customLogo.value) skip.push('2856:645')
  if (firstGalleryPhoto.value) skip.push('2858:249')
  if (secondGalleryPhoto.value) skip.push('2858:245')
  return skip
})

// Figma authors this break. `&#10;` in the template is folded to a space by the
// HTML parser, so the string comes from here and the box sets `white-space: pre-line`.
const KICKER = 'Wedding\ninvitation'
</script>

<template>
  <section :ref="el" class="band invite" :class="{ 'is-in': shown }" aria-labelledby="invite-kicker">
    <BandArt :layers="LAYERS" :skip="skipLayers" :shown="shown" />

    <div v-if="customLogo" class="invite__logo-wrapper" :class="{ 'is-in': shown }">
      <img
        class="invite__logo"
        :src="customLogo"
        alt="Logo Mempelai"
        loading="lazy"
        decoding="async"
      />
    </div>

    <div v-if="firstGalleryPhoto" class="invite__polaroid-wrapper" :class="{ 'is-in': shown }">
      <img
        class="invite__polaroid"
        :src="firstGalleryPhoto"
        alt="Foto Pasangan 1"
        loading="lazy"
        decoding="async"
        :style="{
          maskImage: `url(${assets['invite/parts/2858-249.webp']})`,
          WebkitMaskImage: `url(${assets['invite/parts/2858-249.webp']})`,
          maskSize: '100% 100%',
          WebkitMaskSize: '100% 100%'
        }"
      />
    </div>

    <div v-if="secondGalleryPhoto" class="invite__polaroid-wrapper-2" :class="{ 'is-in': shown }">
      <img
        class="invite__polaroid-2"
        :src="secondGalleryPhoto"
        alt="Foto Pasangan 2"
        loading="lazy"
        decoding="async"
        :style="{
          maskImage: `url(${assets['invite/parts/2858-245.webp']})`,
          WebkitMaskImage: `url(${assets['invite/parts/2858-245.webp']})`,
          maskSize: '100% 100%',
          WebkitMaskSize: '100% 100%'
        }"
      />
    </div>

    <!--
      2858:263 — Charoly Demo 24/28, #000000. Figma authors the break before "invitation".
      The inner span carries the tilt: the band's reveal animates `transform` on every
      direct child and lands on `none`, so a rotation set there would be wiped the moment
      the band arrives.
    -->
    <h2 id="invite-kicker" class="invite__kicker"><span>{{ KICKER }}</span></h2>

    <!-- 2857:227 Charoly Demo 75/38 and 2857:228 Bibliophile Script 64/38, both #702029. -->
    <template v-if="!customLogo">
      <p class="invite__mono invite__mono--first">{{ initials[0] }}</p>
      <p class="invite__mono invite__mono--second">{{ initials[1] }}</p>
    </template>
  </section>
</template>

<style scoped>
.invite {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.invite__logo-wrapper {
  position: absolute;
  z-index: 113; /* BEHIND the oval frame (2856:643 is 114) so the frame edges frame it nicely, but IN FRONT of the cream lace card (58) */
  left: calc(179 * var(--px));
  top: calc(194 * var(--px));
  width: calc(171 * var(--px));
  height: calc(201 * var(--px));
  border-radius: 50%;
  visibility: hidden;
  will-change: transform, opacity;
}

.invite__logo-wrapper.is-in {
  visibility: visible;
  /* Syncs with frame 2856:643 (index 9 in BandArt) -> 440 + 9*150 = 1790ms */
  animation: invite-item-in 2700ms cubic-bezier(0.16, 1, 0.28, 1) backwards;
  animation-delay: 1790ms;
}

.invite__logo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain; /* Keeps the logo elegant without stretching */
}

.invite__polaroid-wrapper {
  position: absolute;
  z-index: 62; /* Replacing 2858:249 which is index 5 */
  left: calc(102 * var(--px));
  top: calc(264 * var(--px));
  width: calc(81 * var(--px));
  height: calc(97 * var(--px));
  visibility: hidden;
  will-change: transform, opacity;
}

.invite__polaroid-wrapper.is-in {
  visibility: visible;
  /* Syncs with index 5 -> 440 + 5*150 = 1190ms */
  animation: invite-item-in 2700ms cubic-bezier(0.16, 1, 0.28, 1) backwards;
  animation-delay: 1190ms;
}

.invite__polaroid {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.invite__polaroid-wrapper-2 {
  position: absolute;
  z-index: 67; /* Replacing 2858:245 which is index 7 */
  left: calc(240 * var(--px));
  top: calc(129 * var(--px));
  width: calc(76 * var(--px));
  height: calc(93 * var(--px));
  visibility: hidden;
  will-change: transform, opacity;
}

.invite__polaroid-wrapper-2.is-in {
  visibility: visible;
  /* Syncs with index 7 -> 440 + 7*150 = 1490ms */
  animation: invite-item-in 2700ms cubic-bezier(0.16, 1, 0.28, 1) backwards;
  animation-delay: 1490ms;
}

.invite__polaroid-2 {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@keyframes invite-item-in {
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
  .invite__logo-wrapper,
  .invite__logo-wrapper.is-in,
  .invite__polaroid-wrapper,
  .invite__polaroid-wrapper.is-in,
  .invite__polaroid-wrapper-2,
  .invite__polaroid-wrapper-2.is-in {
    visibility: visible;
    animation: none;
    will-change: auto;
  }
}

/*
 * NO text-transform. Charoly Demo draws its lowercase as plain capitals and its
 * uppercase as swash capitals — the render's plain "WEDDING" over a swash W is what
 * the design's mixed-case string produces.
 */
.invite__kicker {
  /*
   * Waits for the lace card it prints on. BandArt starts layer i at 440 + i*150ms;
   * 2854:627 is index 3, so 890ms, and its 2700ms ease is ~85% landed 600ms later.
   * Anything shorter and the words arrive on bare velvet before the card does.
   */
  --delay: 1500ms;
  /*
   * The quote band's swan pair (2854:637, z 65) hangs down over this card, and in the
   * design the birds sit IN FRONT of the kicker. Live copy defaults to z 900 — above
   * every plate — so this one node drops back between the lace card it prints on
   * (2854:627, z 60) and the swans.
   */
  z-index: 64;
  /*
   * The node is rotated and Figma's MCP does not report rotation, so both the angle and
   * the position are SWEPT against the render — the live shot cropped to the lace card,
   * (85,1050)-(205,1150), scored the same way as a band. Fitting the ink's principal
   * axis was tried first and answered 20.9 degrees, which is wrong: the axis of a
   * two-line block is pulled toward the block's own diagonal, not the baseline. The
   * sweep is unambiguous — 21 deg scores 22.65, 27 deg 19.72, 33 deg 18.06, 36 deg back
   * up to 20.09 — and 33 is also what the design reads as by eye.
   *
   * Its reported box (100.64, 1053.65, 123x39) is the UNROTATED one and lands nowhere
   * near the ink, so `left`/`top` are swept too rather than derived from it.
   */
  left: calc(77 * var(--px));
  top: calc(70 * var(--px));
  width: calc(123 * var(--px));
  font-family: var(--font-display);
  font-size: calc(24 * var(--px));
  font-weight: 400;
  line-height: calc(28 * var(--px));
  white-space: pre-line;
  color: #000;
}

.invite__kicker span {
  display: block;
  transform: rotate(33deg);
}

.invite__mono {
  /* Same rule against the oval frame 2856:643 — index 9, so it starts at 1790ms. */
  --delay: 2400ms;
  width: calc(82 * var(--px));
  line-height: calc(38 * var(--px));
  color: var(--wine-soft);
}

.invite__mono--first {
  left: calc(220 * var(--px));
  top: calc(259 * var(--px));
  font-family: var(--font-display);
  font-size: calc(75 * var(--px));
}

/* 2857:228 — Bibliophile Script Bold 64/38, the design's own face. */
.invite__mono--second {
  --delay: 2520ms;
  left: calc(216 * var(--px));
  top: calc(292 * var(--px));
  font-family: var(--font-monogram);
  font-weight: 700;
  font-size: calc(64 * var(--px));
}
</style>
