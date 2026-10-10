<script setup lang="ts">
// Figma Frame 253 band "gift", y 5281–6024. Coords are band-local design px.
//
// The three cards are one repeated shape: a flat #6b0d0e plate (2852:328/336/344), a
// darker tab down its right edge (2852:329/337/345) and a copy button on that tab
// (2852:357/358/360). Only the tab is sliced art — the plate is flat colour and the
// copy button has to be a real button, so both are drawn here.
import { computed, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useFitText } from '../../composables/useFitText'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/gift'

const { el, shown } = useReveal(0.15)
// One per plate: a useFitText instance drives a single element.
const fitLines = [useFitText(), useFitText(), useFitText()]
const { gift, videoPrewed } = useWedding()

import bcaLogo from '../../assets/gift/parts/2852-333.webp'
import copyIcon from '../../assets/gift/parts/2852-357.webp'

type Card = { logo: boolean; isKado: boolean; lines: string[]; copy: string }

/*
 * The design repeats the same BCA account twice and then prints a postal address as a
 * third card — its mock data, not a mistake to reproduce. An unconfigured render keeps
 * all three so the band matches the render; live data replaces the lot.
 */
const DESIGN: Card[] = [
  { logo: true, isKado: false, lines: ['No. Rekening : 8715154435', 'A/n Muhammad Arif'], copy: '8715154435' },
  { logo: true, isKado: false, lines: ['No. Rekening : 8715154435', 'A/n Muhammad Arif'], copy: '8715154435' },
  {
    logo: false,
    isKado: true,
    lines: ['Alamat', '65, Jalan Raya Tanjung Barat', 'A/n Putrianti Resti Rusyah'],
    copy: '65, Jalan Raya Tanjung Barat',
  },
]

/* A `kado` row is a postal address, not an account — the API has no separate field. */
const checkKado = (bank?: string) => /kado|alamat|address/i.test(bank || '')

const cards = computed<Card[]>(() => {
  const live = (gift.value as any[])
    .map((g) => {
      const number = (g.account_number || '').trim()
      const name = (g.account_name || '').trim()
      if (!number && !name) return null
      return checkKado(g.bank_name)
        ? { logo: false, isKado: true, lines: ['Alamat', number, name].filter(Boolean), copy: number }
        : {
            logo: /bca/i.test(g.bank_name || ''),
            isKado: false,
            lines: [
              `No. Rekening : ${number}`,
              name ? `A/n ${name}` : '',
              !/bca/i.test(g.bank_name || '') && g.bank_name ? String(g.bank_name) : '',
            ].filter(Boolean),
            copy: number,
          }
    })
    .filter(Boolean) as Card[]
  // Three slots: the art behind them is three plates, so a fourth account has nowhere
  // to go. Extra rows fall off the end rather than painting past the last plate.
  return live.length ? live.slice(0, 3) : DESIGN
})

const hasGift = computed(() => {
  const arr = gift.value as any[]
  return arr && arr.length > 0
})

const hasVideo = computed(() => !!videoPrewed.value)

// Show this section if there are gifts OR if we need to provide the bottom border for the video
const showSection = computed(() => hasGift.value || hasVideo.value)

// Dynamically compute the height based on the number of gifts.
// Slot 0 ends around 363. Gap below is 142. Height = 505.
// Slot 1 ends around 482. Gap below is 142. Height = 624.
// Slot 2 ends around 601. Gap below is 142. Height = 743 (BAND_HEIGHT).
const sectionHeight = computed(() => {
  if (!hasGift.value) return 108
  const count = cards.value.length
  if (count === 1) return 505
  if (count === 2) return 624
  return BAND_HEIGHT
})

const copied = ref(-1)
async function copy(i: number, text: string) {
  if (!text) return
  try {
    await navigator.clipboard.writeText(text)
    copied.value = i
    window.setTimeout(() => (copied.value = -1), 1600)
  } catch {
    // Clipboard is permission-gated and absent over plain http; the number is on
    // screen either way, so a failure is silent rather than an error the guest
    // cannot act on.
  }
}

/* 119px between plates — Figma's own 5534 / 5653 / 5772. */
const SLOT = 119

/*
 * Everything this band draws itself. The copy icons become real buttons, and the BCA
 * logos are per-account: BandArt would paint the raster under a Mandiri account number
 * because the design's own two cards happen to be BCA.
 */
const REDRAWN = ['2852:357', '2852:358', '2852:360', '2852:333', '2852:341']

const skipLayers = computed(() => {
  const skips = [...REDRAWN]
  if (!hasGift.value) {
    skips.push('2852:328', '2852:329')
    skips.push('2852:336', '2852:337')
    skips.push('2852:344', '2852:345')
  } else {
    const count = cards.value.length
    if (count < 2) skips.push('2852:336', '2852:337')
    if (count < 3) skips.push('2852:344', '2852:345')
  }
  return skips
})
</script>

