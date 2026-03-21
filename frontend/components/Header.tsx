import Link from 'next/link'
import styles from './Header.module.css'

export default function Header() {
  return (
    <header className={styles.header}>
      <div className="container">
        <nav className={styles.nav}>
          <Link href="/" className={styles.logo}>
            <img src="/icon.png" alt="" className={styles.logoIcon} />
            <span>kosgeb<span className={styles.logoAccent}>hibe</span>.com</span>
          </Link>

          <div className={styles.links}>
            <Link href="/uygunluk-testi" className={styles.navLink}>Uygunluk Testi</Link>
            <Link href="/blog" className={styles.navLink}>Rehberler</Link>
            <Link href="/fiyatlandirma" className={styles.navLink}>Fiyatlar</Link>
          </div>

          <div className={styles.actions}>
            <Link href="/giris" className="btn btn-secondary btn-sm">Giriş Yap</Link>
            <Link href="/uye-ol" className="btn btn-primary btn-sm">Ücretsiz Başla</Link>
          </div>
        </nav>
      </div>
    </header>
  )
}
