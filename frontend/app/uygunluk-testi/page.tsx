import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import styles from './page.module.css'

export const metadata: Metadata = {
  title: 'Ücretsiz KOSGEB Uygunluk Testi — Hangi Programa Başvurabilirsiniz?',
  description:
    'İşletmenizin KOSGEB hibe programlarına uygun olup olmadığını 2 dakikada öğrenin. Danışman olmadan, ücretsiz.',
}

export default function UygunlukTestiPage() {
  return (
    <>
      <Header />
      <main className={styles.main}>
        <div className="container">
          <div className={styles.intro}>
            <h1 className="section-title">Ücretsiz KOSGEB Uygunluk Testi</h1>
            <p className="text-secondary">
              Aşağıdaki soruları yanıtlayın. Sistem, uygun olduğunuz programları ve tahmini hibe tutarını gösterir.
            </p>
          </div>

          <div className={styles.widgetCard}>
            <EligibilityWidget />
          </div>

          {/* Anchor hedefi: hızlı kontrol listesi */}
          <div id="sorular" style={{ marginTop: '64px', paddingTop: '24px', borderTop: '1px solid var(--color-border)' }}>
            <h2 className="section-title" style={{ fontSize: '18px', marginBottom: '20px' }}>Hızlı Kontrol Listesi</h2>
            <p className="text-secondary fs-sm" style={{ marginBottom: '20px' }}>
              Başvuru yapmadan önce aşağıdaki maddeleri teyit edin. Herhangi birinde sorun varsa başvurunuz reddedilebilir.
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {[
                { q: 'Türkiye\'de kayıtlı ve aktif bir işletmeniz var mı?', note: 'Ticaret veya şahıs firması olabilir.' },
                { q: 'KOSGEB veri tabanına kayıtlı mısınız?', note: 'eportal.kosgeb.gov.tr\'den kontrol edin. Kayıt yoksa önce kayıt olun.' },
                { q: 'Vergi borcunuz var mı?', note: 'Vadesi geçmiş vergi borcu başvuruyu anında reddettiriyor.' },
                { q: 'SGK prim borcunuz var mı?', note: 'Yapılandırılmış borcun dahi belirtilmesi gerekebilir.' },
                { q: 'İşletmeniz kaç yıllık?', note: 'İş Geliştirme Desteği için 3 yıldan genç olmalı. KOBİGEL için koşul yok.' },
                { q: 'NACE kodunuz uygun mu?', note: 'Bazı sektörler belirli programlara başvuramaz. Sorgulama aracımızı kullanın.' },
                { q: 'Son 3 yılda başka şirkette %25+ ortaklığınız var mıydı?', note: 'İGD uygunluğunuzu etkileyebilir.' },
              ].map((item, i) => (
                <div key={i} className="card" style={{ padding: '14px 18px' }}>
                  <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                    <span className="fw-600" style={{ color: 'var(--color-accent)', flexShrink: 0 }}>{i + 1}.</span>
                    <div>
                      <div style={{ fontWeight: 600, fontSize: '14px' }}>{item.q}</div>
                      <div className="fs-xs text-muted" style={{ marginTop: '4px' }}>{item.note}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div style={{ marginTop: '24px', display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
              <a href="/uye-ol" className="btn btn-primary">Hesap Aç — Ücretsiz Test Yap</a>
              <a href="/nace-kodu-sorgula" className="btn btn-secondary">NACE Kodu Sorgula</a>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  )
}

/* ── Uygunluk mini-formu ── */
function EligibilityWidget() {
  'use client'
  // Bu bir placeholder bileşen — tam etkileşim için ayrı Client Component olarak ayrılacak.
  // Şu an SEO yapısını kuruyoruz; interaktif kısım bir sonraki dosyada.
  return (
    <div className={styles.teaser}>
      <div className={styles.teaserIcon}>✓</div>
      <div className="card-title">Hesap Açmadan Başlayın</div>
      <p className="text-secondary fs-sm" style={{ marginTop: '8px' }}>
        Uygunluk testi için hesap gerekmez. Sadece birkaç bilgi yeterli.
      </p>
      <div className={styles.questions}>
        {[
          'Türkiye\'de kayıtlı bir şirketiniz var mı?',
          'İşletmenizin kaç yıllık olduğunu biliyor musunuz?',
          'KOSGEB veri tabanına kayıtlı mısınız?',
          'Vergi veya SGK borcunuz var mı?',
        ].map((q, i) => (
          <div key={i} className={styles.questionItem}>
            <span className="text-success fw-600">{i + 1}.</span> {q}
          </div>
        ))}
      </div>
      <a href="/uye-ol" className="btn btn-primary" style={{ marginTop: '20px' }}>
        Hesap Aç ve Ücretsiz Test Yap
      </a>
      <p className="fs-xs text-muted" style={{ marginTop: '10px' }}>
        Kayıt olmak istemiyorsanız{' '}
        <a href="#sorular" style={{ color: 'inherit', textDecoration: 'underline' }}>
          hızlı kontrol listesine bakın
        </a>
      </p>
    </div>
  )
}