<template>
  <section v-if="showSection" :ref="el" class="band gift" :class="{ 'is-in': shown }" aria-labelledby="gift-heading">
    <BandArt :layers="LAYERS" :skip="skipLayers" :shown="shown" />

    <template v-if="hasGift">
      <!-- 2852:325 — Alex Brush 40/28, #9a1010. -->
      <h2 id="gift-heading" class="gift__heading">Wedding Gift</h2>
      <!-- 2852:348 — EB Garamond 12/17, #000000, left aligned. -->
      <p class="gift__copy">
        Your presence and warm wishes are truly the greatest gifts to us. Should you kindly wish to
        share an additional token of love, we would receive it with heartfelt gratitude.
      </p>

      <template v-for="(card, i) in cards" :key="i">
        <img
          v-if="card.logo"
          class="gift__logo"
          :src="bcaLogo"
          alt="BCA"
          width="60"
          height="19"
          :style="{ '--slot': `${i * SLOT}` }"
        />
        <div
          v-else-if="card.isKado"
          class="gift__icon"
          :style="{ '--slot': `${i * SLOT}` }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="8" width="18" height="4" rx="1"/>
            <path d="M12 8v13"/>
            <path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/>
            <path d="M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/>
          </svg>
        </div>
        <p :ref="fitLines[i]" class="gift__lines" :style="{ '--slot': `${i * SLOT}` }">{{ card.lines.join('\n') }}</p>
        <button
          type="button"
          class="gift__copybtn"
          :style="{ '--slot': `${i * SLOT}` }"
          :aria-label="copied === i ? 'Tersalin' : `Salin ${card.copy}`"
          @click="copy(i, card.copy)"
        >
          <img
            class="gift__copyicon"
            :class="{ 'is-copied': copied === i }"
            :src="copyIcon"
            alt=""
            width="21"
            height="21"
          />
        </button>
      </template>
    </template>
  </section>
</template>

<style scoped>
.gift {
  height: calc(v-bind(sectionHeight) * var(--px));
}

.gift__heading {
  --delay: 60ms;
  left: calc(17 * var(--px));
  top: calc(138 * var(--px));
  width: calc(230 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(40 * var(--px));
  font-weight: 400;
  line-height: calc(28 * var(--px));
  color: var(--crimson);
}

.gift__copy {
  --delay: 160ms;
  left: calc(29 * var(--px));
  top: calc(184 * var(--px));
  width: calc(315 * var(--px));
  font-family: var(--font-body);
  font-size: calc(12 * var(--px));
  line-height: calc(17 * var(--px));
  text-align: left;
  color: #000;
}

.gift__logo {
  --delay: 300ms;
  left: calc(40 * var(--px));
  top: calc((268 + var(--slot)) * var(--px));
  width: calc(60 * var(--px));
  height: calc(19 * var(--px));
}

.gift__icon {
  --delay: 300ms;
  position: absolute;
  left: calc(45 * var(--px));
  top: calc((266 + var(--slot)) * var(--px));
  width: calc(24 * var(--px));
  height: calc(24 * var(--px));
  color: #fff;
}

/*
 * `height` is only useFitText's constraint: what is left of the 110px plate (253..363)
 * below the first line, less a margin. Three lines fit as designed; a long kado address
 * or account name shrinks instead of running onto the next plate.
 */
.gift__lines {
  --delay: 340ms;
  left: calc(40 * var(--px));
  top: calc((291 + var(--slot)) * var(--px));
  width: calc(255 * var(--px));
  height: calc(64 * var(--px));
  font-family: var(--font-body);
  font-size: calc(14 * var(--px) * var(--fit, 1));
  line-height: calc(19 * var(--px) * var(--fit, 1));
  text-align: left;
  white-space: pre-line;
  color: #fff;
}

/* Sits on the tab at 2852:357's own spot; 44px of tab, so the hit area is the tab. */
.gift__copybtn {
  --delay: 380ms;
  z-index: 92;
  display: grid;
  place-items: center;
  left: calc(307 * var(--px));
  top: calc((253 + var(--slot)) * var(--px));
  width: calc(44 * var(--px));
  height: calc(110 * var(--px));
  border: 0;
  background: none;
  cursor: pointer;
}

/* The design's own icon, exported. Redrawing it in CSS is both more code and wrong: the
   glyph is Figma's, not something to guess at with borders and a box-shadow. */
.gift__copyicon {
  display: block;
  width: calc(21 * var(--px));
  height: calc(21 * var(--px));
  transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1), opacity 200ms ease;
}

.gift__copybtn:hover .gift__copyicon,
.gift__copybtn:focus-visible .gift__copyicon {
  transform: translateY(calc(-1 * var(--px)));
}

.gift__copyicon.is-copied {
  transform: scale(0.82);
  opacity: 0.55;
}
</style>
