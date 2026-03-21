import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import styles from './page.module.css'

export const metadata: Metadata = {
  title: 'Ücretsiz NACE Kodu Sorgula — KOSGEB İçin Doğru NACE',
  description:
    'İşletmeniz için doğru NACE kodunu bulun. KOSGEB başvurularında NACE kodu hatalı girilirse başvuru reddedilir.',
}

// Statik NACE kod listesi (sık kullanılan)
const POPULAR_NACE = [
  { code: '62.01', desc: 'Bilgisayar programlama faaliyetleri', eligible: true },
  { code: '47.91', desc: 'İnternet üzerinden perakende ticaret', eligible: true },
  { code: '14.13', desc: 'Diğer dış giyim eşyası imalatı', eligible: true },
  { code: '10.71', desc: 'Ekmek ve pastane ürünleri imalatı', eligible: true },
  { code: '41.20', desc: 'Konut ve konut dışı binaların inşaatı', eligible: true },
  { code: '56.10', desc: 'Restoran ve seyyar yemek hizmetleri', eligible: false },
  { code: '45.11', desc: 'Binek otomobillerin satışı', eligible: false },
  { code: '85.10', desc: 'Okul öncesi eğitim', eligible: true },
  { code: '86.90', desc: 'Diğer insan sağlığı hizmetleri', eligible: false },
  { code: '25.11', desc: 'Metal konstrüksiyonlar ve parçaları imalatı', eligible: true },
  { code: '22.19', desc: 'Diğer kauçuk ürünlerin imalatı', eligible: true },
  { code: '71.12', desc: 'Mühendislik faaliyetleri', eligible: true },
]

export default function NaceKoduSorgulaPage() {
  return (
    <>
      <Header />
      <main>
        {/* Hero */}
        <section style={{ padding: '60px 0 48px', borderBottom: '1px solid var(--color-border)' }}>
          <div className="container" style={{ maxWidth: '700px' }}>
            <h1 className="section-title" style={{ marginBottom: '12px' }}>
              NACE Kodu Sorgula
            </h1>
            <p className="text-secondary">
              KOSGEB başvurularında NACE kodu kritik öneme sahiptir. Yanlış kod girilirse başvuru reddedilebilir.
              Sektörünüzü açıklayın; sistem uygun NACE kodunu bulsun.
            </p>
            <div style={{ marginTop: '20px' }}>
              <a href="/uye-ol" className="btn btn-primary">
                Hesap Aç — NACE Önerisi Al (Ücretsiz)
              </a>
            </div>
          </div>
        </section>

        {/* Sık kullanılan NACE */}
        <section style={{ padding: '48px 0' }}>
          <div className="container" style={{ maxWidth: '900px' }}>
            <h2 className="card-title" style={{ marginBottom: '6px', fontSize: '18px' }}>
              Sık Kullanılan NACE Kodları
            </h2>
            <p className="text-secondary fs-sm" style={{ marginBottom: '20px' }}>
              Aşağıdaki tablo tahmini bilgi içermektedir. Kesin bilgi için{' '}
              <a href="https://www.tuik.gov.tr" target="_blank" rel="noopener noreferrer">TÜİK</a> veya
              muhasebeciye danışın.
            </p>
            <div className={styles.naceTable}>
              {POPULAR_NACE.map(item => (
                <div key={item.code} className={styles.naceRow}>
                  <div className={styles.naceCode}>{item.code}</div>
                  <div className={styles.naceDesc}>{item.desc}</div>
                  <span className={`badge ${item.eligible ? 'badge-success' : 'badge-danger'}`}>
                    {item.eligible ? 'KOSGEB Uygun' : 'Genelde Dışı'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA */}
        <section style={{ padding: '40px 0', background: 'var(--color-surface-2)', borderTop: '1px solid var(--color-border)' }}>
          <div className="container" style={{ maxWidth: '600px', textAlign: 'center' }}>
            <h2 className="card-title" style={{ fontSize: '18px', marginBottom: '12px' }}>
              Sektörünüzü Açıklayın, Doğru Kodu Bulalım
            </h2>
            <p className="text-secondary fs-sm" style={{ marginBottom: '20px' }}>
              Dashboard'da işletme eklerken AI destekli NACE öneri aracı ücretsiz olarak kullanılabilir.
            </p>
            <a href="/uye-ol" className="btn btn-primary">Şimdi Üye Ol</a>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
