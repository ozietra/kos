import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Kullanım Şartları — kosgebhibe.com',
  description: 'kosgebhibe.com kullanım şartları. Platformat hizmetlerimizden yararlanırken geçerli olan kurallar ve koşullar.',
}

export default function KullanimSartlariPage() {
  return (
    <>
      <Header />
      <main style={{ padding: '60px 0 80px' }}>
        <div className="container" style={{ maxWidth: '720px' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 700, marginBottom: '32px' }}>
            Kullanım Şartları
          </h1>
          <p style={{ fontSize: '13px', color: 'var(--color-text-muted)', marginBottom: '32px' }}>
            Son güncelleme: Mart 2026
          </p>

          <div className="legal-content">
            <h2>1. Kabul</h2>
            <p>
              kosgebhibe.com'u kullanarak bu kullanım şartlarını kabul etmiş sayılırsınız.
              Şartları kabul etmiyorsanız platformu kullanmayınız.
            </p>

            <h2>2. Hizmet Kapsamı</h2>
            <p>
              kosgebhibe.com, KOSGEB hibe başvurusu hazırlık sürecinde kullanıcılara uygunluk analizi,
              proje özeti taslağı ve belge kontrol listesi sunan bir dijital araçtır.
              Platform herhangi bir başvurunun kabul edileceğini garanti etmez.
            </p>

            <h2>3. Kullanıcı Yükümlülükleri</h2>
            <ul>
              <li>Platforma yüklediğiniz veya girdiğiniz bilgilerin doğru olmasından siz sorumlusunuz.</li>
              <li>Hesabınızı başkasıyla paylaşamazsınız.</li>
              <li>Platform içeriğini ticari amaçla kopyalayamazsınız.</li>
              <li>Otomatik araçlarla (bot, scraper) erişim yasaktır.</li>
            </ul>

            <h2>4. Ücretlendirme ve Ödemeler</h2>
            <p>
              Starter Plan 499 ₺ (KDV dahil) tek seferlik ödeme ile satın alınır.
              Ödemeler iyzico altyapısıyla güvenli şekilde işlenir.
              Kart bilgileriniz platformda saklanmaz.
            </p>

            <h2>5. Cayma Hakkı ve İadeler</h2>
            <p>
              6502 sayılı Tüketicinin Korunması Hakkında Kanun kapsamında, dijital içerik hizmetinde
              alıcının onayıyla teslimat başladıktan sonra cayma hakkı kullanılamaz.
              PDF dosyasını henüz indirmediyseniz 7 gün içinde iade talebinizi{' '}
              <a href="mailto:destek@kosgebhibe.com">destek@kosgebhibe.com</a> adresine iletebilirsiniz.
            </p>

            <h2>6. Sorumluluk Sınırı</h2>
            <p>
              Platform, KOSGEB kararlarından bağımsız bir hazırlık aracıdır.
              Başvurunun sonucu, platformun kontrolü dışındadır ve herhangi bir garanti verilmez.
            </p>

            <h2>7. Fikri Mülkiyet</h2>
            <p>
              Platform tasarımı, içerikleri ve yazılım altyapısı kosgebhibe.com'a aittir.
              İzinsiz kopyalama, dağıtım veya değiştirme yasaktır.
            </p>

            <h2>8. Değişiklikler</h2>
            <p>
              Bu şartlar önceden haber vermeksizin güncellenebilir. Değişiklikler yayınlanma anında
              geçerli olur. Platformu kullanmaya devam etmeniz değişiklikleri kabul ettiğiniz anlamına gelir.
            </p>

            <h2>9. İletişim</h2>
            <p>
              <a href="mailto:destek@kosgebhibe.com">destek@kosgebhibe.com</a>
            </p>

            <p style={{ marginTop: '24px' }}>
              Ayrıca:{' '}
              <Link href="/kvkk">KVKK Aydınlatma Metni</Link>
              {' · '}
              <Link href="/gizlilik">Gizlilik Politikası</Link>
              {' · '}
              <Link href="/mesafeli-satis">Mesafeli Satış Sözleşmesi</Link>
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}
