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
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/gift'

const { el, shown } = useReveal(0.15)
const { gift } = useWedding()

import bcaLogo from '../../assets/gift/parts/2852-333.webp'
import copyIcon from '../../assets/gift/parts/2852-357.webp'

type Card = { logo: boolean; lines: string[]; copy: string }

/*
 * The design repeats the same BCA account twice and then prints a postal address as a
 * third card — its mock data, not a mistake to reproduce. An unconfigured render keeps
 * all three so the band matches the render; live data replaces the lot.
 */
const DESIGN: Card[] = [
  { logo: true, lines: ['No. Rekening : 8715154435', 'A/n Muhammad Arif'], copy: '8715154435' },
  { logo: true, lines: ['No. Rekening : 8715154435', 'A/n Muhammad Arif'], copy: '8715154435' },
  {
    logo: false,
    lines: ['Alamat', '65, Jalan Raya Tanjung Barat', 'A/n Putrianti Resti Rusyah'],
    copy: '65, Jalan Raya Tanjung Barat',
  },
]

/* A `kado` row is a postal address, not an account — the API has no separate field. */
const isKado = (bank?: string) => /kado|alamat|address/i.test(bank || '')

const cards = computed<Card[]>(() => {
  const live = (gift.value as any[])
    .map((g) => {
      const number = (g.account_number || '').trim()
      const name = (g.account_name || '').trim()
      if (!number && !name) return null
      return isKado(g.bank_name)
        ? { logo: false, lines: ['Alamat', number, name].filter(Boolean), copy: number }
        : {
            logo: /bca/i.test(g.bank_name || ''),
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
</script>

<template>
  <section :ref="el" class="band gift" :class="{ 'is-in': shown }" aria-labelledby="gift-heading">
    <BandArt :layers="LAYERS" :skip="REDRAWN" :shown="shown" />

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
      <p class="gift__lines" :style="{ '--slot': `${i * SLOT}` }">{{ card.lines.join('\n') }}</p>
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
  </section>
</template>

<style scoped>
.gift {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
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

.gift__lines {
  --delay: 340ms;
  left: calc(40 * var(--px));
  top: calc((291 + var(--slot)) * var(--px));
  width: calc(255 * var(--px));
  font-family: var(--font-body);
  font-size: calc(14 * var(--px));
  line-height: calc(19 * var(--px));
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
