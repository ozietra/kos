import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Ödeme Başarısız — kosgebhibe.com',
  robots: { index: false },
}

export default function OdemeBasarisizPage() {
  return (
    <>
      <Header />
      <main style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', padding: '60px 20px' }}>
        <div style={{ maxWidth: '520px', margin: '0 auto', textAlign: 'center' }}>
          <div style={{ fontSize: '60px', marginBottom: '20px' }}>❌</div>
          <h1 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '12px' }}>
            Ödeme Alınamadı
          </h1>
          <p style={{ color: 'var(--color-text-secondary)', marginBottom: '24px' }}>
            Ödeme işlemi tamamlanamadı. Kart bilgilerinizi veya limitinizi kontrol ederek tekrar deneyebilirsiniz.
            Başvurunuz kaydedilmiştir; istediğiniz zaman geri dönebilirsiniz.
          </p>
          <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link href="/dashboard" className="btn btn-secondary">
              Panele Dön
            </Link>
            <Link href="javascript:history.back()" className="btn btn-primary">
              Tekrar Dene
            </Link>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
