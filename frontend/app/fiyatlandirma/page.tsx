import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Link from 'next/link'
import { getPricing } from '@/lib/serverApi'

export const metadata: Metadata = {
  title: 'Fiyatlandırma — kosgebhibe.com | KOSGEB Başvurusu',
  description: 'kosgebhibe.com fiyatlandırma planları. KOSGEB hibe başvurusu hazırlama hizmetleri.',
}

const FREE_PLAN = {
  name: 'Ücretsiz',
  desc: 'Uygunluk testi + bilgi bankası',
  features: ['Uygunluk testi (sınırsız)', 'NACE kodu sorgulama', 'Aktif program takvimi', 'Blog rehberleri'],
  href: '/uye-ol',
}

function fmt(n: number, currency: string) {
  const s = Number.isInteger(n) ? n.toLocaleString('tr-TR') : n.toLocaleString('tr-TR', { minimumFractionDigits: 2 })
  return `${s} ${currency === 'TRY' ? '₺' : currency}`
}

export default async function FiyatlandirmaPage() {
  const pricing = await getPricing()
  const paidPlans = pricing?.plans ?? []

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

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px' }}>
            {/* Ücretsiz plan (statik) */}
            <div className="card" style={{ position: 'relative' }}>
              <div style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-success)', marginBottom: '6px' }}>{FREE_PLAN.name}</div>
              <div style={{ fontSize: '32px', fontWeight: 800, marginBottom: '4px', fontFamily: 'JetBrains Mono, monospace' }}>Ücretsiz</div>
              <div style={{ fontSize: '13px', color: 'var(--color-text-muted)', marginBottom: '20px' }}>{FREE_PLAN.desc}</div>
              <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 24px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {FREE_PLAN.features.map(f => (
                  <li key={f} style={{ fontSize: '14px', display: 'flex', gap: '8px', alignItems: 'flex-start', color: 'var(--color-text-secondary)' }}>
                    <span style={{ color: 'var(--color-success)', flexShrink: 0 }}>✓</span> {f}
                  </li>
                ))}
              </ul>
              <a href={FREE_PLAN.href} className="btn btn-outline" style={{ display: 'block', textAlign: 'center' }}>Hemen Başla</a>
            </div>

            {/* Ücretli planlar (backend'den dinamik) */}
            {paidPlans.map((plan, i) => {
              const highlight = i === 0
              return (
                <div key={plan.code} className="card" style={{ outline: highlight ? '2px solid var(--color-accent)' : undefined, position: 'relative' }}>
                  {plan.is_campaign && (
                    <div style={{ position: 'absolute', top: '-14px', left: '50%', transform: 'translateX(-50%)', background: 'var(--color-accent)', color: '#fff', fontSize: '12px', fontWeight: 700, padding: '3px 14px', borderRadius: '100px', whiteSpace: 'nowrap' }}>
                      {plan.campaign_label || 'Kampanya'}
                    </div>
                  )}
                  <div style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--color-accent)', marginBottom: '6px' }}>{plan.name}</div>
                  <div style={{ fontSize: '32px', fontWeight: 800, marginBottom: '4px', fontFamily: 'JetBrains Mono, monospace' }}>
                    {plan.is_campaign && (
                      <span style={{ textDecoration: 'line-through', opacity: 0.45, fontSize: '0.6em', marginRight: 8 }}>{fmt(plan.price, plan.currency)}</span>
                    )}
                    {fmt(plan.effective_price, plan.currency)}
                  </div>
                  <div style={{ fontSize: '13px', color: 'var(--color-text-muted)', marginBottom: '20px' }}>
                    {plan.is_campaign && plan.campaign_end ? `Kampanya bitiş: ${plan.campaign_end}` : (plan.description || 'Tek seferlik, KDV dahil')}
                  </div>
                  <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 24px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    {plan.features.map(f => (
                      <li key={f} style={{ fontSize: '14px', display: 'flex', gap: '8px', alignItems: 'flex-start', color: 'var(--color-text-secondary)' }}>
                        <span style={{ color: 'var(--color-success)', flexShrink: 0 }}>✓</span> {f}
                      </li>
                    ))}
                  </ul>
                  <a href={`/uye-ol?plan=${plan.code}`} className={`btn btn-${highlight ? 'primary' : 'outline'}`} style={{ display: 'block', textAlign: 'center' }}>Hemen Başla</a>
                </div>
              )
            })}
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
