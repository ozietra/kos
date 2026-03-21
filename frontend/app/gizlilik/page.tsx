import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Gizlilik Politikası — kosgebhibe.com',
  description: 'kosgebhibe.com gizlilik politikası ve kişisel veri işleme süreçleri.',
}

export default function GizlilikPage() {
  return (
    <>
      <Header />
      <main style={{ padding: '60px 0 80px' }}>
        <div className="container" style={{ maxWidth: '720px' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '32px' }}>
            Gizlilik Politikası
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-muted)', marginBottom: '32px' }}>
            Son güncelleme: Mart 2026
          </p>

          <div className="legal-content">
            <h2>1. Genel Bakış</h2>
            <p>
              kosgebhibe.com olarak kullanıcılarımızın gizliliğine önem veriyoruz.
              Bu politika, hangi verilerin toplandığını, nasıl kullanıldığını ve haklarınızı açıklar.
            </p>

            <h2>2. Toplanan Veriler</h2>
            <ul>
              <li>Hesap bilgileri: e-posta, ad-soyad</li>
              <li>İşletme bilgileri: ticaret unvanı, NACE kodu, kuruluş tarihi</li>
              <li>Ödeme bilgileri: iyzico üzerinden güvenli şekilde işlenir; kart bilgisi bizde saklanmaz</li>
              <li>Teknik veriler: IP adresi, tarayıcı türü, oturum bilgileri</li>
            </ul>

            <h2>3. Çerezler</h2>
            <p>
              Yalnızca oturum yönetimi için zorunlu çerezler kullanılır.
              Reklam veya izleme çerezi kullanılmaz.
            </p>

            <h2>4. Veri Güvenliği</h2>
            <p>
              Vergi numarası AES-256 ile şifrelenir. Şifreler bcrypt ile hashlenir.
              Sunucu → tarayıcı iletişimi TLS ile korunur.
            </p>

            <h2>5. KVKK Hakları</h2>
            <p>
              Kişisel verilerinize ilişkin ayrıntılı bilgi için{' '}
              <Link href="/kvkk">KVKK Aydınlatma Metni</Link>'ni inceleyebilirsiniz.
            </p>

            <h2>6. İletişim</h2>
            <p>
              <a href="mailto:kvkk@kosgebhibe.com">kvkk@kosgebhibe.com</a>
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
