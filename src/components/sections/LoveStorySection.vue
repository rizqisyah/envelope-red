<script setup lang="ts">
// Love story — not in Frame 253. The design has no story band, so this one is drawn
// rather than sliced: it borrows the cream half's palette and faces (Alex Brush
// headings in --crimson, Playfair SC labels, EB Garamond copy) and flows instead of
// sitting at fixed coordinates, because the number of chapters and the length of each
// come from the API.
//
// Sits between AcaraSection and YouMeSection: acara's art ends flush with its band and
// youme's only rises 10px, so a variable-height block here cuts no layer in half.
import { computed, type Directive } from 'vue'
import { DESIGN_MODE } from '../../lib/api'
import { useWedding } from '../../composables/useWedding'
import { formatEventDate } from '../../lib/format'
import { assets } from '../../lib/bandAssets'

const { ceritaCinta } = useWedding()

type Chapter = { title: string; date: string; text: string; image: string }

// Design mode has no API, so it shows sample chapters to keep the section visible.
const DESIGN_STORY: Chapter[] = [
  {
    title: 'Pertama Bertemu',
    date: '12 March 2021',
    text: 'Sebuah pertemuan sederhana yang tak pernah kami sangka akan menjadi awal dari segalanya.',
    image: assets['gallery/parts/2875-228.webp'] ?? '',
  },
  {
    title: 'Menjalin Kasih',
    date: '14 February 2023',
    text: 'Dari sahabat menjadi kekasih, kami memutuskan untuk saling menjaga dan berjalan bersama.',
    image: '',
  },
  {
    title: 'Lamaran',
    date: '10 December 2025',
    text: 'Dengan restu kedua keluarga, kami berjanji untuk melangkah ke jenjang yang lebih suci.',
    image: '',
  },
]

// `event_date` is free text in cerita_cinta: an ISO date is set like the acara dates,
// anything else ("Musim hujan 2019") is printed as written.
function storyDate(raw?: string | null): string {
  const s = (raw ?? '').trim()
  if (!s || s === '-') return ''
  return formatEventDate(s)?.date ?? s
}

const chapters = computed<Chapter[]>(() => {
  const live = (ceritaCinta.value as any[])
    .map((c) => ({
      title: (c?.title ?? '').trim(),
      date: storyDate(c?.event_date),
      text: (c?.description ?? '').trim(),
      image: (c?.image_url ?? '').trim(),
    }))
    .filter((c) => c.title || c.text)
  if (live.length) return live
  return DESIGN_MODE ? DESIGN_STORY : []
})

/*
 * Each chapter reveals on its own. A list can run several screens long, so one
 * observer on the section would play the later entrances where nobody is looking.
 */
const vReveal: Directive<HTMLElement> = {
  mounted(node) {
    const obs = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          node.classList.add('is-in')
          obs.disconnect()
        }
      },
      { rootMargin: '0px 0px -12% 0px' },
    )
    obs.observe(node)
    ;(node as any)._revealObs = obs
  },
  unmounted(node) {
    ;(node as any)._revealObs?.disconnect()
  },
}
</script>

<template>
  <section v-if="chapters.length" class="lovestory" aria-labelledby="love-story-title">
    <header v-reveal class="lovestory__head">
      <p class="lovestory__kicker">The Journey of</p>
      <h2 id="love-story-title" class="lovestory__title">Our Love Story</h2>
      <span class="lovestory__rule" aria-hidden="true"><i></i></span>
    </header>

    <ol class="lovestory__list">
      <li
        v-for="(c, i) in chapters"
        :key="i"
        v-reveal
        class="lovestory__item"
        :class="{ 'is-last': i === chapters.length - 1 }"
      >
        <span class="lovestory__dot" aria-hidden="true"></span>

        <figure v-if="c.image" class="lovestory__photo">
          <img :src="c.image" :alt="c.title || 'Foto kisah cinta'" loading="lazy" decoding="async" />
        </figure>

        <p v-if="c.date" class="lovestory__date">{{ c.date }}</p>
        <h3 v-if="c.title" class="lovestory__name">{{ c.title }}</h3>
        <p v-if="c.text" class="lovestory__text">{{ c.text }}</p>
      </li>
    </ol>
  </section>
</template>

