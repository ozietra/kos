import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Fiyatlandırma — kosgebhibe.com | 499 ₺ KOSGEB Başvurusu',
  description: 'kosgebhibe.com fiyatlandırma planları. Starter 499 ₺, Pro 999 ₺. KOSGEB hibe başvurusu hazırlama.',
}

const PLANS = [
  {
    name: 'Ücretsiz',
    price: '0',
    desc: 'Uygunluk testi + bilgi bankası',
    features: ['Uygunluk testi (sınırsız)', 'NACE kodu sorgulama', 'Aktif program takvimi', 'Blog rehberleri'],
    cta: 'Hemen Başla',
    href: '/uye-ol',
    highlight: false,
  },
  {
    name: 'Starter',
    price: '499',
    desc: 'Tek seferlik, KDV dahil',
    features: ['Uygunluk analizi', 'AI destekli proje özeti', 'İş planı + finansal projeksiyon', 'PDF başvuru dosyası', '30 gün erişim'],
    cta: 'Hemen Başla',
    href: '/uye-ol',
    highlight: true,
  },
]

export default function FiyatlandirmaPage() {
  return (
    <>
      <Header />
      <main style={{ padding: '60px 0 80px' }}>
        <div className="container" style={{ maxWidth: '720px' }}>
          <div style={{ textAlign: 'center', marginBottom: '48px' }}>
            <h1 className="section-title">Fiyatlandırma</h1>
            <p className="text-secondary" style={{ marginTop: '12px' }}>
              Danışmanlara 5.000–20.000 ₺ ödemeden başvurunuzu hazırlayın.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px' }}>
            {PLANS.map(plan => (
              <div key={plan.name} className="card" style={{
                outline: plan.highlight ? '2px solid var(--color-accent)' : undefined,
                position: 'relative',
              }}>
                {plan.highlight && (
                  <div style={{
                    position: 'absolute', top: '-14px', left: '50%', transform: 'translateX(-50%)',
                    background: 'var(--color-accent)', color: '#fff',
                    fontSize: '12px', fontWeight: 700, padding: '3px 14px', borderRadius: '100px',
                    whiteSpace: 'nowrap',
                  }}>
                    En Popüler
                  </div>
                )}
                <div style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: plan.highlight ? 'var(--color-accent)' : 'var(--color-success)', marginBottom: '6px' }}>{plan.name}</div>
                <div style={{ fontSize: '32px', fontWeight: 800, marginBottom: '4px', fontFamily: 'JetBrains Mono, monospace' }}>
                  {plan.price === '0' ? 'Ücretsiz' : `${plan.price} ₺`}
                </div>
                <div style={{ fontSize: '13px', color: 'var(--color-text-muted)', marginBottom: '20px' }}>{plan.desc}</div>
                <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 24px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {plan.features.map(f => (
                    <li key={f} style={{ fontSize: '14px', display: 'flex', gap: '8px', alignItems: 'flex-start', color: 'var(--color-text-secondary)' }}>
                      <span style={{ color: 'var(--color-success)', flexShrink: 0 }}>✓</span> {f}
                    </li>
                  ))}
                </ul>
                <a href={plan.href} className={`btn btn-${plan.highlight ? 'primary' : 'outline'}`}
                  style={{ display: 'block', textAlign: 'center' }}>
                  {plan.cta}
                </a>
              </div>
            ))}
          </div>

          <p className="legal-note" style={{ marginTop: '32px' }}>
            Tüm fiyatlar KDV dahildir. İade politikası için{' '}
            <Link href="/mesafeli-satis">Mesafeli Satış Sözleşmesi</Link>&apos;ni inceleyebilirsiniz.
          </p>
        </div>
      </main>
      <Footer />
    </>
  )
}
