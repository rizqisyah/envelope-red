<script setup lang="ts">
import { COVER_LAYERS } from '../../lib/coverLayers'
import { useFitText } from '../../composables/useFitText'

// `ready` gates the reveal on the layers being decoded — see App.vue.
defineProps<{ guestName: string; coupleName: string; ready: boolean }>()
defineEmits<{ open: [] }>()

/*
 * The envelope rises first and the pieces that sit on it — seal, lily, medallion —
 * follow, so the scene assembles the way it was stacked rather than all at once.
 */
const delayFor = (z: number) => Math.min(z * 38, 1080)

// The couple name is the one box on the cover with a fixed height — see its rule below.
const fitCouple = useFitText()
</script>

<template>
  <!-- Figma Frame 254 (2852:577), 375 x 725. Coords below are frame-local design px. -->
  <section class="cover">
    <div class="cover__frame" :class="{ 'cover__frame--ready': ready }">
      <img
        v-for="layer in COVER_LAYERS"
        :key="layer.id"
        class="cover__layer"
        :src="layer.src"
        alt=""
        :width="layer.w"
        :height="layer.h"
        :style="{
          zIndex: layer.z,
          left: `calc(${layer.x} * var(--px))`,
          top: `calc(${layer.y} * var(--px))`,
          width: `calc(${layer.w} * var(--px))`,
          height: `calc(${layer.h} * var(--px))`,
          animationDelay: `${delayFor(layer.z)}ms`,
        }"
      />

      <!-- 2852:583 / 2852:585 — z 6 and 8 in Figma child order. -->
      <p class="cover__eyebrow">The Wedding Of</p>
      <h1 :ref="fitCouple" class="cover__couple">{{ coupleName }}</h1>

      <!-- 2852:587 / 2852:582 — z 10 and 5. -->
      <p class="cover__dear">Dear Mr/ Mrs/ Ms</p>
      <p class="cover__guest">{{ guestName }}</p>

      <!--
        2852:584 — z 7, above the envelope, below the seal and the lily. The words are
        the label; the envelope above them is the hit area, which is what the design
        actually invites you to tap. So the text is a plain <p> and the button is a
        transparent plate over the envelope's box (2854:610, 47/222/295x196), named by
        the label it sits under.
      -->
      <p id="cover-open-label" class="cover__open">Click to open...</p>
      <button
        type="button"
        class="cover__hit"
        aria-labelledby="cover-open-label"
        @click="$emit('open')"
      />
    </div>
  </section>
</template>

<style scoped>
.cover {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 100dvh;
  overflow: hidden;
  background: var(--wine);
}

/*
 * One design pixel = 1cqw / 3.75, so the whole composition scales as a unit instead of
 * reflowing. Width is driven by the viewport height so the card fills the screen; on
 * screens too narrow for that width, `.cover`'s `overflow: hidden` crops the sides
 * evenly. `max()`, not the bare height-derived width: Safari's dvh excludes the
 * toolbars, so the derived width lands short of the screen and leaves a wine gutter
 * down both sides. Filling the width and letting `.cover` crop the extra height keeps
 * the scene full-bleed.
 */
.cover__frame {
  container-type: inline-size;
  position: relative;
  overflow: hidden;
  /* flex-shrink: 0 — otherwise the 430px column squashes the width-driven frame back down */
  flex: 0 0 auto;
  width: max(100%, calc(100dvh * 375 / 725));
  aspect-ratio: 375 / 725;
  background: var(--wine);
}

/*
 * Desktop hosts the cover in a fixed 430px column (App.vue), so a width derived purely
 * from viewport height overshoots it and the composition is cropped down both sides.
 * Phones have no such column, so the fill-the-screen rule above still holds there and
 * only this case is clamped.
 */
@media (min-width: 768px) {
  .cover__frame {
    width: min(100%, calc(100dvh * 375 / 725));
  }
}

.cover__frame > * {
  --px: 0.26667cqw; /* 100cqw / 375 */
  position: absolute;
  margin: 0;
  text-align: center;
  /*
   * Held until the layers are decoded. `animation-play-state` rather than `display`
   * so the images are still in the document and actually fetching while hidden.
   */
  visibility: hidden;
  animation-play-state: paused;
}

.cover__frame--ready > * {
  visibility: visible;
  animation-play-state: running;
}

.cover__layer {
  max-width: none;
  /* The lily is authored across the "Click to open..." box; without this it swallows
     every click and tap meant for the button underneath it. */
  pointer-events: none;
  animation: rise 2200ms cubic-bezier(0.16, 1, 0.3, 1) backwards;
}

/*
 * `backwards`, not `forwards`: the end state is the element's normal state, so once
 * the animation finishes it stops applying and hover transitions get their transform back.
 */
@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(calc(18 * var(--px)));
  }
}

.cover__eyebrow,
.cover__couple,
.cover__dear,
.cover__guest,
.cover__open {
  animation: rise 2400ms cubic-bezier(0.16, 1, 0.3, 1) var(--delay, 0ms) backwards;
}

