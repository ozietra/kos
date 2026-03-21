import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export const metadata: Metadata = {
  title: 'Kullanım Koşulları — kosgebhibe.com',
  description: 'kosgebhibe.com platform kullanım koşulları.',
}

export default function KullanimKosullariPage() {
  return (
    <>
      <Header />
      <main style={{ padding: '60px 0 80px' }}>
        <div className="container" style={{ maxWidth: '720px' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '32px' }}>
            Kullanım Koşulları
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-muted)', marginBottom: '32px' }}>
            Son güncelleme: Mart 2026
          </p>

          <div className="legal-content">
            <h2>1. Hizmetin Kapsamı</h2>
            <p>
              kosgebhibe.com, KOSGEB hibe programları için başvuru belgesi hazırlama hizmeti sunan
              bir platformdur. Hazırlanan belgeler bilgilendirme amaçlıdır; KOSGEB tarafından onay
              garantisi verilmez ve verilmez.
            </p>

            <h2>2. Kullanıcı Yükümlülükleri</h2>
            <ul>
              <li>Platforma girilen bilgilerin doğruluğundan kullanıcı sorumludur.</li>
              <li>Hesap bilgileri kullanıcı tarafından gizli tutulmalıdır.</li>
              <li>Platform yalnızca yasal amaçlar için kullanılabilir.</li>
              <li>KOSGEB başvuruları e-Devlet üzerinden bizzat kullanıcı tarafından gönderilmelidir.</li>
            </ul>

            <h2>3. Sorumluluk Reddi</h2>
            <p>
              Platform tarafından üretilen belgeler, kullanıcının girdiği bilgiler doğrultusunda
              hazırlanmaktadır. Hatalı veya eksik bilgi nedeniyle oluşabilecek olumsuz sonuçlardan
              kosgebhibe.com sorumlu tutulamaz.
            </p>
            <p>
              KOSGEB program koşulları, limitleri ve başvuru tarihleri değişebilir. Güncel bilgi için
              <a href="https://kosgeb.gov.tr" target="_blank" rel="noopener noreferrer"> kosgeb.gov.tr</a>{' '}
              ziyaret edilmelidir.
            </p>

            <h2>4. Ödeme ve İade</h2>
            <p>
              Başvuru dosyası PDF olarak indirildikten sonra iade yapılmamaktadır.
              PDF indirilmeden önce sorun yaşanması halinde 7 gün içinde{' '}
              <a href="mailto:destek@kosgebhibe.com">destek@kosgebhibe.com</a>{' '}
              adresinden destek alabilirsiniz.
            </p>

            <h2>5. Fikri Mülkiyet</h2>
            <p>
              Platform tasarımı, kodu ve içerikleri kosgebhibe.com'a aittir. Kullanıcı tarafından
              üretilen başvuru belgelerinin telif hakkı kullanıcıya aittir.
            </p>

            <h2>6. Değişiklikler</h2>
            <p>
              Bu koşullar önceden bildirim yapılmaksızın güncellenebilir. Güncel hali her zaman
              bu sayfada yayımlanır.
            </p>

            <h2>7. İletişim</h2>
            <p>
              <a href="mailto:destek@kosgebhibe.com">destek@kosgebhibe.com</a>
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
