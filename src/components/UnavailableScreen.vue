<script setup lang="ts">
// Shown in place of the whole invitation when the server refuses it. See `blocked` in
// useWedding.ts for why the invitation cannot simply render with empty data.
import { computed } from 'vue'

const props = defineProps<{ status: number; code?: string; message: string }>()

/*
 * A 403 carries a guest-facing Indonesian sentence (private link, device lock), so it is
 * shown as sent. A 404 says "Wedding not found" in English whether the invitation never
 * existed, was switched off, or its owner was deactivated — the guest gets one plain line.
 */
const body = computed(() =>
  props.status === 403 && props.message
    ? props.message
    : 'Undangan ini sudah tidak aktif atau tidak dapat ditemukan.',
)
</script>

<template>
  <section class="unavailable" role="alert">
    <h1 class="unavailable__title">Undangan Tidak Tersedia</h1>
    <p class="unavailable__body">{{ body }}</p>
  </section>
</template>

<style scoped>
.unavailable {
  display: grid;
  place-content: center;
  gap: 16px;
  min-height: 100dvh;
  padding: 32px 24px;
  text-align: center;
  background: var(--wine);
  color: var(--gold-muted);
}

.unavailable__title {
  margin: 0;
  font-family: var(--font-heading);
  font-size: 40px;
  font-weight: 400;
  line-height: 1.1;
  color: var(--gold-bright);
}

.unavailable__body {
  max-width: 32ch;
  margin: 0 auto;
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.5;
}
</style>
