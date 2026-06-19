/**
 * Server-only API yardımcısı (SSR / sunucu bileşenleri için).
 * Tarayıcı rewrite'ı (/api → backend) yalnızca istemcide çalışır; sunucuda
 * backend'e mutlak URL ile gidilir. Backend düşse bile sayfa kırılmasın diye
 * tüm fonksiyonlar hata halinde null döner ve çağıran taraf fallback kullanır.
 */
const BASE =
  process.env.INTERNAL_API_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  'http://localhost:8000'

async function getJson<T>(path: string, revalidate = 30): Promise<T | null> {
  try {
    const res = await fetch(`${BASE}${path}`, { next: { revalidate } })
    if (!res.ok) return null
    return (await res.json()) as T
  } catch {
    return null
  }
}

export interface HomeStat {
  key: string
  label: string | null
  value: string | null
}
export interface HomeContent {
  hero_badge: string
  stats: HomeStat[]
}
export interface PricingPlanPublic {
  code: string
  name: string
  description: string | null
  features: string[]
  currency: string
  price: number
  effective_price: number
  is_campaign: boolean
  campaign_label: string | null
  campaign_end: string | null
  is_active: boolean
}

export interface SeoSettings {
  ga_id: string
  gsc_verification: string
}

export const getHomeContent = () => getJson<HomeContent>('/api/content/home')
export const getPricing = () => getJson<{ plans: PricingPlanPublic[] }>('/api/content/pricing')
export const getSeo = () => getJson<SeoSettings>('/api/content/seo')
