<template>
  <div v-show="!isVideoVisible" v-if="musicUrl" class="floating-music" @click="toggleMusic">
    <img 
      src="../../assets/vinyl.png" 
      alt="Toggle Music" 
      class="vinyl-disc" 
      :class="{ 'is-spinning': playing }"
    />
    <audio
      ref="audioEl"
      :src="musicUrl"
      loop
      preload="auto"
      @play="playing = true"
      @pause="playing = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useWedding } from '../../composables/useWedding'

const { wedding } = useWedding()

const musicUrl = computed(() => wedding.value?.music_url || 'https://qinvi-worker.kesone01.workers.dev/Music/Brian McKnight - Back At One (Lyrics) (mp3cut.net).mp3')

const audioEl = ref<HTMLAudioElement | null>(null)
const playing = ref(false)
const isVideoVisible = ref(false)
let observer: IntersectionObserver | null = null

async function playMusic() {
  if (!audioEl.value) return
  try {
    await audioEl.value.play()
    playing.value = true
  } catch {
    playing.value = false
  }
}

function toggleMusic() {
  if (!audioEl.value) return
  if (playing.value) {
    audioEl.value.pause()
  } else {
    playMusic()
  }
}

onMounted(() => {
  playMusic()

  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      isVideoVisible.value = entry.isIntersecting
    })
  }, { threshold: 0.1 })

  let attempts = 0
  const checkVideo = setInterval(() => {
    const videoEl = document.querySelector('.video')
    if (videoEl) {
      observer!.observe(videoEl)
      clearInterval(checkVideo)
    }
    if (++attempts > 20) clearInterval(checkVideo)
  }, 100)
})

onBeforeUnmount(() => {
  audioEl.value?.pause()
  if (observer) observer.disconnect()
})
</script>

<style scoped>
.floating-music {
  position: fixed;
  right: 20px;
  bottom: calc(25px + env(safe-area-inset-bottom, 0px));
  z-index: 99;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  background-color: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}

.floating-music:active {
  transform: scale(0.9);
}

@media (min-width: 1025px) {
  .floating-music {
    right: auto;
    left: 40px;
    bottom: 40px;
    width: 60px;
    height: 60px;
  }
}

.vinyl-disc {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  pointer-events: none;
}

.vinyl-disc.is-spinning {
  animation: spin 3s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}
</style>
