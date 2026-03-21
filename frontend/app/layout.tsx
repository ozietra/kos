import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: {
    default: 'kosgebhibe.com — KOSGEB Hibe Başvurusu Hazırlık Platformu',
    template: '%s | kosgebhibe.com',
  },
  description:
    'KOSGEB hibe başvurunuzu danışman olmadan hazırlayın. Uygunluk analizi, başvuru metni ve belge listesi — 499 ₺ ile.',
  keywords: ['kosgeb hibe', 'kosgeb başvuru', 'kosgeb 2026', 'kosgeb iş geliştirme desteği', 'kobigel başvuru'],
  metadataBase: new URL('https://kosgebhibe.com'),
  icons: {
    icon: '/icon.png',
    apple: '/apple-icon.png',
    shortcut: '/icon.png',
  },
  openGraph: {
    siteName: 'kosgebhibe.com',
    locale: 'tr_TR',
    type: 'website',
    images: [
      {
        url: '/og-image.png',
        width: 512,
        height: 512,
        alt: 'kosgebhibe.com',
      },
    ],
  },
  twitter: {
    card: 'summary',
    title: 'kosgebhibe.com — KOSGEB Hibe Başvurusu Hazırlık Platformu',
    description: 'KOSGEB başvurunuzu danışman olmadan 499 ₺\'ye hazırlayın.',
    images: ['/og-image.png'],
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr" data-scroll-behavior="smooth">
      <body>{children}</body>
    </html>
  )
}
