import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://kosgebhibe.com'
  const now = new Date()

  const staticPages = [
    { url: `${baseUrl}/`, changeFrequency: 'weekly' as const, priority: 1.0, lastModified: now },
    { url: `${baseUrl}/uygunluk-testi`, changeFrequency: 'monthly' as const, priority: 0.9, lastModified: now },
    { url: `${baseUrl}/nace-kodu-sorgula`, changeFrequency: 'monthly' as const, priority: 0.85, lastModified: now },
    { url: `${baseUrl}/fiyatlandirma`, changeFrequency: 'monthly' as const, priority: 0.75, lastModified: now },
    { url: `${baseUrl}/blog`, changeFrequency: 'weekly' as const, priority: 0.8, lastModified: now },
  ]

  // Blog slugları (Bölüm 11: 52 makale)
  const blogSlugs = [
    'kosgeb-hibe-basvurusu-nasil-yapilir',
    'kosgeb-2026-destekleri',
    'kosgeb-icin-nace-kodu-nasil-belirlenir',
    'kosgeb-is-gelistirme-destegi-nedir',
    'kobigel-2026-basvuru-rehberi',
    'kosgeb-basvurularinda-en-cok-yapilan-hatalar',
    'kosgeb-kaydi-nasil-yapilir',
    'kosgeb-hibe-miktarlari-2026',
    // Diğer 44 makale yayına alındıkça buraya eklenecek
  ]

  const blogPages = blogSlugs.map(slug => ({
    url: `${baseUrl}/blog/${slug}`,
    changeFrequency: 'monthly' as const,
    priority: 0.7,
    lastModified: now,
  }))

  return [...staticPages, ...blogPages]
}
