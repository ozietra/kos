import type { Metadata } from 'next'
import Script from 'next/script'
import './globals.css'
import { getSeo } from '@/lib/serverApi'

const baseMetadata: Metadata = {
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

// Google Search Console doğrulama kodu admin panelinden gelir → <meta google-site-verification>
export async function generateMetadata(): Promise<Metadata> {
  const seo = await getSeo()
  const code = seo?.gsc_verification?.trim()
  if (!code) return baseMetadata
  return { ...baseMetadata, verification: { google: code } }
}

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const seo = await getSeo()
  const ga = seo?.ga_id?.trim()

  return (
    <html lang="tr" data-scroll-behavior="smooth">
      <body>
        {children}

        {/* Google Analytics (admin panelinden ölçüm kimliği girilince devreye girer) */}
        {ga && (
          <>
            <Script
              src={`https://www.googletagmanager.com/gtag/js?id=${ga}`}
              strategy="afterInteractive"
            />
            <Script id="ga-init" strategy="afterInteractive">
              {`window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', '${ga}');`}
            </Script>
          </>
        )}
      </body>
    </html>
  )
}
