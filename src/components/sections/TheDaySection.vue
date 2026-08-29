<script setup lang="ts">
// Figma Frame 253 band "theday", y 3795–4265. Coords are band-local design px.
// The countdown is live: Figma bakes four zeroes, this counts down to the akad.
import { computed, onUnmounted, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { parseEventStart, remainingUntil } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/theday'

const { el, shown } = useReveal(0.15)
const { acara, wedding } = useWedding()

const now = ref(Date.now())
const timer = window.setInterval(() => (now.value = Date.now()), 1000)
onUnmounted(() => window.clearInterval(timer))

/*
 * The first event with a parseable date is the one being counted to.
 *
 * The fallback is Frame 253's own printed date — which has already passed, so with no
 * `acara` configured the counter sits at 0/0/0/0. That is what the render shows too, and
 * it is the honest reading of "the design's wedding was in June 2026", but it means a
 * DEPLOYMENT WITH NO EVENT DATA SHIPS A DEAD COUNTDOWN. `VITE_DEFAULT_SLUG` and a real
 * acara list are what fix that; do not paper over it by inventing a future date here.
 */
const DESIGN_DAY = new Date(2026, 5, 10, 8, 0)

const target = computed(() => {
  if (wedding.value?.countdown_date) {
    const at = new Date(wedding.value.countdown_date)
    if (!Number.isNaN(at.getTime())) return at
  }
  for (const a of acara.value as any[]) {
    const at = parseEventStart(a?.event_date, a?.event_time)
    if (at) return at
  }
  return DESIGN_DAY
})

const left = computed(() => remainingUntil(target.value, now.value))

// Figma authors this break. `&#10;` in the template is folded to a space by the
// HTML parser, so the string comes from here and the box sets `white-space: pre-line`.
const TITLE = 'Save the\nDate'
</script>

<template>
  <section :ref="el" class="band theday" :class="{ 'is-in': shown }" aria-labelledby="save-the-date">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- 2877:266 — Alex Brush 40/28, #9a1010. Figma authors the break after "Save the". -->
    <h2 id="save-the-date" class="theday__title">{{ TITLE }}</h2>

    <!-- 2877:268-276 — Activists 24/38 for the figures, Alex Brush 15/38 for the labels. -->
    <p class="theday__n theday__n--days">{{ left.days }}</p>
    <p class="theday__l theday__l--days">days</p>
    <p class="theday__n theday__n--hours">{{ left.hours }}</p>
    <p class="theday__l theday__l--hours">Hours</p>
    <p class="theday__n theday__n--minutes">{{ left.minutes }}</p>
    <p class="theday__l theday__l--minutes">Minutes</p>
    <p class="theday__n theday__n--seconds">{{ left.seconds }}</p>
    <p class="theday__l theday__l--seconds">Seconds</p>
  </section>
</template>

<style scoped>
.theday {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.theday__title {
  --delay: 60ms;
  left: calc(88 * var(--px));
  top: calc(181 * var(--px));
  width: calc(198 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(40 * var(--px));
  font-weight: 400;
  line-height: calc(28 * var(--px));
  white-space: pre-line;
  color: var(--crimson);
}

.theday__n {
  --delay: 200ms;
  width: calc(41 * var(--px));
  font-family: var(--font-figures);
  font-size: calc(24 * var(--px));
  line-height: calc(38 * var(--px));
  color: var(--crimson-bright);
  /* The seconds tick every second; a proportional face would shuffle the row sideways. */
  font-variant-numeric: tabular-nums;
}

.theday__l {
  --delay: 260ms;
  font-family: var(--font-heading);
  font-size: calc(15 * var(--px));
  line-height: calc(38 * var(--px));
  color: var(--crimson-bright);
}

.theday__n--days {
  left: calc(129 * var(--px));
  top: calc(256 * var(--px));
}

.theday__l--days {
  left: calc(129 * var(--px));
  top: calc(277 * var(--px));
  width: calc(41 * var(--px));
}

.theday__n--hours {
  left: calc(205 * var(--px));
  top: calc(256 * var(--px));
}

.theday__l--hours {
  left: calc(205 * var(--px));
  top: calc(277 * var(--px));
  width: calc(41 * var(--px));
}

.theday__n--minutes {
  left: calc(129 * var(--px));
  top: calc(318 * var(--px));
}

.theday__l--minutes {
  left: calc(116 * var(--px));
  top: calc(339 * var(--px));
  width: calc(68 * var(--px));
}

.theday__n--seconds {
  left: calc(205 * var(--px));
  top: calc(318 * var(--px));
}

.theday__l--seconds {
  left: calc(193 * var(--px));
  top: calc(339 * var(--px));
  width: calc(65 * var(--px));
}
</style>
