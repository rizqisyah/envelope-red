<script setup lang="ts">
// Figma Frame 253 band "acara", y 4265–5132. Coords are band-local design px.
//
// Akad and Resepsi are one band, not two: the design draws them inside a single floral
// arch whose layers cross both cards, and splitting them would put half of that arch in
// each band's coordinate space for no gain.
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useFitText } from '../../composables/useFitText'
import { useWedding } from '../../composables/useWedding'
import { formatEventDate, formatEventTime } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/acara'

const { el, shown } = useReveal(0.15)
// One per card: a useFitText instance drives a single element.
const fitTitle = [useFitText(), useFitText()]
const fitPlace = [useFitText(), useFitText()]
const { acara } = useWedding()

type Card = {
  title: string
  date: string
  time: string
  venue: string
  address: string
  maps: string
}

const DESIGN_DATE = 'Saturday,\n10th June 2026'
const DESIGN_ADDRESS = 'Jl. Singaraja Mataram, Sungai Badung,\nKec. Singkawang'

const FALLBACK: Card[] = [
  {
    title: 'Akad\nNikah',
    date: DESIGN_DATE,
    time: '08.00 - 10.00',
    venue: 'Kediaman Mempelai Wanita',
    address: DESIGN_ADDRESS,
    maps: '',
  },
  {
    title: 'Resepsi',
    date: DESIGN_DATE,
    time: '08.00 - 10.00',
    venue: 'Kediaman Mempelai Wanita',
    address: DESIGN_ADDRESS,
    maps: '',
  },
]

/*
 * All or nothing, never a mix. Topping a one-event list up from FALLBACK would print the
 * design's placeholder date and address in the second aperture as if they were this
 * couple's reception, and a guest would drive to Jl. Singaraja Mataram. So live data
 * replaces the whole pair, and a live list of one renders one card and leaves the second
 * aperture empty — the arch behind it is art either way.
 *
 * Capped at two: the arch has two apertures, so a third event has nowhere to go.
 */
const cards = computed<Card[]>(() => {
  const live = (acara.value as any[]).filter((a) => a?.name || a?.event_date)
  if (!live.length) return FALLBACK
  return live.slice(0, 2).map((a, i) => {
    const fallback = FALLBACK[i]
    const when = formatEventDate(a.event_date)
    return {
      // The design breaks the weekday onto its own line; the API sends one date.
      title: a.name || fallback.title,
      date: when ? `${when.weekday},\n${when.date}` : fallback.date,
      time: formatEventTime(a.event_time) || fallback.time,
      // NOT `|| fallback.*`: the design's placeholder is a real street in Singkawang,
      // and printing it under a live event would send guests to the wrong address.
      venue: a.location_name || '',
      address: a.address || '',
      maps: a.maps_url || '',
    }
  })
})

const skipLayers = computed(() => {
  const skip = []
  if (cards.value.length === 1) {
    skip.push(
      '2880:333', // second aperture background
      '2880:334', '2880:335', '2880:336', '2880:337', // corner dots
      '2878:323', // pin
      '2878:325', // maps chip
      '2881:360', // pink lace
      '2881:347', // dahlia stem
      '2881:342', // dahlia small
      '2881:348', // dahlia large
      '2881:352', // golden seal
      '2880:339', // left floral (starts at 2nd aperture)
      '2881:361'  // right floral (starts at 2nd aperture)
    )
  }
  return skip
})

// When there is only 1 event, the second slot (which is 358px tall) is removed.
// We shrink the band height so the next section slides up naturally.
const sectionHeight = computed(() => cards.value.length === 1 ? BAND_HEIGHT - 358 : BAND_HEIGHT)
</script>

