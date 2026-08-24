<script setup lang="ts">
// Figma Frame 253 band "wish", y 6414–7082. Coords are band-local design px.
//
// Everything below the heading is live. The two inputs are Figma frames, the three
// cards are 292px plates whose height follows the message, and "Show more" reveals the
// rest of the list — none of which a raster can do, so this band draws its own chrome
// and BandArt only paints the florals behind it.
import { computed, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/wish'
import sendIcon from '../../assets/wish/parts/2894-860.webp'

const { el, shown } = useReveal(0.15)

/*
 * The three card plates and the "Show more" plate are sliced art of a FIXED-height
 * list. The live list is neither three long nor fixed height, so those four rasters
 * are skipped and the cards below are drawn instead. 2894:860 is the send icon, which
 * moves inside a real button.
 */
const SKIP = ['2894:863', '2894:872', '2894:877', '2894:880', '2894:860']
const { wishes, sendWish, guest } = useWedding()

type Wish = { guest_name?: string; message?: string; created_at?: string | null }

// Frame 253 prints these three, so an unconfigured render matches the design.
const DESIGN: Wish[] = [
  {
    guest_name: 'Budi & Sarti',
    message: 'Dear Ahmad & Salma, happy wedding ya. semoga bahagia selalu',
  },
  {
    guest_name: 'Budi & Sarti',
    message:
      'Wishing you a lifetime of love, laughter, and endless happiness. Happy Wedding! 💐🤍 Semoga bisa menjadi keluarga yang sejahtera, selalu bahagia, selalu bersama.....',
  },
  {
    guest_name: 'Budi & Sarti',
    message:
      'Wishing you a lifetime of love, laughter, and endless happiness. Happy Wedding! 💐🤍 Semoga bisa menjadi keluarga yang sejahtera, selalu bahagia, selalu bersama.....',
  },
  // A fourth, so the design fallback still shows the render's "Show more" — the button
  // is part of Frame 253's layout, and one that reveals nothing is worse than no button.
  {
    guest_name: 'Rian & Keluarga',
    message: 'Selamat menempuh hidup baru, semoga sakinah mawaddah warahmah 🤍',
  },
]

const list = computed<Wish[]>(() => {
  const live = (wishes.value as Wish[]).filter((w) => w.guest_name || w.message)
  return live.length ? live : DESIGN
})

const PAGE = 3
const shownCount = ref(PAGE)
const visible = computed(() => list.value.slice(0, shownCount.value))
const hasMore = computed(() => shownCount.value < list.value.length)

const name = ref(guest.value?.name || '')
const message = ref('')
const sending = ref(false)
const error = ref('')

async function send() {
  error.value = ''
  if (!message.value.trim()) {
    error.value = 'Ucapannya masih kosong.'
    return
  }
  sending.value = true
  try {
    await sendWish({
      guest_name: name.value.trim() || 'Tamu',
      message: message.value.trim(),
    })
    message.value = ''
    // A new wish lands at the top; keep it visible without expanding the whole list.
    shownCount.value = Math.max(shownCount.value, PAGE)
  } catch (err: any) {
    error.value = err?.message || 'Gagal mengirim ucapan. Coba lagi.'
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <section :ref="el" class="band wish" :class="{ 'is-in': shown }" aria-labelledby="wish-heading">
    <BandArt :layers="LAYERS" :skip="SKIP" :shown="shown" />

    <!-- 2894:855 — Alex Brush 40/28, #9a1010. -->
    <h2 id="wish-heading" class="wish__heading">Wedding Wish</h2>

    <!-- 2894:856 / 2894:858 — the two fields, and 2894:860's send button on the second. -->
    <form class="wish__form" novalidate @submit.prevent="send">
      <label class="sr-only" for="wish-name">Nama</label>
      <input id="wish-name" v-model="name" class="wish__name" type="text" placeholder="Nama" />

      <label class="sr-only" for="wish-message">Ucapan</label>
      <textarea
        id="wish-message"
        v-model="message"
        class="wish__message"
        rows="1"
        placeholder="Give your wish"
      ></textarea>

      <button class="wish__send" type="submit" :disabled="sending" aria-label="Kirim ucapan">
        <img class="wish__sendicon" :src="sendIcon" alt="" width="33" height="33" />
      </button>
    </form>

    <p v-if="error" class="wish__error" role="alert">{{ error }}</p>

    <!-- 2894:863 / 872 / 877 — 292px plates, stacked from y 232 with a 7px gutter. -->
    <ul class="wish__list">
      <li v-for="(w, i) in visible" :key="i" class="wish__card">
        <p class="wish__who">{{ w.guest_name || 'Tamu' }}</p>
        <p class="wish__text">{{ w.message }}</p>
      </li>
    </ul>

    <!-- 2894:880 plate + 2894:881 Libre Caslon Condensed 16/38, #ffffff. -->
    <button v-if="hasMore" class="wish__more" type="button" @click="shownCount += PAGE">
      Show more
    </button>
  </section>
</template>

<style scoped>
.wish {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.wish__heading {
  --delay: 60ms;
  left: calc(52 * var(--px));
  top: calc(81 * var(--px));
  width: calc(271 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(40 * var(--px));
  font-weight: 400;
  line-height: calc(28 * var(--px));
  color: var(--crimson);
}

.wish__form {
  --delay: 160ms;
  inset: 0;
  width: 100%;
  height: 100%;
}

/*
 * Both fields are white with a hairline olive rule and a fully rounded end — Figma
 * draws them as frames with a stroke, which is a border here rather than an image.
 */
.wish__name,
.wish__message {
  position: absolute;
  left: calc(44 * var(--px));
  width: calc(286 * var(--px));
  padding: 0 calc(10 * var(--px));
  border: calc(1 * var(--px)) solid #7b7c4a;
  border-radius: calc(6 * var(--px));
  background: #fff;
  font-family: var(--font-serif);
  font-style: italic;
  font-size: calc(16 * var(--px));
  line-height: calc(27 * var(--px));
  color: #000;
}

.wish__name::placeholder,
.wish__message::placeholder {
  color: rgba(0, 0, 0, 0.5);
}

.wish__name {
  top: calc(129 * var(--px));
  height: calc(29 * var(--px));
}

.wish__message {
  top: calc(171 * var(--px));
  height: calc(43 * var(--px));
  padding-top: calc(7 * var(--px));
  padding-right: calc(48 * var(--px));
  resize: none;
}

/* 2894:860 — the paper-plane button inside the textarea's right end. */
.wish__send {
  position: absolute;
  display: grid;
  place-items: center;
  left: calc(294 * var(--px));
  top: calc(174 * var(--px));
  width: calc(33 * var(--px));
  height: calc(33 * var(--px));
  border: 0;
  border-radius: 50%;
  background: none;
  cursor: pointer;
  transition: transform 220ms cubic-bezier(0.16, 1, 0.3, 1), opacity 220ms ease;
}

.wish__send:hover:not(:disabled),
.wish__send:focus-visible:not(:disabled) {
  transform: scale(1.06);
}

.wish__send:disabled {
  opacity: 0.6;
  cursor: default;
}

/* The design's own icon, exported — including its brown disc, which is why the button
   itself has no background of its own. */
.wish__sendicon {
  display: block;
  width: calc(33 * var(--px));
  height: calc(33 * var(--px));
}

.wish__error {
  left: calc(44 * var(--px));
  top: calc(216 * var(--px));
  width: calc(286 * var(--px));
  font-family: var(--font-card);
  font-style: italic;
  font-size: calc(12 * var(--px));
  line-height: calc(16 * var(--px));
  text-align: left;
  color: var(--crimson-deep);
}

/*
 * The cards are a flow, not three fixed plates: a live message can be any length, and
 * the design's own three are already two different heights. Stacking them means one
 * long wish pushes the next card down instead of overprinting it.
 */
.wish__list {
  --delay: 300ms;
  display: flex;
  flex-direction: column;
  gap: calc(7 * var(--px));
  left: calc(42 * var(--px));
  top: calc(232 * var(--px));
  width: calc(292 * var(--px));
  list-style: none;
}

.wish__card {
  /* Figma's own card box: 6 above the name, 6 between name and message, 19 below. */
  padding: calc(6 * var(--px)) calc(17 * var(--px)) calc(19 * var(--px));
  border-radius: calc(6 * var(--px));
  background: #6b0d0e;
  text-align: left;
}

.wish__who {
  font-family: var(--font-card);
  font-style: italic;
  font-size: calc(16 * var(--px));
  line-height: calc(26 * var(--px));
  color: #fff;
}

.wish__text {
  margin-top: calc(6 * var(--px));
  font-family: var(--font-card);
  font-style: italic;
  font-size: calc(12 * var(--px));
  line-height: calc(18 * var(--px));
  color: #fff;
}

.wish__more {
  --delay: 420ms;
  left: calc(42 * var(--px));
  top: calc(627 * var(--px));
  width: calc(292 * var(--px));
  height: calc(33 * var(--px));
  border: 0;
  border-radius: calc(6 * var(--px));
  background: #a15a5a;
  cursor: pointer;
  font-family: var(--font-card);
  font-style: italic;
  font-size: calc(16 * var(--px));
  line-height: calc(33 * var(--px));
  color: #fff;
  transition: opacity 220ms ease;
}

.wish__more:hover,
.wish__more:focus-visible {
  opacity: 0.86;
}
</style>
