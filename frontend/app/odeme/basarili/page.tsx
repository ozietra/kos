import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Link from 'next/link'
import Icon from '@/components/Icon'

export const metadata: Metadata = {
  title: 'Ödeme Başarılı — kosgebhibe.com',
  robots: { index: false },
}

export default function OdemeBasariliPage() {
  return (
    <>
      <Header />
      <main style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', padding: '60px 20px' }}>
        <div style={{ maxWidth: '520px', margin: '0 auto', textAlign: 'center' }}>
          <div style={{ marginBottom: '20px', color: 'var(--color-success)', display: 'flex', justifyContent: 'center' }}>
            <Icon name="checkCircle" size={64} strokeWidth={1.5} />
          </div>
          <h1 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '12px' }}>
            Ödemeniz Alındı!
          </h1>
          <p style={{ color: 'var(--color-text-secondary)', marginBottom: '24px' }}>
            Teşekkürler! Başvurunuza erişim sağlandı. Onay e-postası kayıtlı adresinize gönderildi.
          </p>
          <Link href="/dashboard" className="btn btn-primary btn-lg">
            Başvuruma Git
          </Link>
          <p style={{ fontSize: '12px', color: 'var(--color-text-muted)', marginTop: '16px' }}>
            E-posta gelmedi mi? Spam klasörünü kontrol edin.
          </p>
        </div>
      </main>
      <Footer />
    </>
  )
}