<template>
  <section :ref="el" class="band acara" :class="{ 'is-in': shown }" aria-labelledby="acara-0">
    <BandArt :layers="LAYERS" :skip="skipLayers" :shown="shown" />

    <template v-for="(card, i) in cards" :key="i">
      <!-- 2878:289 / 2878:318 — Alex Brush 32/26, #ffffff. -->
      <h2 :ref="fitTitle[i]" :id="`acara-${i}`" class="acara__title" :class="`acara__slot--${i}`">{{ card.title }}</h2>
      <!-- 2878:290 / 2878:319 — Alex Brush 20/24. -->
      <p class="acara__date" :class="`acara__slot--${i}`">{{ card.date }}</p>
      <!-- 2878:292 / 2878:320 — Bellefair 15/18. -->
      <p class="acara__time" :class="`acara__slot--${i}`">{{ card.time }}</p>
      <!--
        Venue and address share one box: a venue name that wrapped printed its second
        line over the address, which sat at a fixed 16px below it.
      -->
      <div :ref="fitPlace[i]" class="acara__place" :class="`acara__slot--${i}`">
        <!-- 2878:303 / 2878:321 — Bellefair 13/16. -->
        <p class="acara__venue">{{ card.venue }}</p>
        <!-- 2878:304 / 2878:322 — Bellefair 11/13. -->
        <p class="acara__address">{{ card.address }}</p>
      </div>
      <!-- 2878:306 / 2878:326 — Bellefair 10/16, #660c21, on the chip at 2878:305/325. -->
      <a
        v-if="card.maps"
        class="acara__maps"
        :class="`acara__slot--${i}`"
        :href="card.maps"
        target="_blank"
        rel="noopener noreferrer"
        >MAPS</a
      >
      <p v-else class="acara__maps" :class="`acara__slot--${i}`">MAPS</p>
    </template>
  </section>
</template>

<style scoped>
.acara {
  height: calc(v-bind(sectionHeight) * var(--px));
}

/* The two cards are identical apart from their y, so each row is placed once and the
 * slot modifier moves the whole card down to the second aperture. */
.acara__slot--0 {
  --slot: 0;
  --tslot: 0;
}

/*
 * 358, not 377. Every row of the Resepsi card sits 358 below its Akad twin — except the
 * heading, which sits 377 below, because "Akad Nikah" wraps to two lines in a box only
 * one line tall and Figma placed the one-line "Resepsi" against the wrap, not the box.
 */
.acara__slot--1 {
  --slot: 358;
  --tslot: 377;
}

.acara__title,
.acara__date,
.acara__time,
.acara__venue,
.acara__address,
.acara__maps {
  white-space: pre-line;
  color: #fff;
}

/*
 * `height` is only useFitText's constraint (overflow stays visible): two lines, as
 * "Akad Nikah" takes, plus the gap down to the date at 165. A third line shrinks the
 * heading instead of landing on the date.
 */
.acara__title {
  --delay: 60ms;
  left: calc(88 * var(--px));
  top: calc((96 + var(--tslot)) * var(--px));
  width: calc(198 * var(--px));
  height: calc(64 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(32 * var(--px) * var(--fit, 1));
  font-weight: 400;
  line-height: calc(26 * var(--px) * var(--fit, 1));
}

.acara__date {
  --delay: 140ms;
  left: calc(89 * var(--px));
  top: calc((165 + var(--slot)) * var(--px));
  width: calc(198 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(20 * var(--px));
  line-height: calc(24 * var(--px));
}

.acara__time {
  --delay: 200ms;
  left: calc(89 * var(--px));
  top: calc((227 + var(--slot)) * var(--px));
  width: calc(198 * var(--px));
  font-family: var(--font-detail);
  font-size: calc(15 * var(--px));
  line-height: calc(18 * var(--px));
}

/*
 * The MAPS chip (2878:305) is art at a fixed y, so the box cannot grow down onto it:
 * `height` runs from the venue's 284 to the chip's 339 plus a pixel, and useFitText
 * shrinks both lines together when a long venue or address needs more than that.
 */
.acara__place {
  --delay: 260ms;
  left: calc(96 * var(--px));
  top: calc((284 + var(--slot)) * var(--px));
  width: calc(183 * var(--px));
  height: calc(56 * var(--px));
}

.acara__venue {
  width: calc(182 * var(--px));
  font-family: var(--font-detail);
  font-size: calc(13 * var(--px) * var(--fit, 1));
  line-height: calc(16 * var(--px) * var(--fit, 1));
}

/* Figma's x is 97, a pixel right of the venue's. */
.acara__address {
  margin-left: calc(1 * var(--px));
  width: calc(182 * var(--px));
  font-family: var(--font-detail);
  font-size: calc(11 * var(--px) * var(--fit, 1));
  line-height: calc(13 * var(--px) * var(--fit, 1));
}

/* Sits on 2878:305, the cream chip — hence the dark fill rather than white. */
.acara__maps {
  --delay: 360ms;
  left: calc(155 * var(--px));
  top: calc((342 + var(--slot)) * var(--px));
  width: calc(66 * var(--px));
  font-family: var(--font-detail);
  font-size: calc(10 * var(--px));
  line-height: calc(16 * var(--px));
  letter-spacing: 0.06em;
  text-decoration: none;
  color: var(--maps);
}

a.acara__maps:hover,
a.acara__maps:focus-visible {
  text-decoration: underline;
}
</style>
