import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export const metadata: Metadata = {
  title: 'Mesafeli Satış Sözleşmesi — kosgebhibe.com',
  description: 'kosgebhibe.com mesafeli satış sözleşmesi metni.',
}

export default function MesafeliSatisPage() {
  return (
    <>
      <Header />
      <main style={{ padding: '60px 0 80px' }}>
        <div className="container" style={{ maxWidth: '720px' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '32px' }}>
            Mesafeli Satış Sözleşmesi
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-muted)', marginBottom: '32px' }}>
            Son güncelleme: Mart 2026
          </p>

          <div className="legal-content">
            <h2>1. Taraflar</h2>
            <p>
              <strong>Satıcı:</strong> kosgebhibe.com platformu<br />
              <strong>Alıcı:</strong> Platformu satın alma amacıyla kullanan kişi
            </p>

            <h2>2. Sözleşme Konusu</h2>
            <p>
              Bu sözleşme, Alıcı'nın kosgebhibe.com platformu üzerinden satın aldığı
              dijital hizmet (KOSGEB başvuru dosyası hazırlama) için geçerlidir.
            </p>

            <h2>3. Hizmet ve Ücret</h2>
            <ul>
              <li><strong>Starter Plan:</strong> 499 ₺ (KDV dahil) — KOSGEB başvuru dosyası + PDF çıktısı</li>
            </ul>

            <h2>4. Teslimat</h2>
            <p>
              Ödeme onaylandıktan sonra hizmet anında aktif edilir. Başvuru dosyası
              PDF formatında platform üzerinden indirilebilir.
            </p>

            <h2>5. Cayma Hakkı</h2>
            <p>
              6502 sayılı Tüketicinin Korunması Hakkında Kanun'un 49. maddesi uyarınca,
              dijital içeriklerin teslimi alıcının onayıyla başlandığında cayma hakkı
              kullanılamaz. PDF dosyası indirildiğinde iade yapılmamaktadır.
            </p>
            <p>
              PDF indirilmeden önce sorun yaşanması halinde 7 gün içinde{' '}
              <a href="mailto:destek@kosgebhibe.com">destek@kosgebhibe.com</a> ile iletişime geçebilirsiniz.
            </p>

            <h2>6. Uyuşmazlık</h2>
            <p>
              Bu sözleşmeden doğan uyuşmazlıklarda Türkiye Cumhuriyeti mahkemeleri
              ve Tüketici Hakem Heyetleri yetkilidir.
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