<style scoped>
.lovestory {
  position: relative;
  /* Above the sheet's wine plate (z 2) in case the two ever meet. */
  z-index: 3;
  padding: calc(44 * var(--px)) calc(32 * var(--px)) calc(56 * var(--px));
  color: var(--bronze);
}

.lovestory__head {
  text-align: center;
  margin-bottom: calc(30 * var(--px));
}

.lovestory__kicker {
  margin: 0;
  font-family: var(--font-caps);
  font-size: calc(11 * var(--px));
  letter-spacing: 0.18em;
  color: var(--gold);
}

.lovestory__title {
  margin: calc(4 * var(--px)) 0 0;
  font-family: var(--font-heading);
  font-size: calc(40 * var(--px));
  font-weight: 400;
  line-height: calc(40 * var(--px));
  color: var(--crimson);
}

/* A hairline with a lozenge at its middle, in the akad/resepsi gold. */
.lovestory__rule {
  position: relative;
  display: block;
  width: calc(120 * var(--px));
  height: 1px;
  margin: calc(12 * var(--px)) auto 0;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

.lovestory__rule i {
  position: absolute;
  left: 50%;
  top: 50%;
  width: calc(6 * var(--px));
  height: calc(6 * var(--px));
  background: var(--gold);
  transform: translate(-50%, -50%) rotate(45deg);
}

.lovestory__list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.lovestory__item {
  position: relative;
  padding: 0 0 calc(28 * var(--px)) calc(30 * var(--px));
}

.lovestory__item.is-last {
  padding-bottom: 0;
}

/* The thread that ties the chapters together; it stops at the last dot. */
.lovestory__item::before {
  content: '';
  position: absolute;
  left: calc(6 * var(--px));
  top: calc(10 * var(--px));
  bottom: calc(-4 * var(--px));
  width: 1px;
  background: color-mix(in srgb, var(--gold) 55%, transparent);
}

.lovestory__item.is-last::before {
  display: none;
}

.lovestory__dot {
  position: absolute;
  left: 0;
  top: calc(3 * var(--px));
  width: calc(13 * var(--px));
  height: calc(13 * var(--px));
  border: 1px solid var(--gold);
  border-radius: 50%;
  background: #f7f8ee;
}

.lovestory__dot::after {
  content: '';
  position: absolute;
  inset: calc(3 * var(--px));
  border-radius: 50%;
  background: var(--crimson);
}

/* An arched frame, the top rounded off like a window. */
.lovestory__photo {
  margin: 0 0 calc(12 * var(--px));
  width: 100%;
  aspect-ratio: 4 / 3;
  padding: calc(4 * var(--px));
  border: 1px solid color-mix(in srgb, var(--gold) 70%, transparent);
  border-radius: calc(120 * var(--px)) calc(120 * var(--px)) calc(6 * var(--px)) calc(6 * var(--px));
  overflow: hidden;
}

.lovestory__photo img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: inherit;
}

.lovestory__date {
  margin: 0;
  font-family: var(--font-caps);
  font-size: calc(11 * var(--px));
  letter-spacing: 0.08em;
  line-height: calc(18 * var(--px));
  color: var(--gold);
}

.lovestory__name {
  margin: calc(2 * var(--px)) 0 0;
  font-family: var(--font-heading);
  font-size: calc(26 * var(--px));
  font-weight: 400;
  line-height: calc(30 * var(--px));
  color: var(--crimson);
}

.lovestory__text {
  margin: calc(6 * var(--px)) 0 0;
  font-family: var(--font-body);
  font-size: calc(13 * var(--px));
  line-height: 1.55;
  white-space: pre-line;
  color: var(--bronze);
}

/* Same entrance as the bands' copy. */
.lovestory__head,
.lovestory__item {
  opacity: 0;
  transform: translateY(calc(24 * var(--px)));
  transition:
    opacity 1200ms cubic-bezier(0.16, 1, 0.3, 1),
    transform 1600ms cubic-bezier(0.16, 1, 0.28, 1);
}

.lovestory__head.is-in,
.lovestory__item.is-in {
  opacity: 1;
  transform: none;
}

@media (prefers-reduced-motion: reduce) {
  .lovestory__head,
  .lovestory__item {
    opacity: 1;
    transform: none;
    transition: none;
  }
}
</style>
