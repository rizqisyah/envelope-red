<script setup lang="ts">
// Figma Frame 253 band "rsvp", y 6024–6414. Coords are band-local design px.
//
// The three fields are `Input` frames in Figma with a flat #6b0d0e fill and the sample
// answer typed inside. They ship as real inputs, not as art — a raster of a form cannot
// be filled in — so 2852:389 is skipped and all three plates are CSS.
import { computed, onMounted, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { submitRsvp } from '../../lib/api'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/rsvp'

const { el, shown } = useReveal(0.15)
const { slug, guest } = useWedding()

/*
 * Redrawn below, so the rasters are skipped: 2852:389 is the third field's plate (the
 * other two are frames Figma never exported at all) and 2852:387 is the Send button's.
 * Leaving 2852:387 in the table put a stray 115x32 wine rectangle on the page that only
 * looked fine because it happened to land on the select, which is the same colour.
 */
const SKIP = ['2852:389', '2852:387']

const name = ref('')
const phone = ref('')
const attendance = ref('')
const guestCount = ref('1')
const sending = ref(false)
const error = ref('')
const done = ref(false)
const showPopup = ref(false)

/* The `?to=` link names the guest, so the field starts filled in for them. */
onMounted(() => {
  const known = guest.value?.name || new URLSearchParams(location.search).get('to')
  if (known) name.value = String(known)
})

const canSend = computed(() => !!name.value.trim() && !!attendance.value && !sending.value)

async function send() {
  error.value = ''
  if (!name.value.trim()) {
    error.value = 'Nama masih kosong.'
    return
  }
  if (!attendance.value) {
    error.value = 'Pilih kehadiran dulu.'
    return
  }
  sending.value = true
  try {
    await submitRsvp(slug.value, {
      guest_name: name.value.trim(),
      phone: phone.value.trim(),
      attendance_status: attendance.value,
      guest_count: attendance.value === 'hadir' ? parseInt(guestCount.value) || 1 : 0,
    })
    done.value = true
    showPopup.value = true
  } catch (err: any) {
    error.value = err?.message || 'Gagal mengirim. Coba lagi.'
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <section :ref="el" class="band rsvp" :class="{ 'is-in': shown }" aria-labelledby="rsvp-heading">
    <BandArt :layers="LAYERS" :skip="SKIP" :shown="shown" />

    <!-- 2852:386 — Alex Brush 48/28, #9a1010. -->
    <h2 id="rsvp-heading" class="rsvp__heading">Reservation</h2>
    <!-- 2852:385 — EB Garamond 16/20, #6b0d0e. -->
    <p class="rsvp__copy">Mohon konfirmasi kehadiran Anda melalui formulir reservasi di bawah:</p>

    <form class="rsvp__form" novalidate @submit.prevent="send">
      <!-- 2852:391 / 2852:394 -->
      <label class="rsvp__label rsvp__label--name" for="rsvp-name">Nama:</label>
      <input
        id="rsvp-name"
        v-model="name"
        class="rsvp__field rsvp__field--name"
        type="text"
        autocomplete="name"
        placeholder="Maria &amp; Suami"
      />

      <!-- 2852:392 / 2852:393 -->
      <label class="rsvp__label rsvp__label--phone" for="rsvp-phone">No Hp:</label>
      <input
        id="rsvp-phone"
        v-model="phone"
        class="rsvp__field rsvp__field--phone"
        type="tel"
        inputmode="tel"
        autocomplete="tel"
        placeholder="08451515151515151"
      />

      <!-- 2852:390 / 2852:389 -->
      <label class="rsvp__label rsvp__label--going" for="rsvp-going">Kehadiran</label>
      <select id="rsvp-going" v-model="attendance" class="rsvp__field rsvp__field--going" :class="{ 'is-half': attendance === 'hadir' }">
        <option value="" disabled>Pilih</option>
        <option value="hadir">Hadir</option>
        <option value="tidak">Tidak hadir</option>
      </select>

      <label v-if="attendance === 'hadir'" class="rsvp__label rsvp__label--count" for="rsvp-count">Tamu</label>
      <select v-if="attendance === 'hadir'" id="rsvp-count" v-model="guestCount" class="rsvp__field rsvp__field--count">
        <option value="1">1 Orang</option>
        <option value="2">2 Orang</option>
        <option value="3">3 Orang</option>
        <option value="4">4 Orang</option>
        <option value="5">5 Orang</option>
      </select>

      <!-- 2852:387 plate + 2852:388 Jost 13/16.8, #f4e8c1. -->
      <button class="rsvp__send" type="submit" :disabled="!canSend">
        {{ done ? 'Terkirim' : sending ? 'Mengirim…' : 'Send' }}
      </button>
    </form>

    <p v-if="error" class="rsvp__error" role="alert">{{ error }}</p>

    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showPopup" class="success-popup">
          <div class="success-popup__box">
            <svg viewBox="0 0 24 24" class="success-popup__icon"><path d="M20 6L9 17l-5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <p class="success-popup__title">Terima Kasih!</p>
            <p class="success-popup__text">Konfirmasi kehadiran Anda telah berhasil dikirim.</p>
            <button class="success-popup__close" type="button" @click="showPopup = false">Tutup</button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<style scoped>
.rsvp {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

.rsvp__heading {
  --delay: 60ms;
  left: calc(34 * var(--px));
  top: calc(38 * var(--px));
  width: calc(305 * var(--px));
  font-family: var(--font-heading);
  font-size: calc(48 * var(--px));
  font-weight: 400;
  line-height: calc(28 * var(--px));
  color: var(--crimson);
}

.rsvp__copy {
  --delay: 140ms;
  left: calc(72 * var(--px));
  top: calc(86 * var(--px));
  width: calc(231 * var(--px));
  font-family: var(--font-body);
  font-size: calc(16 * var(--px));
  line-height: calc(20 * var(--px));
  color: var(--crimson-deep);
}

/* A bare positioning box: the fields inside carry their own design coordinates. */
.rsvp__form {
  --delay: 220ms;
  inset: 0;
  width: 100%;
  height: 100%;
}

.rsvp__label {
  position: absolute;
  font-family: var(--font-quote);
  font-weight: 700;
  font-size: calc(16 * var(--px));
  line-height: calc(22.4 * var(--px));
  text-align: left;
  color: var(--crimson-deep);
}

.rsvp__label--name {
  left: calc(57 * var(--px));
  top: calc(146 * var(--px));
}

.rsvp__label--phone {
  left: calc(57 * var(--px));
  top: calc(211 * var(--px));
}

.rsvp__label--going {
  left: calc(59 * var(--px));
  top: calc(274 * var(--px));
}

/*
 * 2852:394 / 2852:393 / 2852:389 — 36px plates of flat #6b0d0e with the answer set in
 * white Cormorant Garamond, 9px in from the left edge.
 */
.rsvp__field {
  position: absolute;
  left: calc(58 * var(--px));
  width: calc(261 * var(--px));
  height: calc(36 * var(--px));
  padding: 0 calc(9 * var(--px));
  border: 0;
  border-radius: 0;
  background: #6b0d0e;
  font-family: var(--font-quote);
  font-weight: 700;
  font-size: calc(16 * var(--px));
  line-height: calc(22.4 * var(--px));
  color: #fff;
  appearance: none;
}

.rsvp__field::placeholder {
  color: rgba(255, 255, 255, 0.62);
}

.rsvp__field:focus-visible {
  outline: calc(1.5 * var(--px)) solid var(--gold-muted);
  outline-offset: calc(1 * var(--px));
}

.rsvp__field--name {
  top: calc(169 * var(--px));
}

.rsvp__field--phone {
  left: calc(57 * var(--px));
  top: calc(234 * var(--px));
}

.rsvp__field--going {
  top: calc(297 * var(--px));
  transition: width 0.3s ease;
}
.rsvp__field--going.is-half {
  width: calc(125 * var(--px));
}

.rsvp__label--count {
  left: calc(195 * var(--px));
  top: calc(274 * var(--px));
}
.rsvp__field--count {
  left: calc(194 * var(--px));
  top: calc(297 * var(--px));
  width: calc(125 * var(--px));
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateX(10px); }
  to { opacity: 1; transform: translateX(0); }
}

.rsvp__send {
  position: absolute;
  left: calc(129 * var(--px));
  top: calc(365 * var(--px));
  width: calc(115 * var(--px));
  height: calc(32 * var(--px));
  border: 0;
  background: #6b0d0e;
  cursor: pointer;
  font-family: var(--font-sans);
  font-size: calc(13 * var(--px));
  line-height: calc(16.8 * var(--px));
  color: #f4e8c1;
  transition: transform 220ms cubic-bezier(0.16, 1, 0.3, 1), opacity 220ms ease;
}

.rsvp__send:hover:not(:disabled),
.rsvp__send:focus-visible:not(:disabled) {
  transform: translateY(calc(-2 * var(--px)));
}

.rsvp__send:disabled {
  opacity: 0.55;
  cursor: default;
}

.rsvp__error {
  left: calc(34 * var(--px));
  top: calc(400 * var(--px));
  width: calc(305 * var(--px));
  font-family: var(--font-body);
  font-size: calc(12 * var(--px));
  line-height: calc(16 * var(--px));
  color: var(--crimson-deep);
}

.success-popup {
  position: fixed;
  inset: 0;
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  padding: 24px;
}
.success-popup__box {
  background: #fff;
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  width: 100%;
  max-width: 320px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  animation: popIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.success-popup__icon {
  width: 48px;
  height: 48px;
  color: var(--crimson);
  margin: 0 auto 16px;
}
.success-popup__title {
  font-family: var(--font-heading);
  font-size: 28px;
  color: var(--crimson-deep);
  margin: 0 0 8px;
}
.success-popup__text {
  font-family: var(--font-body);
  font-size: 14px;
  color: #444;
  margin: 0 0 24px;
  line-height: 1.5;
}
.success-popup__close {
  background: var(--crimson-deep);
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  font-family: var(--font-sans);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.success-popup__close:hover {
  opacity: 0.85;
}

@keyframes popIn {
  from { transform: scale(0.9); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