/*
 * 2852:583 — BusinessPenmanshipW00-Bold 20/30, #e8e4a9. That face has no webfont and no
 * file, so this runs on Playball. Playball sets NARROWER than the penmanship at the same
 * size — 133 design px of ink against the render's 153 — so the size is compensated up to
 * 23 and `left` pulled 2px back to 51 to re-centre the wider line. Both numbers are ink
 * boxes measured against .figma-tmp/frame254-1x.png, and both must be reverted to Figma's
 * 20/53 if the real face is ever licensed.
 */
.cover__eyebrow {
  --delay: 900ms;
  z-index: 6;
  top: calc(147 * var(--px));
  left: calc(51 * var(--px));
  width: calc(269 * var(--px));
  font-family: var(--font-script);
  font-size: calc(23 * var(--px));
  line-height: calc(30 * var(--px));
  color: var(--gold-pale);
}

/*
 * 2852:585 — Charoly Demo 32/27, #eed891. The real face, self-hosted (see style.css),
 * so every number here is Figma's own and there is no substitute compensation to carry.
 *
 * NO text-transform. The Figma string is "Ahmad & Salma" in title case, and in this face
 * the lowercase are drawn as cap-height alternates while the actual capitals are a
 * different, swashed set — uppercasing it swaps the whole word onto that set and the
 * name stops looking like the render. Feed it the string as it comes.
 *
 * Figma's box is 27 tall for a 32px line, so its line box is shorter than the glyphs it
 * holds. Reproducing that literally made `scrollHeight` exceed `clientHeight` on a single
 * line and useFitText shrank the name to 0.92 for no reason — 190px of ink against the
 * render's 207. So line-height carries the full 32 and `top` gives back the 2.5px that
 * re-centres it on Figma's baseline; the ink then lands within 1px of the render.
 *
 * `height` (34, a hair over the line box) exists only as the constraint useFitText
 * measures against — nothing is clipped, `overflow` stays visible. One line always fits;
 * a name long enough to wrap measures 2x32 and shrinks instead of painting across the
 * envelope. line-height scales with --fit too, otherwise shrinking the glyphs would never
 * shorten the block and the fit would never converge.
 */
.cover__couple {
  --delay: 1150ms;
  z-index: 8;
  top: calc(182.5 * var(--px));
  left: calc(50 * var(--px));
  width: calc(289 * var(--px));
  height: calc(34 * var(--px) * var(--fit, 1));
  font-family: var(--font-display);
  font-size: calc(32 * var(--px) * var(--fit, 1));
  font-weight: 400;
  line-height: calc(32 * var(--px) * var(--fit, 1));
  color: var(--gold-bright);
}

/* 2852:587 — Ibarra Real Nova 14 Medium Italic, #d0cb84. */
.cover__dear {
  --delay: 1450ms;
  z-index: 10;
  top: calc(500 * var(--px));
  left: calc(91 * var(--px));
  width: calc(193 * var(--px));
  font-family: var(--font-serif);
  font-style: italic;
  font-weight: 500;
  font-size: calc(14 * var(--px));
  line-height: calc(25 * var(--px));
  color: var(--gold-muted);
}

/* 2852:582 — Ibarra Real Nova 16 Medium Italic, #d0cb84. */
.cover__guest {
  --delay: 1600ms;
  z-index: 5;
  top: calc(522 * var(--px));
  left: calc(106 * var(--px));
  width: calc(163 * var(--px));
  font-family: var(--font-serif);
  font-style: italic;
  font-weight: 500;
  font-size: calc(16 * var(--px));
  line-height: calc(25 * var(--px));
  color: var(--gold-muted);
}

/* 2852:584 — Jost 15/30, +2% tracking, #eed891. */
.cover__open {
  --delay: 1800ms;
  z-index: 7;
  top: calc(454 * var(--px));
  left: calc(40 * var(--px));
  width: calc(133 * var(--px));
  pointer-events: none;
  font-family: var(--font-sans);
  font-size: calc(15 * var(--px));
  line-height: calc(30 * var(--px));
  letter-spacing: 0.02em;
  color: var(--gold-bright);
  transition:
    transform 240ms cubic-bezier(0.16, 1, 0.3, 1),
    opacity 240ms ease;
}

/*
 * The hit area is invisible, so its own hover state would be too — the affordance is
 * carried by the label and the envelope, which lift together when the plate is hovered.
 */
.cover__hit {
  z-index: 7;
  top: calc(222 * var(--px));
  left: calc(47 * var(--px));
  width: calc(295 * var(--px));
  height: calc(196 * var(--px));
  border: 0;
  background: none;
  cursor: pointer;
  /* No entrance of its own — it is invisible, and animating it would gate the tap. */
  animation: none;
}

.cover__frame:has(.cover__hit:hover) .cover__open,
.cover__frame:has(.cover__hit:focus-visible) .cover__open {
  transform: translateY(calc(-2 * var(--px)));
  opacity: 0.82;
}

.cover__hit:focus-visible {
  outline: calc(1.5 * var(--px)) solid var(--gold-muted);
  outline-offset: calc(2 * var(--px));
}

@media (prefers-reduced-motion: reduce) {
  .cover__frame > * {
    animation: none;
  }
}
</style>
