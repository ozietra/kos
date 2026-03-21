import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        // Standart arama motorları — tam erişim
        userAgent: '*',
        allow: '/',
        disallow: ['/dashboard/', '/api/', '/giris', '/uye-ol'],
      },
      {
        // AI arama botları — blog ve programlar sayfalarına izin
        userAgent: ['OAI-SearchBot', 'ChatGPT-User', 'PerplexityBot', 'YouBot', 'AI2Bot'],
        allow: ['/', '/blog/', '/kosgeb-programlari', '/uygunluk-testi', '/nace-kodu-sorgula'],
        disallow: ['/dashboard/', '/api/'],
      },
      {
        // AI eğitim botları — içerik sıyırmayı engelle (KVKK uyumu)
        userAgent: ['GPTBot', 'Google-Extended', 'CCBot', 'anthropic-ai', 'Claude-Web'],
        disallow: '/',
      },
    ],
    sitemap: 'https://kosgebhibe.com/sitemap.xml',
  }
}
