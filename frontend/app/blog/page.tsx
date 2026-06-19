import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Link from 'next/link'
import styles from './page.module.css'

export const metadata: Metadata = {
  title: 'KOSGEB Rehberleri ve Hibe Başvurusu Bilgileri — kosgebhibe.com',
  description:
    'KOSGEB hibe başvurusu nasıl yapılır, hangi belgeler gerekir, başvurularda en sık yapılan hatalar ve daha fazlası.',
}

// Faz 5'te CMS/MDX ile gerçek makaleler eklenecek
const POSTS = [
  {
    slug: 'kosgeb-geri-odemeli-destek-faizsiz-kredi',
    title: 'KOSGEB Geri Ödemeli Destek ve Faizsiz Kredi Nedir?',
    excerpt: 'Hibe mi kredi mi? Geri ödemesiz, geri ödemeli (faizsiz) ve karma destek yapıları arasındaki farklar.',
    category: 'Bilgi',
    readMin: 6,
  },
  {
    slug: 'vergi-sgk-borcu-kosgeb-basvurusu',
    title: 'Vergi ve SGK Borcu KOSGEB Başvurusunu Engeller mi?',
    excerpt: 'Borç başvuruyu nasıl etkiler, yapılandırma ne işe yarar ve başvuru öncesi neler yapılmalı?',
    category: 'İpucu',
    readMin: 5,
  },
  {
    slug: 'kosgeb-is-plani-nasil-yazilir',
    title: 'KOSGEB İş Planı Nasıl Yazılır? (Örnekli Adım Adım Rehber)',
    excerpt: 'Jürinin onaylayacağı iş planı: bölüm bölüm içerik, bütçe gerekçelendirme ve sık yapılan hatalar — örneklerle.',
    category: 'Başvuru Rehberi',
    readMin: 9,
  },
  {
    slug: 'yesil-sanayi-mi-dijital-donusum-mu',
    title: 'Yeşil Sanayi mi, KOBİ Dijital Dönüşüm mü? Hangi Programa Başvurmalı?',
    excerpt: 'İki güçlü KOSGEB programının farkları, kimler için uygun ve doğru programa nasıl karar verilir?',
    category: 'Program Analizi',
    readMin: 7,
  },
  {
    slug: 'kosgeb-basvurusu-reddedilirse-ne-yapmali',
    title: 'KOSGEB Başvurusu Reddedilirse Ne Yapmalı? İtiraz ve Yeniden Başvuru',
    excerpt: 'Başvurunuz reddedildiyse red nedenini öğrenme, itiraz hakkı ve bir sonraki dönem güçlü başvuru için adım adım rehber.',
    category: 'İpucu',
    readMin: 7,
  },
  {
    slug: 'kadin-girisimci-kosgeb-destekleri-2026',
    title: 'Kadın Girişimci KOSGEB Destekleri 2026: Avantajlar ve Başvuru',
    excerpt: 'Kadın girişimciler için ek hibe avantajları, uygun programlar ve başvuru adımları — 2026 güncel.',
    category: 'Program Analizi',
    readMin: 6,
  },
  {
    slug: 'kosgeb-hibe-basvurusu-nasil-yapilir',
    title: 'KOSGEB Hibe Başvurusu Nasıl Yapılır? (2026 Güncel Rehber)',
    excerpt: 'Adım adım KOSGEB hibe başvuru süreci: kayıt, belgeler, başvuru formu ve sık yapılan hatalar.',
    category: 'Başvuru Rehberi',
    readMin: 8,
  },
  {
    slug: 'kosgeb-is-gelistirme-destegi-nedir',
    title: 'İş Geliştirme Desteği (İGD) Nedir? 2026 Koşulları ve Limitleri',
    excerpt: '1.500.000 ₺\'ye kadar geri ödemesiz hibe. Kimler başvurabilir, koşullar nelerdir, belgeler nelerdir?',
    category: 'Program Analizi',
    readMin: 6,
  },
  {
    slug: 'kobigel-2026-basvuru-rehberi',
    title: 'KOBİGEL 2026 Başvuru Rehberi — 5 Milyon ₺ Hibe',
    excerpt: 'KOBİGEL KOBİ Gelişim Programı 2026 başvuruları için tam rehber. Jüri sistemi, proje yazımı ve ipuçları.',
    category: 'Program Analizi',
    readMin: 10,
  },
  {
    slug: 'kosgeb-basvurularinda-en-cok-yapilan-hatalar',
    title: 'KOSGEB Başvurularında En Çok Yapılan 7 Hata',
    excerpt: 'Binlerce başvurudan derlenen verilerle en yaygın red nedenleri ve bunlardan nasıl kaçınacağınız.',
    category: 'İpucu',
    readMin: 5,
  },
  {
    slug: 'kosgeb-icin-nace-kodu-nasil-belirlenir',
    title: 'KOSGEB İçin NACE Kodu Nasıl Belirlenir?',
    excerpt: 'Yanlış NACE kodu başvurunuzu reddettiriyor. Doğru kodu nasıl bulacağınızı adım adım anlattık.',
    category: 'Teknik Rehber',
    readMin: 4,
  },
  {
    slug: 'kosgeb-kaydi-nasil-yapilir',
    title: 'KOSGEB Kaydı Nasıl Yapılır? (e-Devlet Üzerinden)',
    excerpt: 'KOSGEB veri tabanına kayıt zorunlu. Adım adım kayıt işlemi ve olası sorunlar.',
    category: 'Teknik Rehber',
    readMin: 3,
  },
  {
    slug: 'kosgeb-hibe-miktarlari-2026',
    title: 'KOSGEB Hibe Miktarları 2026 — Tüm Destekler Tablosu',
    excerpt: '2026 yılı tüm KOSGEB destekleri, limitleri ve türleri tek tabloda.',
    category: 'Bilgi',
    readMin: 3,
  },
  {
    slug: 'kosgeb-2026-destekleri',
    title: 'KOSGEB 2026 Destekleri: Hangi Program Size Uygun?',
    excerpt: 'İşletme yaşınıza ve sektörünüze göre hangi KOSGEB programına başvurabilirsiniz?',
    category: 'Başvuru Rehberi',
    readMin: 7,
  },
]

export default function BlogPage() {
  return (
    <>
      <Header />
      <main>
        <section style={{ padding: '60px 0 40px', borderBottom: '1px solid var(--color-border)' }}>
          <div className="container" style={{ maxWidth: '800px' }}>
            <h1 className="section-title" style={{ marginBottom: '12px' }}>KOSGEB Rehberleri</h1>
            <p className="text-secondary">
              KOSGEB hibe başvuruları ve program koşulları hakkında yeni başlayanlardan
              deneyimlilere kadar her seviyeye yönelik rehberler.
            </p>
          </div>
        </section>

        <section style={{ padding: '48px 0 80px' }}>
          <div className="container" style={{ maxWidth: '900px' }}>
            <div className={styles.postGrid}>
              {POSTS.map(post => (
                <Link key={post.slug} href={`/blog/${post.slug}`} className={styles.postCard}>
                  <div className={styles.postCategory}>
                    <span className="badge badge-muted">{post.category}</span>
                    <span className="fs-xs text-muted">{post.readMin} dk okuma</span>
                  </div>
                  <h2 className={styles.postTitle}>{post.title}</h2>
                  <p className={styles.postExcerpt}>{post.excerpt}</p>
                  <span className={styles.readMore}>Devamını oku →</span>
                </Link>
              ))}
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  )
}
