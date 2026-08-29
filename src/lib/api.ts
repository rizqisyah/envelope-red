const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const DEFAULT_SLUG = import.meta.env.VITE_DEFAULT_SLUG || 'demo-envelop'

export const DESIGN_MODE =
  import.meta.env.VITE_DESIGN_MODE === '1' || import.meta.env.VITE_DESIGN_MODE === 'true'

export function resolveSlug(): string {
  const searchParams = new URLSearchParams(window.location.search)
  const querySlug = searchParams.get('slug')
  if (querySlug) return querySlug

  const segments = window.location.pathname.split('/').filter(Boolean)
  if (segments.length === 0) return DEFAULT_SLUG

  const last = segments[segments.length - 1]
  if (last.toLowerCase() === 'temaenvelopred' || last.toLowerCase() === 'tema-envelop-red') {
    return DEFAULT_SLUG
  }
  return last
}

async function request(path: string, options: RequestInit = {}): Promise<any> {
  let res: Response
  try {
    res = await fetch(`${BASE_URL}${path}`, {
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
      ...options,
    })
  } catch (networkError: any) {
    throw new Error(`Network error: ${networkError.message}`)
  }

  let payload: any = null
  try {
    payload = await res.json()
  } catch {
    // Non-JSON response
  }

  if (!res.ok || (payload && payload.success === false)) {
    const message = (payload && payload.message) || `Request failed (${res.status})`
    throw new Error(message)
  }

  return payload
}

export async function getHome(slug: string, to = ''): Promise<any> {
  const query = to ? `?to=${encodeURIComponent(to)}` : ''
  const payload = await request(`/v1/service/menu/getHome/${encodeURIComponent(slug)}${query}`)
  return payload?.data ?? null
}

export async function submitRsvp(slug: string, body: any): Promise<any> {
  if (DESIGN_MODE) {
    throw new Error('Design mode: undangan ini belum terhubung ke server.')
  }
  return request(`/v1/service/menu/hadir2/${encodeURIComponent(slug)}`, {
    method: 'POST',
    body: JSON.stringify(body),
  })
}

export async function submitUcapan(slug: string, body: any): Promise<any> {
  if (DESIGN_MODE) {
    throw new Error('Design mode: undangan ini belum terhubung ke server.')
  }
  return request(`/v1/service/menu/ucapan/${encodeURIComponent(slug)}`, {
    method: 'POST',
    body: JSON.stringify(body),
  })
}
