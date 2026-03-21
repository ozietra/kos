import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import styles from './page.module.css'

export const metadata: Metadata = {
  title: 'KOSGEB Hibe Başvurusu Hazırlık Platformu — kosgebhibe.com',
  description:
    'İşletmenizin uygun olduğu KOSGEB programını bulun, başvuru metinlerinizi dakikalar içinde hazırlayın. Danışman olmadan, 499 ₺\'ye.',
}

export default function HomePage() {
  return (
    <>
      <Header />
      <main>
        {/* ── HERO ── */}
        <section className={styles.hero}>
          <div className="container">
            <div className={styles.heroContent}>
              <div className={styles.heroBadge}>
                <span className="badge badge-info">2026 Güncel • KOBİGEL Başvurusu: 30 Nisan 2026</span>
              </div>
              <h1 className="hero-title">
                KOSGEB Hibesine<br />
                Başvurun —<br />
                <span className={styles.accent}>Danışman Olmadan</span>
              </h1>
              <p className={styles.heroSub}>
                İşletmenizin uygun olduğu programı bulun, başvuru metinlerinizi
                dakikalar içinde hazırlayın. Danışmanlar 5.000–20.000 ₺ alıyor.
                Biz 499 ₺&apos;ye aynı kalitede başvuru dosyası hazırlıyoruz.
              </p>
              <div className={styles.heroCtas}>
                <a href="/uygunluk-testi" className="btn btn-primary btn-lg">
                  Ücretsiz Uygunluk Testi Yap
                </a>
                <a href="/uye-ol" className="btn btn-secondary btn-lg">
                  Hemen Başvur — 499 ₺
                </a>
              </div>
              <p className={styles.heroNote}>
                Kayıt gerekmez • Kredi kartı gerekmez • Uygunluk testi ücretsiz
              </p>
            </div>
          </div>
        </section>

        {/* ── STATS BAND ── */}
        <section className={styles.statsBand}>
          <div className="container">
            <div className={styles.statsGrid}>
              <div className={styles.statItem}>
                <div className="amount">2.45 Milyar ₺</div>
                <div className={styles.statLabel}>2025 yılında dağıtılan toplam hibe</div>
              </div>
              <div className={styles.statItem}>
                <div className="amount">1.699</div>
                <div className={styles.statLabel}>Desteklenen proje sayısı (2025)</div>
              </div>
              <div className={styles.statItem}>
                <div className="amount">1.650.000 ₺</div>
                <div className={styles.statLabel}>Kadın/Genç/Engelli girişimcilere hibe limiti</div>
              </div>
              <div className={styles.statItem}>
                <div className="amount">3</div>
                <div className={styles.statLabel}>Yılda açılan başvuru dönemi</div>
              </div>
            </div>
          </div>
        </section>

        {/* ── HOW IT WORKS ── */}
        <section className={styles.section}>
          <div className="container">
            <h2 className={`section-title ${styles.sectionTitle}`}>Nasıl Çalışır?</h2>
            <div className={styles.stepsGrid}>
              <div className={styles.stepCard}>
                <div className={styles.stepNum}>1</div>
                <div className="card-title">İşletmenizi Tanıtın</div>
                <p className="text-secondary">
                  Sektörünüzü, kuruluş tarihinizi ve proje fikrinizi girin.
                  5 dakika sürer.
                </p>
              </div>
              <div className={styles.stepArrow}>→</div>
              <div className={styles.stepCard}>
                <div className={styles.stepNum}>2</div>
                <div className="card-title">Başvuru Dosyanız Hazırlanır</div>
                <p className="text-secondary">
                  Platform başvuru özetinizi, iş planınızı ve finansal
                  projeksiyonunuzu hazırlar. 3–5 dakika sürer.
                </p>
              </div>
              <div className={styles.stepArrow}>→</div>
              <div className={styles.stepCard}>
                <div className={styles.stepNum}>3</div>
                <div className="card-title">PDF İndirin, Gönderin</div>
                <p className="text-secondary">
                  Hazır PDF&apos;i indirin. Eksik belgeler listesine bakın.
                  e-Devlet&apos;ten başvuruyu siz yapın.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* ── WARNING BOX ── */}
        <section className={styles.sectionGray}>
          <div className="container">
            <h2 className={`section-title ${styles.sectionTitle}`}>
              Başvurunuz Yanmasın
            </h2>
            <p className={styles.sectionSub}>
              Ülke genelinde ilk 1.000 proje jüriye davet ediliyor, ilk 500 destek alıyor.
              Küçük hatalar elenmene neden olabilir.
            </p>
            <div className={styles.warningGrid}>
              <div className="card">
                <div className={styles.warnIcon}>!</div>
                <div className="card-title">Ortaklık Payına Dikkat</div>
                <p className="text-secondary fs-sm">
                  Son 3 yılda başka bir şirkette %25 ve üzeri ortaklığınız varsa
                  İş Geliştirme Desteğine uygun olmayabilirsiniz.
                </p>
              </div>
              <div className="card">
                <div className={styles.warnIcon}>!</div>
                <div className="card-title">KOSGEB Kaydınız Aktif Mi?</div>
                <p className="text-secondary fs-sm">
                  Kayıt olmadan başvuru değerlendirmeye alınmaz.
                  eportal.kosgeb.gov.tr&apos;den kontrol edin.
                </p>
              </div>
              <div className="card">
                <div className={styles.warnIcon}>!</div>
                <div className="card-title">Vergi / SGK Borcu</div>
                <p className="text-secondary fs-sm">
                  Vergi veya SGK borcunuz varsa başvurunuz reddolur.
                  Başvurmadan önce mutlaka temizleyin.
                </p>
              </div>
            </div>
          </div>
        </section>


        {/* ── PRICING ── */}
        <section className={styles.sectionGray} id="fiyatlar">
          <div className="container">
            <h2 className={`section-title ${styles.sectionTitle}`}>Fiyatlandırma</h2>
            <p className={styles.sectionSub}>
              Danışmanlar başvuru başına 5.000–20.000 ₺ alıyor. Biz çok daha azına aynı işi yapıyoruz.
            </p>
            <div className={styles.pricingGrid}>
              {/* Ücretsiz */}
              <div className="card">
                <div className="label" style={{ color: 'var(--color-success)' }}>Ücretsiz</div>
                <div className={styles.planName}>Araçlar</div>
                <div className={styles.planDesc}>Kayıt gerekmez</div>
                <ul className={styles.featureList}>
                  <li>✓ Uygunluk Testi</li>
                  <li>✓ NACE Kodu Sorgula</li>
                  <li>✓ Program Takvimi</li>
                </ul>
                <a href="/uygunluk-testi" className="btn btn-outline" style={{ width: '100%', marginTop: '20px' }}>
                  Ücretsiz Başla
                </a>
              </div>

              {/* Starter */}
              <div className={`card ${styles.featuredCard}`}>
                <div className="label">Starter</div>
                <div className={styles.planPrice}>499 ₺</div>
                <div className={styles.planDesc}>Tek seferlik, KDV dahil</div>
                <ul className={styles.featureList}>
                  <li>✓ Tam başvuru dosyası</li>
                  <li>✓ PDF çıktısı</li>
                  <li>✓ Belge kontrol listesi</li>
                  <li>✓ 30 gün erişim</li>
                </ul>
                <a href="/uye-ol?plan=starter" className="btn btn-primary" style={{ width: '100%', marginTop: '20px' }}>
                  Hemen Başla
                </a>
              </div>
            </div>
          </div>
        </section>

        {/* ── NOTIFICATION BAND ── */}
        <section className={styles.notifyBand}>
          <div className="container">
            <div className={styles.notifyContent}>
              <div>
                <div className="card-title">Yeni Dönem Açıldığında Haberdar Ol</div>
                <p className="text-secondary fs-sm">
                  Başvuru dönemi açıldığında e-posta ile bildirim alın. Ücretsiz.
                </p>
              </div>
              <form className={styles.notifyForm}>
                <input
                  type="email"
                  className="input"
                  placeholder="E-posta adresiniz"
                  style={{ maxWidth: '280px' }}
                />
                <button type="submit" className="btn btn-primary">
                  Bildir
                </button>
              </form>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
