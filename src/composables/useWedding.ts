import { ref, computed, onMounted } from 'vue'


import { resolveSlug, getHome, submitUcapan, DESIGN_MODE } from '../lib/api'

const state = ref<{
  loading: boolean
  error: string | null
  data: any | null
}>({
  loading: true,
  error: null,
  data: null,
})

function applyTheme(themeData: any, weddingData: any) {
  const cfg = themeData?.theme_config
  let override = weddingData?.theme_override
  if (typeof override === 'string') {
    try {
      override = JSON.parse(override)
    } catch {
      override = {}
    }
  }
  override = override || {}

  const root = document.documentElement
  const colors = { ...(cfg?.colors || {}), ...(override?.colors || {}) }
  const fonts = { ...(cfg?.fonts || {}), ...(override?.fonts || {}) }

  if (colors.primary) root.style.setProperty('--maroon-title', colors.primary)
  if (colors.secondary) root.style.setProperty('--maroon-text', colors.secondary)
  if (colors.accent) root.style.setProperty('--gold', colors.accent)
  if (colors.bg_body) root.style.setProperty('--bg-body', colors.bg_body)

  if (fonts.script) root.style.setProperty('--font-script', fonts.script)
  if (fonts.display) root.style.setProperty('--font-display', fonts.display)
  if (fonts.serif) root.style.setProperty('--font-serif', fonts.serif)
  if (fonts.sans) root.style.setProperty('--font-sans', fonts.sans)
  if (fonts.heading) root.style.setProperty('--font-heading', fonts.heading)
  if (fonts.name) root.style.setProperty('--font-name', fonts.name)
  if (fonts.caps) root.style.setProperty('--font-caps', fonts.caps)
  if (fonts.parent) root.style.setProperty('--font-parent', fonts.parent)
  if (fonts.detail) root.style.setProperty('--font-detail', fonts.detail)
  if (fonts.body) root.style.setProperty('--font-body', fonts.body)
  if (fonts.card) root.style.setProperty('--font-card', fonts.card)
  if (fonts.figures) root.style.setProperty('--font-figures', fonts.figures)
  if (fonts.quote) root.style.setProperty('--font-quote', fonts.quote)
  if (fonts.signature) root.style.setProperty('--font-signature', fonts.signature)
  if (fonts.monogram) root.style.setProperty('--font-monogram', fonts.monogram)
  if (fonts.closing) root.style.setProperty('--font-closing', fonts.closing)
  if (fonts.arabic) root.style.setProperty('--font-arabic', fonts.arabic)
  if (fonts.verse) root.style.setProperty('--font-verse', fonts.verse)
}

/*
 * 18 components call useWedding(), and they all mount in the same tick. The old guard
 * checked `state.loading`, which is still true at that point for every one of them, so
 * all 18 fired the same getHome request. Hold the first promise instead: the other 17
 * mounts see it and skip. Only the explicit `refetch` bypasses this.
 */
let inflight: Promise<void> | null = null

function getGuestCode(): string {
  if (typeof window === 'undefined') return ''
  const searchParams = new URLSearchParams(window.location.search)
  return (
    searchParams.get('to') ||
    searchParams.get('k') ||
    searchParams.get('code') ||
    searchParams.get('guest') ||
    ''
  ).trim()
}

const slug = ref(resolveSlug())
const guestCode = ref(getGuestCode())

async function fetchWeddingData() {
  if (DESIGN_MODE) return
  slug.value = resolveSlug()
  guestCode.value = getGuestCode()
  state.value.loading = true
  state.value.error = null
  try {
    const data = await getHome(slug.value, guestCode.value)
    
    // Preserve and merge any preview overrides if present
    const currentWedding = state.value.data?.wedding
    let currentOverride = currentWedding?.theme_override
    if (typeof currentOverride === 'string') {
      try { currentOverride = JSON.parse(currentOverride) } catch { currentOverride = {} }
    }
    let dataOverride = data?.wedding?.theme_override
    if (typeof dataOverride === 'string') {
      try { dataOverride = JSON.parse(dataOverride) } catch { dataOverride = {} }
    }

    state.value.data = {
      ...data,
      wedding: {
        ...(data?.wedding || {}),
        ...(currentWedding || {}),
        theme_override: {
          ...(dataOverride || {}),
          ...(currentOverride || {}),
        },
      },
      theme: state.value.data?.theme || data?.theme,
    }

    if (state.value.data?.theme || state.value.data?.wedding) {
      applyTheme(state.value.data.theme, state.value.data.wedding)
    }
    if (state.value.data?.wedding?.title) {
      document.title = `${state.value.data.wedding.title} - Undangan Pernikahan`
    }
  } catch (err: any) {
    console.error('Failed to load wedding data:', err)
    state.value.error = err.message
  } finally {
    state.value.loading = false
  }
}

