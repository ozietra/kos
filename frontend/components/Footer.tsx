import Link from 'next/link'
import styles from './Footer.module.css'

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className="container">
        <div className={styles.grid}>
          <div className={styles.brand}>
            <div className={styles.logo}>
              kosgeb<span>hibe</span>.com
            </div>
            <p className={styles.tagline}>
              KOSGEB başvurularınızı danışman olmadan hazırlayın.
            </p>
          </div>

          <div>
            <div className="label" style={{ marginBottom: '12px' }}>Platform</div>
            <div className={styles.links}>
              <Link href="/uygunluk-testi">Uygunluk Testi</Link>
              <Link href="/nace-kodu-sorgula">NACE Kodu Sorgula</Link>
              <Link href="/fiyatlandirma">Fiyatlandırma</Link>
            </div>
          </div>

          <div>
            <div className="label" style={{ marginBottom: '12px' }}>Rehberler</div>
            <div className={styles.links}>
              <Link href="/blog/kosgeb-hibe-basvurusu-nasil-yapilir">Başvuru Nasıl Yapılır?</Link>
              <Link href="/blog/kosgeb-icin-nace-kodu-nasil-belirlenir">NACE Kodu</Link>
              <Link href="/blog/kosgeb-basvurularinda-en-cok-yapilan-hatalar">Kaçınılacak Hatalar</Link>
              <Link href="/blog">Tüm Yazılar</Link>
            </div>
          </div>

          <div>
            <div className="label" style={{ marginBottom: '12px' }}>Yasal</div>
            <div className={styles.links}>
              <Link href="/kvkk">KVKK Aydınlatma Metni</Link>
              <Link href="/gizlilik">Gizlilik Politikası</Link>
              <Link href="/kullanim-sartlari">Kullanım Şartları</Link>
              <Link href="/mesafeli-satis">Mesafeli Satış Sözleşmesi</Link>
            </div>
          </div>
        </div>

        <div className={styles.bottom}>
          <p className={styles.legal}>
            Bu platform bilgilendirme ve hazırlık amaçlıdır. Güncel program şartları için{' '}
            <a href="https://kosgeb.gov.tr" target="_blank" rel="noopener noreferrer">
              kosgeb.gov.tr
            </a>{' '}
            ziyaret ediniz. Onay garantisi verilmez.
          </p>
          <p className={styles.copyright}>
            © {new Date().getFullYear()} kosgebhibe.com — Tüm hakları saklıdır.
          </p>
        </div>
      </div>
    </footer>
  )
}
