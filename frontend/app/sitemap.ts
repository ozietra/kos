import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://kosgebhibe.com'
  const now = new Date()

  // Tanıtım / araç sayfaları (indekslenmeli)
  const corePages = [
    { url: `${baseUrl}/`, changeFrequency: 'weekly' as const, priority: 1.0 },
    { url: `${baseUrl}/uygunluk-testi`, changeFrequency: 'monthly' as const, priority: 0.9 },
    { url: `${baseUrl}/nace-kodu-sorgula`, changeFrequency: 'monthly' as const, priority: 0.85 },
    { url: `${baseUrl}/fiyatlandirma`, changeFrequency: 'monthly' as const, priority: 0.75 },
    { url: `${baseUrl}/demo`, changeFrequency: 'monthly' as const, priority: 0.6 },
    { url: `${baseUrl}/blog`, changeFrequency: 'weekly' as const, priority: 0.8 },
  ]

  // Yasal / bilgilendirme sayfaları (düşük öncelik ama indekslensin — güven sinyali)
  const legalPages = [
    'kvkk',
    'gizlilik',
    'kullanim-kosullari',
    'kullanim-sartlari',
    'mesafeli-satis',
  ].map((p) => ({
    url: `${baseUrl}/${p}`,
    changeFrequency: 'yearly' as const,
    priority: 0.3,
  }))

  // Yayında olan blog makaleleri (blog/[slug]/page.tsx içindeki CONTENT ile birebir)
  const blogSlugs = [
    'kosgeb-is-plani-nasil-yazilir',
    'yesil-sanayi-mi-dijital-donusum-mu',
    'kosgeb-basvurusu-reddedilirse-ne-yapmali',
    'kadin-girisimci-kosgeb-destekleri-2026',
    'kosgeb-hibe-basvurusu-nasil-yapilir',
    'kosgeb-2026-destekleri',
    'kosgeb-icin-nace-kodu-nasil-belirlenir',
    'kosgeb-is-gelistirme-destegi-nedir',
    'kobigel-2026-basvuru-rehberi',
    'kosgeb-basvurularinda-en-cok-yapilan-hatalar',
    'kosgeb-kaydi-nasil-yapilir',
    'kosgeb-hibe-miktarlari-2026',
  ]
  const blogPages = blogSlugs.map((slug) => ({
    url: `${baseUrl}/blog/${slug}`,
    changeFrequency: 'monthly' as const,
    priority: 0.7,
  }))

  return [...corePages, ...legalPages, ...blogPages].map((p) => ({ ...p, lastModified: now }))
}