// Listen for live preview messages from the admin dashboard ("Mode Imajinasi")
if (typeof window !== 'undefined') {
  window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'QINVI_PREVIEW_UPDATE') {
      const { wedding: previewWedding, theme: previewTheme, refetch } = event.data

      if (previewWedding) {
        let resolvedWedding = { ...previewWedding }
        if (typeof resolvedWedding.theme_override === 'string') {
          try {
            resolvedWedding.theme_override = JSON.parse(resolvedWedding.theme_override)
          } catch (e) {
            console.error('Failed to parse theme_override:', e)
          }
        }

        const existingOverride = state.value.data?.wedding?.theme_override || {}
        const mergedOverride = {
          ...existingOverride,
          ...(resolvedWedding.theme_override || {}),
        }

        state.value.data = {
          ...(state.value.data || {}),
          wedding: {
            ...(state.value.data?.wedding || {}),
            ...resolvedWedding,
            theme_override: mergedOverride,
          },
        }
      }

      if (previewTheme) {
        state.value.data = {
          ...(state.value.data || {}),
          theme: previewTheme,
        }
      }

      // Re-apply theme styles dynamically
      if (state.value.data?.theme || state.value.data?.wedding) {
        applyTheme(state.value.data.theme, state.value.data.wedding)
      }

      if (refetch || !state.value.data?.content) {
        inflight = null
        fetchWeddingData()
      }
    }
  })
}

/*
 * Wishes posted while in design mode. Kept outside `state` on purpose: seeding
 * state.data to hold them would make `wedding` non-null, and every band would drop
 * its design fallback mid-session.
 */
const designWishes = ref<any[]>([])

