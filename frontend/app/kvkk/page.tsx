import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

export const metadata: Metadata = {
  title: 'KVKK Aydınlatma Metni — kosgebhibe.com',
  description: 'kosgebhibe.com kişisel verilerin korunması kanunu (KVKK) kapsamındaki aydınlatma metni.',
}

export default function KvkkPage() {
  return (
    <>
      <Header />
      <main style={{ padding: '60px 0 80px' }}>
        <div className="container" style={{ maxWidth: '720px' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '32px' }}>
            KVKK Aydınlatma Metni
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-muted)', marginBottom: '32px' }}>
            Son güncelleme: Mart 2026
          </p>

          <div className="legal-content">
            <h2>1. Veri Sorumlusu</h2>
            <p>
              Kişisel verileriniz, kosgebhibe.com platformu ("Platform") veri sorumlusu sıfatıyla tarafımızca
              6698 sayılı Kişisel Verilerin Korunması Kanunu ("KVKK") hükümleri kapsamında işlenmektedir.
            </p>

            <h2>2. İşlenen Kişisel Veriler</h2>
            <p>Platform üzerinden aşağıdaki kişisel verileriniz işlenmektedir:</p>
            <ul>
              <li><strong>Kimlik bilgileri:</strong> Ad, soyad</li>
              <li><strong>İletişim bilgileri:</strong> E-posta adresi, telefon numarası</li>
              <li><strong>İşletme bilgileri:</strong> Ticaret unvanı, NACE kodu, kuruluş tarihi (şifrelenmiş vergi no dahil)</li>
              <li><strong>Finansal bilgiler:</strong> Ödeme bilgileri (iyzico güvenli öğe)</li>
              <li><strong>Teknik veriler:</strong> IP adresi, oturum bilgileri</li>
            </ul>

            <h2>3. Kişisel Verilerin İşlenme Amaçları</h2>
            <ul>
              <li>Hizmetin sunulması, başvuru dosyalarının hazırlanması</li>
              <li>Kullanıcı hesabının yönetilmesi</li>
              <li>Ödeme işlemlerinin gerçekleştirilmesi</li>
              <li>Yasal yükümlülüklerin yerine getirilmesi</li>
              <li>Hizmet kalitesinin iyileştirilmesi</li>
            </ul>

            <h2>4. Kişisel Verilerin Aktarımı</h2>
            <p>
              Kişisel verileriniz; ödeme işlemi kapsamında <strong>iyzico Ödeme Hizmetleri A.Ş.</strong>'ye,
              e-posta teslimatı kapsamında <strong>Postal SMTP</strong> sunucusuna ve yasal zorunluluk
              halinde yetkili kamu kurumlarına aktarılabilir. Verileriniz üçüncü şahıslara satılmaz.
            </p>

            <h2>5. Veri Güvenliği</h2>
            <p>
              Vergi numarası AES-256 şifreleme ile saklanmaktadır. Sunucu iletişimleri TLS ile
              korunmaktadır. Şifreler bcrypt hash ile tutulmaktadır.
            </p>

            <h2>6. Haklarınız (KVKK Madde 11)</h2>
            <ul>
              <li>Kişisel verilerinizin işlenip işlenmediğini öğrenme</li>
              <li>İşlenmişse bilgi talep etme</li>
              <li>İşlenme amacını ve amaca uygun kullanılıp kullanılmadığını öğrenme</li>
              <li>Yurtiçi veya yurtdışında aktarıldığı üçüncü kişileri bilme</li>
              <li>Eksik/yanlış işlenmişse düzeltilmesini isteme</li>
              <li>Silinmesini/yok edilmesini isteme (yasal saklama süresi dolduğunda)</li>
            </ul>

            <h2>7. İletişim</h2>
            <p>
              KVKK kapsamındaki başvuru ve talepler için:{' '}
              <a href="mailto:kvkk@kosgebhibe.com">kvkk@kosgebhibe.com</a>
            </p>

            <h2>8. Çerezler</h2>
            <p>
              Platform yalnızca oturum ve basit analytics çerezleri kullanır. Reklamcılık
              veya üçüncü parti izleme çerezi kullanılmamaktadır.
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