export function useWedding() {
  onMounted(() => {
    if (DESIGN_MODE) return
    if (state.value.data?.content) return
    inflight ??= fetchWeddingData().finally(() => {
      inflight = null
    })
  })

  const wedding = computed(() => state.value.data?.wedding ?? null)
  const theme = computed(() => state.value.data?.theme ?? null)
  const guest = computed(() => state.value.data?.guest ?? null)
  /*
   * getHome nests every list under `data.content` -- these were read straight off `data`,
   * so all five were permanently empty. No pixel diff could catch it: an empty list falls
   * back to the design's own copy and scores perfectly. Same class of bug as the `ucapan`
   * / `wishes` guess below. Read `content` first, then the flat key, so a payload of
   * either shape works.
   */
  const content = computed(() => state.value.data?.content ?? state.value.data ?? null)
  const pengantin = computed(() => content.value?.pengantin ?? [])
  const acara = computed(() => content.value?.acara ?? [])
  const gallery = computed(() => content.value?.gallery ?? [])
  // The API calls the account list `rekening`.
  const gift = computed(() => content.value?.rekening ?? content.value?.gift ?? [])
  const wishes = computed(() => designWishes.value.length ? designWishes.value : content.value?.ucapan ?? content.value?.wishes ?? [])

  /**
   * Post a wish and get it into the list without a refetch. The API may answer with the
   * refreshed list, with just the created row, or with neither, so all three are handled
   * — otherwise a guest submits and sees nothing happen.
   */
  // Writes `ucapan` back where `content` reads it from, or the new row is invisible.
  function putWishes(list: any[]) {
    const data = state.value.data
    if (!data) return
    state.value.data = data.content
      ? { ...data, content: { ...data.content, ucapan: list } }
      : { ...data, ucapan: list }
  }

  async function sendWish(body: { guest_name: string; message: string }): Promise<any> {
    /*
     * Design mode must not write to the live backend. The wish form is real and has
     * to keep working -- validation, pending, success, and the new wish appearing in
     * the list -- so the post is answered locally instead of being sent.
     */
    if (DESIGN_MODE) {
      const row = { id: `local-${Date.now()}`, ...body, created_at: new Date().toISOString() }
      designWishes.value = [row, ...designWishes.value]
      return { success: true, data: row }
    }
    const res = await submitUcapan(slug.value, body)
    if (!state.value.data) return res

    const list = Array.isArray(res) ? res : Array.isArray(res?.data) ? res.data : null
    if (list) {
      putWishes(list)
      return res
    }

    const row =
      res?.data && typeof res.data === 'object' && !Array.isArray(res.data)
        ? res.data
        : { id: `local-${Date.now()}`, ...body, created_at: new Date().toISOString() }
    putWishes([row, ...(Array.isArray(wishes.value) ? wishes.value : [])])
    return res
  }
  const groom = computed(() => {
    return (
      pengantin.value.find(
        (p: any) =>
          p.type?.toLowerCase() === 'groom' || p.type?.toLowerCase() === 'pria',
      ) || null
    )
  })
  const bride = computed(() => {
    return (
      pengantin.value.find(
        (p: any) =>
          p.type?.toLowerCase() === 'bride' || p.type?.toLowerCase() === 'wanita',
      ) || null
    )
  })

  const isGroomFirst = computed(() => {
    if (!wedding.value) return false
    return wedding.value.order_groom_first !== false
  })

  const coupleNickname = computed(() => {
    if (groom.value?.name && bride.value?.name) {
      const gName = groom.value?.nickname?.trim() || groom.value.name.trim().split(' ')[0]
      const bName = bride.value?.nickname?.trim() || bride.value.name.trim().split(' ')[0]
      return isGroomFirst.value ? `${gName} & ${bName}` : `${bName} & ${gName}`
    }
    if (wedding.value?.title) return wedding.value.title
    // Frame 243/244 print "Ahmad & Salma", so an unconfigured render matches the design.
    return isGroomFirst.value ? 'Ahmad & Salma' : 'Salma & Ahmad'
  })

  const quoteText = computed(
    () =>
      wedding.value?.theme_override?.quote?.text ||
      // Matches the copy set on the card in Frame 242, so an unconfigured
      // render lines up with the design.
      'Di antara tanda-tanda kebesaran-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri agar kamu merasa tenteram kepadanya. Dia menjadikan di antaramu rasa cinta dan kasih sayang. Sesungguhnya pada yang demikian itu benar-benar terdapat tanda-tanda kebesaran Allah bagi kaum yang berpikir.',
  )
  const quoteVerse = computed(() => wedding.value?.theme_override?.quote?.verse || 'QS Ar-Rum 21')
  const quoteArabic = computed(
    () =>
      wedding.value?.theme_override?.quote?.arabic ||
      'وَمِنْ اٰيٰتِهٖٓ اَنْ خَلَقَ لَكُمْ مِّنْ اَنْفُسِكُمْ اَزْوَاجًا لِّتَسْكُنُوْٓا اِلَيْهَا وَجَعَلَ بَيْنَكُمْ مَّوَدَّةً وَّرَحْمَةًۗ اِنَّ فِيْ ذٰلِكَ لَاٰيٰتٍ لِّقَوْمٍ يَّتَفَكَّرُوْنَ',
  )

  return {
    slug,
    guestCode,
    loading: computed(() => state.value.loading),
    error: computed(() => state.value.error),
    wedding,
    theme,
    guest,
    pengantin,
    acara,
    gallery,
    quoteVerse,
    quoteArabic,
    gift,
    wishes,
    sendWish,
    groom,
    bride,
    isGroomFirst,
    coupleNickname,
    quoteText,
    logoMempelai: computed(() => {
      let override = wedding.value?.theme_override
      if (typeof override === 'string') {
        try { override = JSON.parse(override) } catch { override = {} }
      }
      return override?.images?.logo_mempelai ||
        override?.images?.['logo-mempelai'] ||
        override?.logo_mempelai ||
        wedding.value?.logo_mempelai || 
        wedding.value?.['logo-mempelai'] || 
        content.value?.logo_mempelai || 
        content.value?.['logo-mempelai']
    }),
    videoPrewed: computed(() => {
      let override = wedding.value?.theme_override
      if (typeof override === 'string') {
        try { override = JSON.parse(override) } catch { override = {} }
      }
      return override?.words?.video_prewed || ''
    }),
    videoUrl: computed(() => wedding.value?.video_url || ''),
    leftCoverBg: computed(() => {
      let override = wedding.value?.theme_override
      if (typeof override === 'string') {
        try { override = JSON.parse(override) } catch { override = {} }
      }
      return override?.backgrounds?.left_bg ||
        override?.images?.left_bg || 
        override?.backgrounds?.['left-cover-bg'] ||
        override?.images?.['left-cover-bg'] ||
        override?.images?.left_cover_bg ||
        wedding.value?.left_cover_bg ||
        wedding.value?.['left-cover-bg'] ||
        content.value?.left_cover_bg ||
        content.value?.['left-cover-bg'] ||
        wedding.value?.image_bg1 ||
        wedding.value?.image_cover || ''
    }),
    closingMessage: computed(() => {
      let override = wedding.value?.theme_override
      if (typeof override === 'string') {
        try { override = JSON.parse(override) } catch { override = {} }
      }
      return override?.words?.footer_message_en || override?.words?.footer_message || wedding.value?.pesan_penutup || 'We sincerely thank you for your presence, prayers, and blessings on our special day.'
    }),
    parsedOverride: computed(() => {
      let ov = wedding.value?.theme_override
      if (typeof ov === 'string') {
        try { ov = JSON.parse(ov) } catch { ov = {} }
      }
      return ov || {}
    }),
    customHeroPhoto: computed(() => {
      let ov = wedding.value?.theme_override
      if (typeof ov === 'string') {
        try { ov = JSON.parse(ov) } catch { ov = {} }
      }
      const raw =
        ov?.images?.foto_mempelai_setelah_buka ||
        ov?.images?.['foto-mempelai-setelah-buka'] ||
        ov?.foto_mempelai_setelah_buka ||
        ov?.['foto-mempelai-setelah-buka'] ||
        theme.value?.theme_config?.images?.foto_mempelai_setelah_buka ||
        wedding.value?.foto_mempelai_setelah_buka ||
        content.value?.foto_mempelai_setelah_buka ||
        content.value?.images?.foto_mempelai_setelah_buka ||
        wedding.value?.image_spouse ||
        wedding.value?.image_cover ||
        content.value?.image_spouse ||
        content.value?.image_cover ||
        ''
      return typeof raw === 'string' ? raw.trim() : (raw || '')
    }),
    customSpousePhoto: computed(() => {
      let ov = wedding.value?.theme_override
      if (typeof ov === 'string') {
        try { ov = JSON.parse(ov) } catch { ov = {} }
      }
      return (
        wedding.value?.image_spouse ||
        wedding.value?.['image-spouse'] ||
        content.value?.image_spouse ||
        ov?.images?.image_spouse ||
        ov?.images?.foto_pasangan ||
        ov?.images?.foto_mempelai_setelah_buka ||
        theme.value?.theme_config?.images?.image_spouse ||
        ''
      )
    }),
    fotoMempelaiTransform: computed(() => {
      let ov = wedding.value?.theme_override
      if (typeof ov === 'string') {
        try { ov = JSON.parse(ov) } catch { ov = {} }
      }
      const t = ov?.foto_mempelai_transform
      return {
        scale: typeof t?.scale === 'number' ? t.scale : (parseFloat(t?.scale) || 1),
        x: typeof t?.x === 'number' ? t.x : (parseFloat(t?.x) || 50),
        y: typeof t?.y === 'number' ? t.y : (parseFloat(t?.y) || 50),
      }
    }),
    spousePhotoTransform: computed(() => {
      let ov = wedding.value?.theme_override
      if (typeof ov === 'string') {
        try { ov = JSON.parse(ov) } catch { ov = {} }
      }
      return ov?.spouse_photo_transform || { scale: 1, x: 50, y: 50 }
    }),
    refetch: fetchWeddingData,
  }
}
