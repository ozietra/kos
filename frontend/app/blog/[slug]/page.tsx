import { notFound } from 'next/navigation'
import type { Metadata } from 'next'
import Header from '@/components/Header'
import Footer from '@/components/Footer'
import Link from 'next/link'
import styles from './page.module.css'

// ── Blog Makale İçerikleri ─────────────────────────────────────────────────────
const CONTENT: Record<string, {
  title: string
  description: string
  content: string
  category: string
  readMin: number
  dateStr: string
  faq?: { q: string; a: string }[]
}> = {

  'kosgeb-is-plani-nasil-yazilir': {
    title: 'KOSGEB İş Planı Nasıl Yazılır? (Örnekli Adım Adım Rehber)',
    description: 'Jürinin onaylayacağı KOSGEB iş planı nasıl hazırlanır? Bölüm bölüm içerik, bütçe gerekçelendirme ve sık yapılan hatalar — örneklerle.',
    category: 'Başvuru Rehberi',
    readMin: 9,
    dateStr: 'Haziran 2026',
    content: `
## İş Planı Neden Bu Kadar Önemli?

KOSGEB başvurusunda jürinin kararını en çok etkileyen belge **iş planıdır**. İyi bir iş planı; fikrinizin gerçekçi, ölçülebilir ve sürdürülebilir olduğunu kanıtlar. Zayıf, afaki veya tutarsız bir iş planı ise güçlü bir fikri bile elettirir. Amaç, "para istiyorum" değil; **"bu yatırım şu sonucu üretecek, şu kadar istihdam ve gelir yaratacak"** mantığını sayısal verilerle ortaya koymaktır.

## İş Planının Temel Bölümleri

### 1. Yönetici Özeti
İşletmenizi, proje fikrinizi ve talep ettiğiniz desteği birkaç paragrafta özetler. En sona yazın ama en başa koyun.

### 2. İşletme ve Ekip
Faaliyet alanınız (NACE), kuruluş durumu, ekip ve yetkinlikler. Genç/kadın girişimci gibi avantajlarınızı belirtin.

### 3. Pazar Analizi
Hedef kitleniz kim, pazar ne kadar büyük, rakipler kimler ve sizin **rekabet avantajınız** ne? Mümkünse sayısal verilerle destekleyin.

### 4. Ürün/Hizmet ve Değer Önerisi
Müşterinin hangi problemini, nasıl çözüyorsunuz? Somut faydayı (ör. "süreçleri %30 hızlandırır") vurgulayın.

### 5. Finansal Plan ve Bütçe
En kritik bölüm. Her bütçe kalemini **gerekçesiyle** yazın:

| Bütçe Kalemi | Tutar | Gerekçe (neden gerekli, ne kazandırır) |
|---|---|---|
| Donanım | 50.000 ₺ | Üretim/geliştirme kapasitesi için zorunlu ekipman |
| Yazılım | 50.000 ₺ | Lisanslı geliştirme araçları, verimlilik artışı |
| Eğitim | 100.000 ₺ | Ekip yetkinliği, kaliteli çıktı |

Toplam talebiniz, kalemlerin toplamıyla **birebir tutarlı** olmalı. Tüm dosyada aynı rakamları kullanın.

### 6. Zaman Planı ve Hedefler
Aylara/çeyreklere bölünmüş somut kilometre taşları; ilk yıl gelir ve istihdam hedefleri.

## Sık Yapılan Hatalar

- Bölümler arası **çelişen rakamlar** (özette 1 milyon, finansalda 5 milyon gibi)
- Gerekçesiz, "olsun" diye eklenmiş bütçe kalemleri
- Abartılı, sektör ortalamasının çok üstünde gelir/istihdam vaatleri
- Kopyala-yapıştır, kişiselleştirilmemiş genel metinler

## İpucu: Tutarlılık = Güven

Jüri, dosyanın her yerinde aynı işletmeyi, aynı rakamları ve aynı hikâyeyi görmek ister. Tutarlı ve gerçekçi bir dosya, profesyonellik sinyali verir ve onay şansını artırır.

---

Tutarlı, gerekçeli ve jüriye uygun bir iş planını **kosgebhibe.com** ile dakikalar içinde hazırlayabilirsiniz. Güncel program koşulları için kosgeb.gov.tr'yi esas alın.
`,
    faq: [
      { q: 'KOSGEB iş planı kaç sayfa olmalı?', a: 'Kesin bir sayfa zorunluluğu yoktur; önemli olan tüm temel bölümleri (özet, pazar, ürün, finansal plan, zaman planı) net ve tutarlı biçimde içermesidir. Gereksiz dolgu yerine somut, gerekçeli içerik tercih edilir.' },
      { q: 'Bütçe kalemleri nasıl gerekçelendirilir?', a: 'Her kalem için "neden gerekli, ne işe yarayacak, geri dönüşü ne" sorularını yanıtlayın. Tutarlar sektör gerçeklerine uygun ve toplam talebinizle birebir tutarlı olmalıdır.' },
      { q: 'İş planında en sık hangi hata yapılır?', a: 'Bölümler arası çelişen rakamlar (örneğin özette ve finansal bölümde farklı gelir/istihdam sayıları) ve gerekçesiz bütçe kalemleri en sık yapılan, en çok eletten hatalardır.' },
    ],
  },

  'yesil-sanayi-mi-dijital-donusum-mu': {
    title: 'Yeşil Sanayi mi, KOBİ Dijital Dönüşüm mü? Hangi KOSGEB Programına Başvurmalı?',
    description: 'Yeşil Sanayi Destek Programı ile KOBİ Dijital Dönüşüm Destek Programı arasındaki farklar, kimler için uygun ve nasıl karar verilir?',
    category: 'Program Analizi',
    readMin: 7,
    dateStr: 'Haziran 2026',
    content: `
## İki Güçlü Program, Farklı Odaklar

KOSGEB'in öne çıkan iki programı, **Yeşil Sanayi Destek Programı** ve **KOBİ Dijital Dönüşüm Destek Programı**, farklı ihtiyaçlara hitap eder. Yanlış programa başvurmak, güçlü bir projeyi bile uygunluk aşamasında eletebilir. Doğru tercih, işletmenizin **önceliğine ve yatırım konusuna** bağlıdır.

## Temel Fark

| Kriter | Yeşil Sanayi | KOBİ Dijital Dönüşüm |
|---|---|---|
| Ana odak | Enerji verimliliği, temiz/döngüsel ekonomi, yenilenebilir enerji | Üretim/iş süreçlerinde dijitalleşme, otomasyon, yazılım |
| Tipik hedef kitle | Sanayi/imalat KOBİ'leri | Dijital olgunluğunu artırmak isteyen KOBİ'ler |
| Örnek yatırım | Güneş enerjisi, atık azaltma, verimlilik ekipmanı | ERP/MES yazılımı, otomasyon, veri altyapısı |

## Hangi Durumda Hangisi?

- **Enerji maliyetlerinizi düşürmek, atığı azaltmak, yenilenebilir enerjiye geçmek** istiyorsanız → Yeşil Sanayi yönü mantıklıdır.
- **Üretim/iş süreçlerinizi dijitalleştirmek, otomasyon ve yazılımla verimlilik kazanmak** istiyorsanız → Dijital Dönüşüm yönü uygundur.

İki ihtiyaç da varsa, hangisinin **ölçülebilir geri dönüşü daha net ve projeniz daha olgun** ise ondan başlamak genelde daha akıllıcadır.

## Karar Öncesi Kontrol Listesi

- İşletmenizin NACE kodu ve yaşı, hedef programın uygunluk kriterine uyuyor mu?
- Yatırım konunuz, programın desteklediği kalemlerle örtüşüyor mu?
- Beklenen sonucu (enerji tasarrufu %, verimlilik artışı %, vb.) somut sayılarla gösterebiliyor musunuz?

## Sonuç

İki program da yüksek katma değer sağlar; doğru tercih, "hangisi daha çok para veriyor" değil, **"hangisi benim yatırımıma ve önceliğime uyuyor"** sorusunun cevabıdır.

---

Programların güncel üst limitleri, oranları ve başvuru koşulları KOSGEB kararıyla değişebilir; başvuru öncesi **kosgeb.gov.tr** üzerinden ilgili programın güncel Uygulama Esaslarını inceleyin. Hangi programa uygun olduğunuzu görmek için ücretsiz uygunluk testimizi kullanabilirsiniz.
`,
    faq: [
      { q: 'Yeşil Sanayi ve Dijital Dönüşüm programlarına aynı anda başvurabilir miyim?', a: 'Programların kendi uygulama esasları ve uygunluk kuralları vardır; aynı yatırım için iki ayrı programdan mükerrer destek genelde mümkün değildir. Önceliğinize en uygun, projesi en olgun olan programdan başlamak önerilir.' },
      { q: 'Hangi program daha çok hibe veriyor?', a: 'Üst limitler ve oranlar programa, yatırım konusuna ve güncel Uygulama Esaslarına göre değişir. Karar verirken tutardan çok, yatırımınızın programa uygunluğuna ve geri dönüşünün netliğine bakın.' },
      { q: 'Hangi programa uygun olduğumu nasıl anlarım?', a: 'İşletmenizin NACE kodu, yaşı, sektörü ve yatırım konusu belirleyicidir. Sitemizdeki ücretsiz uygunluk testi ile hızlıca ön değerlendirme yapabilirsiniz.' },
    ],
  },

  'kosgeb-basvurusu-reddedilirse-ne-yapmali': {
    title: 'KOSGEB Başvurusu Reddedilirse Ne Yapmalı? İtiraz ve Yeniden Başvuru',
    description: 'KOSGEB başvurunuz reddedildiyse panik yapmayın. Red nedenini öğrenme, itiraz hakkı ve bir sonraki dönem güçlü başvuru için adım adım rehber.',
    category: 'İpucu',
    readMin: 7,
    dateStr: 'Haziran 2026',
    content: `
## Başvurum Reddedildi, Bu Son mu?

Hayır. KOSGEB başvurusunun reddedilmesi, bir daha başvuramayacağınız anlamına gelmez. Çoğu red, **düzeltilebilir** eksikliklerden kaynaklanır: eksik belge, zayıf gerekçelendirme, bütçe-faaliyet uyumsuzluğu veya uygunluk kriterlerinin karşılanmaması. Önce red nedenini net olarak anlamak, sonra ona göre hareket etmek gerekir.

## Adım 1: Red Nedenini Öğrenin

Değerlendirme sonucu ve gerekçesi, başvuruyu yaptığınız KOSGEB e-Hizmetler (edevlet.kosgeb.gov.tr) sistemindeki başvuru kaydınızda yer alır. Ayrıca bağlı bulunduğunuz **KOSGEB İl Müdürlüğü** ile görüşerek gerekçe hakkında daha ayrıntılı bilgi alabilirsiniz.

Red nedenleri genellikle iki gruba ayrılır:

- **Uygunluk (ön eleme) reddi:** Vergi/SGK borcu, pasif KOSGEB kaydı, yaş/sektör kriterine uymama gibi. Bunlar genelde başvurunun jüriye bile gitmeden elenmesine yol açar.
- **Değerlendirme (jüri) reddi:** Proje jüriye gitmiş ama yeterli puanı alamamıştır. Burada sorun içeriğin kalitesi, gerçekçiliği ve gerekçelendirmesidir.

## Adım 2: İtiraz Hakkınızı Değerlendirin

KOSGEB süreçlerinde, sonuca **itiraz** edebileceğiniz bir süre tanımlanır. İtiraz, kararın hatalı olduğunu düşündüğünüz somut bir gerekçeniz varsa anlamlıdır (örneğin sistem bir belgenizi görmemişse). İtiraz süresi ve yöntemi başvuru sonucuyla birlikte bildirilir; bu süreyi kaçırmayın.

İtirazın kabulü garanti değildir; bu yüzden çoğu durumda en sağlıklı yol, **eksikleri giderip bir sonraki başvuru döneminde daha güçlü bir dosyayla** tekrar başvurmaktır.

## Adım 3: Eksikleri Giderin

| Red Nedeni | Çözüm |
|---|---|
| Vergi / SGK borcu | Borcu kapatın veya yapılandırın; "borcu yoktur" belgesi alın |
| Pasif KOSGEB kaydı | edevlet.kosgeb.gov.tr üzerinden kaydı aktif hale getirin |
| Zayıf gerekçelendirme | Her bütçe kalemini "neden gerekli, ne kazandıracak" mantığıyla yeniden yazın |
| Afaki/abartılı hedefler | Sektör ortalamalarına dayalı, ölçülebilir ve gerçekçi hedefler koyun |
| NACE-program uyumsuzluğu | Faaliyet kodunuzun programa uygunluğunu doğrulayın |

## Adım 4: Bir Sonraki Döneme Güçlü Hazırlanın

KOSGEB yılda birden fazla başvuru dönemi açar. Reddi bir "geri bildirim" olarak kullanın: jürinin zayıf bulduğu noktaları güçlendirin, somut sayısal verilerle destekleyin ve dosyanızı profesyonel bir kurguyla yeniden hazırlayın. İyi gerekçelendirilmiş, tutarlı ve gerçekçi bir başvuru, ikinci denemede kabul şansını belirgin şekilde artırır.

---

Güncel başvuru dönemleri ve resmi sonuç/itiraz süreçleri için her zaman **kosgeb.gov.tr** ve KOSGEB e-Hizmetler sistemini esas alın. Koşullar KOSGEB kararıyla değişebilir.
`,
    faq: [
      { q: 'KOSGEB başvurusu reddedilince tekrar başvurabilir miyim?', a: 'Evet. Red, kalıcı bir engel değildir. Eksikleri giderip bir sonraki başvuru döneminde yeniden başvurabilirsiniz. KOSGEB yıl içinde birden fazla başvuru dönemi açar.' },
      { q: 'Red nedenini nereden öğrenirim?', a: 'Değerlendirme gerekçesi KOSGEB e-Hizmetler (edevlet.kosgeb.gov.tr) sistemindeki başvuru kaydınızda yer alır. Ayrıca bağlı olduğunuz KOSGEB İl Müdürlüğü ile görüşerek ayrıntılı bilgi alabilirsiniz.' },
      { q: 'Red kararına itiraz edebilir miyim?', a: 'Evet, sonuçla birlikte bildirilen süre içinde itiraz hakkınız vardır. İtiraz, kararın hatalı olduğuna dair somut bir gerekçeniz olduğunda anlamlıdır. Aksi halde eksikleri giderip yeniden başvurmak genellikle daha sonuç odaklıdır.' },
      { q: 'En sık red nedenleri nelerdir?', a: 'Vergi/SGK borcu, pasif KOSGEB kaydı, NACE-program uyumsuzluğu, zayıf veya abartılı gerekçelendirme ve eksik belgeler en sık karşılaşılan red nedenleridir.' },
    ],
  },

  'kadin-girisimci-kosgeb-destekleri-2026': {
    title: 'Kadın Girişimci KOSGEB Destekleri 2026: Avantajlar ve Başvuru',
    description: 'Kadın girişimciler için KOSGEB destekleri, ek hibe avantajları ve başvuru adımları. 2026 güncel bilgilerle kadın girişimci destek rehberi.',
    category: 'Program Analizi',
    readMin: 6,
    dateStr: 'Haziran 2026',
    content: `
## Kadın Girişimciler İçin KOSGEB Avantajı

KOSGEB, girişimciliği yaygınlaştırmak amacıyla **kadın, genç ve engelli girişimcilere** çeşitli programlarda ek avantajlar tanır. Kadın girişimciler için bu avantaj genellikle **daha yüksek destek üst limiti** veya **ek geri ödemesiz destek** şeklinde uygulanır. Yani aynı projeyi sunan iki girişimciden kadın girişimci, belirli kalemlerde daha fazla destekten yararlanabilir.

## Hangi Programlara Başvurulabilir?

Kadın girişimciler, KOSGEB'in tüm ana programlarına başvurabilir; ek avantajlar özellikle **Girişimci Destek Programı** kapsamında öne çıkar:

- **İş Kurma / İş Geliştirme Destekleri:** Yeni kurulan işletmeler için kuruluş, makine-teçhizat, yazılım ve işletme giderlerine yönelik destekler.
- **KOBİ Gelişim ve sektörel programlar:** Mevcut işletmenizi büyütmek, dijitalleşmek veya ihracata yönelmek için.

Önemli olan, işletmenizin **KOSGEB veri tabanına kayıtlı ve aktif** olması ve faaliyet kodunuzun (NACE) başvurduğunuz programa uygun olmasıdır.

## Başvuru Adımları

1. **KOSGEB kaydı:** edevlet.kosgeb.gov.tr adresine e-Devlet şifrenizle girip KOSGEB Veri Tabanı kaydınızı yapın/aktifleştirin.
2. **Uygunluk kontrolü:** İşletme yaşı, sektör ve borç durumu açısından programa uygunluğunuzu doğrulayın.
3. **Eğitim:** Bazı girişimcilik desteklerinde Uygulamalı Girişimcilik Eğitimi sertifikası istenebilir.
4. **Proje/başvuru dosyası:** İş planı, bütçe ve gerekçelerinizi içeren dosyanızı hazırlayın.
5. **Başvuru:** KOSGEB e-Hizmetler üzerinden başvurunuzu gönderin.

## Güçlü Başvuru İçin İpuçları

- Kadın girişimci avantajını projenizin **gerçekçiliğiyle** birleştirin; ek limit, zayıf bir projeyi kurtarmaz.
- İstihdam hedeflerinizde, özellikle kadın istihdamına katkıyı somut sayılarla belirtin.
- Bütçe kalemlerini sektör gerçeklerine uygun, ölçülebilir gerekçelerle açıklayın.

---

Güncel destek tutarları, oranları ve ek avantajların kapsamı KOSGEB kararıyla değişebilir; başvuru öncesi mutlaka **kosgeb.gov.tr** üzerinden ilgili programın güncel Uygulama Esaslarını kontrol edin.
`,
    faq: [
      { q: 'Kadın girişimcilere KOSGEB ek destek veriyor mu?', a: 'Evet. KOSGEB, kadın (ayrıca genç ve engelli) girişimcilere belirli programlarda daha yüksek üst limit veya ek geri ödemesiz destek şeklinde avantaj tanır. Kapsam ve tutarlar programın güncel Uygulama Esaslarına göre değişir.' },
      { q: 'Kadın girişimci olarak hangi programa başvurmalıyım?', a: 'Yeni kurduysanız Girişimci Destek Programı, mevcut işletmenizi büyütüyorsanız KOBİ Gelişim ve sektörel programlar uygundur. İşletme yaşınıza ve sektörünüze göre uygunluk testi yaptırmanız önerilir.' },
      { q: 'Başvuru için hangi şartlar gerekli?', a: 'İşletmenizin KOSGEB veri tabanına kayıtlı ve aktif olması, vergi/SGK borcunuzun bulunmaması ve NACE kodunuzun programa uygun olması temel şartlardır. Bazı desteklerde girişimcilik eğitimi sertifikası istenebilir.' },
    ],
  },

  'kosgeb-hibe-basvurusu-nasil-yapilir': {
    title: 'KOSGEB Hibe Başvurusu Nasıl Yapılır? (2026 Güncel Rehber)',
    description: 'Adım adım KOSGEB hibe başvuru süreci: kayıt, belgeler, başvuru formu ve sık yapılan hatalar. 2026 güncel.',
    category: 'Başvuru Rehberi',
    readMin: 8,
    dateStr: 'Mart 2026',
    content: `
## KOSGEB Hibe Başvurusu Nedir?

KOSGEB (Küçük ve Orta Ölçekli İşletmeleri Geliştirme ve Destekleme İdaresi Başkanlığı), Türkiye'deki KOBİ'lere geri ödemesiz hibe ve kredi faiz desteği sağlayan devlet kurumudur. Her yıl 3 ayrı başvuru döneminde on binlerce işletme başvuru yapmaktadır.

2025 yılında toplam **2.45 milyar ₺** hibe dağıtılmış, **1.699 proje** desteklenmiştir.

## Başvuru Öncesi Zorunlu Kontroller

Başvuru yapmadan önce şu maddeleri eksiksiz kontrol edin. Bu kontrollerden herhangi birinde sorun çıkması başvurunuzu anında reddettirilebilir:

- **KOSGEB Kaydı:** edevlet.kosgeb.gov.tr adresine girerek kaydınızın "Aktif" durumda olduğunu teyit edin. Pasif kayıt başvuruya engel oluşturur.
- **Vergi Borcu:** Türkiye Gelir İdaresi Başkanlığı (GİB) üzerinden vergi borcu sorgulaması yapın. Vadesi geçmiş herhangi bir vergi borcu diskalifiye sebebidir.
- **SGK Borcu:** SGK e-bildirge sisteminden prim borcunuzu kontrol edin. Yapılandırılmış borcun bile belirtilmesi gerekebilir.
- **NACE Kodu Uyumluluğu:** İşletmenizin faaliyet kodu ile başvuru programı arasındaki sektörel eşleşmeyi doğrulayın. Bazı NACE kodları belirli programlardan hariç tutulmuştur.
- **Ortaklık Durumu:** Son 3 yıl içinde başka bir şirkette %25 veya daha fazla payınız varsa İş Geliştirme Desteği'ne uygunluğunuz sorgulanabilir.

## Hangi Belgeleri Hazırlamanız Gerekiyor?

KOSGEB programlarına bağlı olarak istenen belgeler değişse de temel belgeler şunlardır:

- **Şirket Kuruluş Belgesi:** Ticaret Sicil Gazetesi'nden güncel suret
- **İmza Sirküleri:** Noter onaylı, 6 aydan eski olmayan
- **Ortaklar ve Pay Dağılım Listesi:** Tüm ortakların TC kimlik numaralarıyla birlikte
- **Vergi Borcu Yokluğu Yazısı:** Son 30 gün içinde alınmış
- **SGK Borcu Yokluğu Yazısı:** Son 30 gün içinde alınmış
- **Banka Hesap Bilgileri:** IBAN'ın işletmeye ait olduğuna dair belge
- **Proje Özeti:** Başvurduğunuz programa göre proje tanımı
- **Mali Tablolar:** Son 2 yıl bilanço ve gelir tablosu (büyük ölçekli destek talepleri için)

## Adım Adım Başvuru Süreci

### Adım 1: Uygunluk Analizi

Hangi programa başvuracağınızı belirleyin. İşletme yaşınız, sektörünüz ve çalışan sayınız belirleyicidir. kosgebhibe.com ücretsiz uygunluk testini kullanarak size en uygun programı 2 dakikada öğrenebilirsiniz.

### Adım 2: Proje Dosyasını Hazırlama

KOSGEB başvurusunun en kritik kısmı proje dosyasıdır. Şunları içermesi gerekir:

- İş fikri ve hedefler (en az 300 kelime, özgün)
- Pazar analizi ve rekabet değerlendirmesi
- Finansal projeksiyon (3 yıllık gelir-gider tahmini)
- Proje takvimi (Gantt şeması veya tablo)
- Beklenen istihdam artışı

### Adım 3: e-Devlet Üzerinden Başvuru

1. edevlet.kosgeb.gov.tr adresine e-Devlet şifresiyle girin
2. "Destek Başvurusu" menüsünü seçin
3. İlgili programı seçip başvuru formunu doldurun
4. Belgeleri PDF formatında yükleyin (her dosya max 10 MB)
5. Başvuruyu gönderin ve referans numarasını kayıt altına alın

### Adım 4: Değerlendirme Süreci

Başvurular bir ön kontrol aşamasından geçer. Belge eksikliği olması durumunda tamamlatma süresi verilir. Bu süreyi kaçırmak başvurunun düşmesine neden olur.

KOBİGEL gibi jürili programlarda sözlü sunum aşaması da bulunmaktadır.

## 2026 Başvuru Takvimi

| Dönem | Açılış | Kapanış |
|---|---|---|
| 1. Dönem | Mart 2026 | 30 Nisan 2026 |
| 2. Dönem | Haziran 2026 | Temmuz 2026 (tahmini) |
| 3. Dönem | Ekim 2026 | Kasım 2026 (tahmini) |

## Sık Yapılan Hatalar

- Belgelerin tarihinin geçmiş olması (taze belge alınmalıdır)
- Proje özetinin çok kısa veya genel kalması
- Yanlış program seçimi (işletme yaşı koşulunu gözden kaçırma)
- Son başvuru gününü beklemek (portal yoğunluğu nedeniyle teknik sorun yaşanabilir)
- Ortaklık hissesini bildirmemek

---

**kosgebhibe.com ile başvuru dosyanızı 499 ₺'ye hazırlayın. Jüriye sunmayı unutmayın: güçlü bir proje özeti, desteklenme oranını 3 kat artırıyor.**
    `,
    faq: [
      { q: 'KOSGEB başvurusu nereden yapılır?', a: 'Başvurular KOSGEB e-Hizmetler sistemi (edevlet.kosgeb.gov.tr) üzerinden, e-Devlet şifrenizle giriş yapılarak çevrimiçi gönderilir. Önce KOSGEB Veri Tabanı kaydınızın aktif olması gerekir.' },
      { q: 'KOSGEB başvurusu için hangi belgeler gerekir?', a: 'Genellikle güncel vergi levhası, ticaret sicil gazetesi, KOSGEB veri tabanı kaydı, iş planı ve bütçe tablosu istenir. Program ve işletme türüne göre ek belgeler gerekebilir.' },
      { q: 'KOSGEB hibesi geri ödenir mi?', a: 'Programa göre değişir. Bazı destekler geri ödemesiz hibe, bazıları faizsiz/düşük faizli geri ödemeli kredi, bazıları ise karma yapıdadır. İlgili programın Uygulama Esaslarını kontrol edin.' },
      { q: 'Başvuru sonucu ne zaman belli olur?', a: 'Süre programa ve başvuru yoğunluğuna göre değişir; ön eleme ardından jüri/kurul değerlendirmesi yapılır. Sonuç ve gerekçe KOSGEB e-Hizmetler sistemindeki başvuru kaydınıza işlenir.' },
    ],
  },

  'kosgeb-is-gelistirme-destegi-nedir': {
    title: 'İş Geliştirme Desteği (İGD) Nedir? 2026 Koşulları ve Başvuru Rehberi',
    description: '1.500.000 ₺\'ye kadar geri ödemesiz hibe. 2026 yılı İş Geliştirme Desteği koşulları, kimler başvurabilir, belgeler nelerdir?',
    category: 'Program Analizi',
    readMin: 7,
    dateStr: 'Mart 2026',
    content: `
## İş Geliştirme Desteği Nedir?

İş Geliştirme Desteği (İGD), KOSGEB'in yeni ve küçük işletmelere sunduğu **geri ödemesiz hibe programıdır**. Program, işletmelerin ilk kritik yıllarında ayakta kalmasını ve büyümesini desteklemek amacıyla tasarlanmıştır.

2026 yılı itibarıyla bu programda destek üst limiti **1.500.000 ₺**'ye çıkarılmıştır.

## Kimler Başvurabilir?

İş Geliştirme Desteği'nden yararlanabilmek için aşağıdaki kriterlerin tamamını karşılamanız gerekir:

- İşletme kuruluş tarihi itibarıyla **3 yılı aşmamış** olmalıdır (36 ay)
- KOSGEB veri tabanına kayıtlı ve kaydı aktif olmalıdır
- Vergi ve SGK prim borcu bulunmamalıdır
- Yasaklı sektörler listesinde yer almamalıdır (silah, alkol, tütün üretimi vb.)
- KOBİ tanımına uygun olmalıdır (çalışan sayısı ve ciro koşulları)

## Destek Kalemleri ve Limitleri

İGD kapsamında şu harcama kalemleri desteklenmektedir:

- **Makine ve Teçhizat:** İşletmenizin faaliyet konusuyla doğrudan ilişkili ekipman
- **Yazılım:** ERP, muhasebe, e-ticaret yazılımları
- **Tanıtım ve Pazarlama:** Web sitesi, reklam, fuar katılımı
- **Eğitim ve Danışmanlık:** İşletme sahipleri ve çalışanlara yönelik mesleki eğitim
- **İşletme Giderleri (kira, fatura):** Belirli koşullar altında

Her kalem için ayrı limitler uygulanabilmektedir. Toplam destek tutarı **1.500.000 ₺**'yi aşamaz.

## Özel Kategoriler — Ek Destek

Şu kategorilerdeki girişimciler standart limite **ek 150.000 ₺** destek alabilir:

- Kadın girişimciler
- Genç girişimciler (18-35 yaş)
- Engelli girişimciler
- Şehit ve gazi ailesinden girişimciler

Bu durumda maksimum destek **1.650.000 ₺**'ye ulaşmaktadır.

## Başvuru için Gerekli Belgeler

- Ticaret Sicil Gazetesi (kuruluş ve güncel)
- İmza sirküleri (noter onaylı, 6 aydan eski olmayan)
- Vergi borcu yokluğu yazısı
- SGK prim borcu yokluğu yazısı
- Ortaklar listesi ve pay dağılımı
- Proje özeti ve iş planı
- Tahmini harcama listesi (proforma fatura veya piyasa araştırması)

## Değerlendirme Süreci

İGD başvuruları önce ön incelemeye alınır. Belge eksikliği varsa tamamlatma talebi gelir. Ön incelemeyi geçen başvurular uzman değerlendirmesine girer.

Desteklenmesi uygun bulunan projeler sahibiyle iletişime geçilerek sözleşme imzalanır. Harcamalar yapıldıktan sonra faturalar KOSGEB'e sunularak geri ödeme talep edilir.

**Önemli Not:** İGD, harcama sonrası geri ödeme modeliyle çalışmaktadır. Parayı peşin almış gibi davranmayın; önce harcama yapın, sonra belgeleyin.

## 2026 Başvuru Dönemleri

- **1. Dönem:** Mart–Nisan 2026 (aktif)
- **2. Dönem:** Haziran–Temmuz 2026 (tahmini)
- **3. Dönem:** Ekim–Kasım 2026 (tahmini)

---

**kosgebhibe.com ile İGD başvuru dosyanızı 3–5 dakikada hazırlayın. 499 ₺'ye profesyonel proje özeti, iş planı ve belge kontrol listesi.**
    `,
  },

  'kobigel-2026-basvuru-rehberi': {
    title: 'KOBİGEL 2026 Başvuru Rehberi — 5 Milyon ₺ Hibe için Tam Kılavuz',
    description: 'KOBİGEL KOBİ Gelişim Programı 2026: jüri sistemi, proje yazımı, sözlü sunum ve 5 milyon ₺ hibe için ipuçları.',
    category: 'Program Analizi',
    readMin: 10,
    dateStr: 'Mart 2026',
    content: `
## KOBİGEL Nedir?

KOBİGEL (KOBİ Gelişim Destek Programı), KOSGEB'in orta ve ileri ölçekli işletmelere yönelik **en yüksek tutarlı hibe programıdır**. 2026 yılında tek projeye verilebilecek maksimum destek **5.000.000 ₺**'ye ulaşmaktadır.

Program, diğer KOSGEB desteklerinden farklı olarak **jüri değerlendirmesi** içermekte ve sözlü sunum aşaması gerektirmektedir. Bu da proje kalitesini rakiplerinizden fark etmenize olan ihtiyacı artırmaktadır.

## 2026 Yılı Öncelikleri

KOBİGEL her yıl değerlendirme önceliklerini ilan eder. 2026 yılında öne çıkan başlıklar:

- **Dijital dönüşüm:** İmalat ve hizmet sektörlerinde otomasyon, ERP ve dijitalleşme projeleri
- **Yeşil üretim:** Enerji verimliliği, geri dönüşüm ve karbon ayak izi azaltma
- **İhracat odaklılık:** Yurt dışı pazar hedefleyen ve ihracat potansiyeli taşıyan projeler
- **İstihdam artışı:** Yeni istihdam yaratacak büyüme projeleri

Projenizin bu öncelik alanlarından en az birini karşılaması puan avantajı sağlar.

## Kimler Başvurabilir?

- KOBİ tanımı kapsamındaki işletmeler (250 kişiden az çalışan, yıllık ciro 250 milyon ₺ altında)
- KOSGEB'e kayıtlı ve aktif olan firmalar
- Vergi ve SGK borcu bulunmayan işletmeler
- Son 3 yıl içinde KOBİGEL'den destek almamış firmalar

**İş Geliştirme Desteği'nden farklı olarak** işletme yaşı koşulu yoktur; kurulu her KOBİ başvurabilir.

## Başvuru ve Değerlendirme Süreci

KOBİGEL iş akışı 5 aşamadan oluşur:

### Aşama 1: Çevrimiçi Başvuru
edevlet.kosgeb.gov.tr üzerinden başvuru formu doldurulur. Proje özeti, iş planı ve destekleyici belgeler yüklenir.

### Aşama 2: Ön Değerlendirme
KOSGEB uzmanları başvuruları teknik açıdan inceler. Belge eksikliği varsa 5 iş günü içinde tamamlatma talep edilir.

### Aşama 3: Puanlama
Başvurular bir puanlama sistemiyle değerlendirilir. Puan eşiğini geçen projeler jüri aşamasına davet edilir.

### Aşama 4: Sözlü Sunum (Jüri)
Jüri karşısında 15–20 dakikalık sunum yapılır. Jüri genellikle 3–5 akademisyen/iş insanından oluşur. Sorulara hazırlıklı olun.

### Aşama 5: Destek Kararı
Jüri sonuçlarına göre desteklenecek projeler açıklanır. Sözleşme imzalandıktan sonra harcamalar başlatılabilir.

## Güçlü Bir Proje Özeti Nasıl Yazılır?

KOBİGEL proje değerlendirmesinde en kritik faktör proje özeti kalitesidir. Güçlü bir proje özeti şu unsurları içermeli:

- **Problem tanımı:** Hangi sorunu çözüyorsunuz?
- **Çözümünüzün özgündüğü:** Piyasadaki mevcut seçeneklerden farkı nedir?
- **Hedef kitle:** Müşterileriniz kim?
- **Pazar büyüklüğü:** Adreslenebilir pazar ne kadar?
- **Finansal sürdürülebilirlik:** 3 yıllık gelir projeksiyonu gerçekçi mi?
- **İstihdam etkisi:** Kaç yeni çalışan alacaksınız?

## Harcama Kalemleri

KOBİGEL kapsamında desteklenen başlıca harcama kalemleri:

- Makine, teçhizat ve yazılım alımları
- Proses geliştirme ve teknoloji transferi giderleri
- Test, analiz ve kalibrasyon
- Belgelendirme ve sertifikasyon
- Tanıtım ve pazarlama faaliyetleri
- Personel giderleri (belirli koşullar altında)

## İpuçları — Başvurunuzu Öne Çıkarın

- Finansal projeksiyonlarınızı gerçekçi tutun; fazla iyimser rakamlar jüride güvensizlik yaratır
- Projenizin dijital veya yeşil dönüşüme katkısını açıkça belirtin
- İhracat potansiyelinizi sayılarla destekleyin
- Sözlü sunumda 5 dakikalık ön hazırlık yapın ve olası soruları listeleyin
- Belge eksikliği tamamlatma süresinin son gününü beklemeyin

---

**kosgebhibe.com'da KOBİGEL proje özeti, iş planı ve finansal projeksiyon 499 ₺'ye hazırlanır. Jüriye hazır, profesyonel dosya.**
    `,
  },

  'kosgeb-basvurularinda-en-cok-yapilan-hatalar': {
    title: 'KOSGEB Başvurularında En Çok Yapılan 7 Hata ve Çözümleri',
    description: 'Başvuruların büyük çoğunluğu bu 7 hatadan biriyle reddediliyor. Hatalardan nasıl kaçınacağınızı öğrenin.',
    category: 'İpucu',
    readMin: 6,
    dateStr: 'Mart 2026',
    content: `
## Neden Bu Kadar Çok Başvuru Reddediliyor?

Her başvuru döneminde binlerce işletme KOSGEB'e başvuru yapıyor. Ancak başvuruların önemli bir kısmı değerlendirmeye alınmadan teknik red alıyor. Bunun en büyük nedeni önlenebilir hatalar.

Aşağıda en sık karşılaşılan 7 hata ve bunlardan nasıl kaçınılacağı açıklanmaktadır.

## Hata 1: Tarihi Geçmiş Belge Kullanmak

Vergi borcu yokluğu yazısı, SGK prim borcu yokluğu yazısı ve imza sirküleri için geçerlilik süresi vardır. Çoğu KOSGEB programı **son 30 gün içerisinde** alınmış belgeler talep eder.

**Çözüm:** Başvuru tarihine yakın, mümkünse son 1 hafta içinde tüm belgeleri yenileyin.

## Hata 2: Yanlış NACE Kodu

İşletmenizin ticaret sicilindeki NACE kodu ile başvurduğunuz programın kabul ettiği kodlar eşleşmiyorsa başvurunuz reddedilir. Bazı kodlar (özellikle tarım, madencilik, finans) bazı programlardan muaf tutulmuştur.

**Çözüm:** Başvurmadan önce kosgebhibe.com NACE sorgulama aracını kullanarak kodunuzu kontrol edin.

## Hata 3: Ortaklık Durumunu Beyan Etmemek

Son 3 yıl içinde başka bir şirkette %25 veya üzeri ortaklığınız varsa İş Geliştirme Desteği'ne uygunluğunuz sorgulanır. Bu durumu beyan etmemek hukuki sorun doğurabilir.

**Çözüm:** Ortaklık geçmişinizi eksiksiz beyan edin. Şüphe duyduğunuz durumlarda KOSGEB danışma hattını arayın.

## Hata 4: Proje Özetinin Çok Kısa veya Genel Olması

"Tekstil sektöründe faaliyet göstermekteyiz ve büyümek istiyoruz" türünde genel ifadeler değerlendirme puanını düşürür. Jüri, somut ve ölçülebilir hedefler arar.

**Çözüm:** Proje özetinizde şunları mutlaka belirtin: hedef pazar, rekabet üstünlüğü, 3 yıllık gelir tahmini, istihdam etkisi.

## Hata 5: Yanlış Program Seçimi

İşletme yaşı 3 yılı geçmişse İş Geliştirme Desteği'ne başvuramazsınız. İhracat geçmişi olmayan bir firma bazı KOBİGEL bileşenlerine uygun olmayabilir.

**Çözüm:** Ücretsiz uygunluk testimizle size uygun programı 2 dakikada belirleyin.

## Hata 6: Son Günü Beklemek

Başvuru süresinin son günü portal genellikle yoğunluktan yavaşlar ya da kesintiye uğrar. Teknik sorun nedeniyle başvuruyu tamamlayamazsanız süre uzatımı verilmez.

**Çözüm:** Başvurunuzu son tarihten en az 3 iş günü önce tamamlayın.

## Hata 7: Tamamlatma Süresini Kaçırmak

KOSGEB eksik bulduğu belge için tamamlatma talebi gönderir ve genellikle 5 iş günü süre tanır. Bu sürede yanıt verilmezse başvuru düşer.

**Çözüm:** Başvuru sürecinde KOSGEB portalınızı ve kayıtlı e-postanızı düzenli takip edin.

## Özet Kontrol Listesi

Başvurmadan önce şu 7 maddeyi teyit edin:

- Belgeler 30 günden yeni mi?
- NACE kodunuz uygun mu?
- Ortaklık geçmişini eksiksiz beyan ettiniz mi?
- Proje özeti en az 300 kelime ve somut hedef içeriyor mu?
- Doğru programı seçtiniz mi?
- Başvuruyu son günden 3 gün önce yapacak mısınız?
- KOSGEB portalınızı ve e-postanızı takip ediyor musunuz?

---

**kosgebhibe.com, başvuru dosyanızı bu hataları engelleyecek biçimde adım adım kontrol ederek hazırlar. 499 ₺'ye, danışmansız.**
    `,
  },

  'kosgeb-icin-nace-kodu-nasil-belirlenir': {
    title: 'KOSGEB İçin NACE Kodu Nasıl Belirlenir? (2026 Güncel)',
    description: 'Yanlış NACE kodu KOSGEB başvurunuzu reddettiriyor. Doğru NACE kodunu nasıl bulacağınızı ve değiştireceğinizi adım adım anlattık.',
    category: 'Teknik Rehber',
    readMin: 5,
    dateStr: 'Mart 2026',
    content: `
## NACE Kodu Nedir?

NACE (Nomenclature Générale des Activités Économiques dans les Communautés Européennes), işletmelerin ekonomik faaliyetlerini sınıflandıran Avrupa kaynaklı standart bir kodlama sistemidir. Türkiye bu sistemi TÜİK aracılığıyla uyarlamış ve "NACE Rev. 2" olarak uygulamaktadır.

Ticaret sicilinde ve vergi levhasında yer alan bu kod, KOSGEB başvurusunda hangi programlara uygun olduğunuzu doğrudan belirler.

## Neden Bu Kadar Önemli?

KOSGEB programlarının bir kısmı belirli sektörlere açık, bir kısmı ise belirli sektörlere kapalıdır. Kodunuz programla eşleşmiyorsa başvurunuz otomatik olarak reddedilir.

Örneğin:
- A grubu (tarım, ormancılık) bazı İGD bileşenlerinden muaf tutulabilir
- K grubu (finans ve sigortacılık) KOBİGEL'e başvuramaz
- C grubu (imalat) tüm ana programlara açıktır

## NACE Kodunuzu Nasıl Öğrenirsiniz?

### Yöntem 1: Vergi Levhası
Vergi dairesinden aldığınız vergi levhanızda faaliyet konunuz ve NACE kodunuz yazmaktadır.

### Yöntem 2: Ticaret Sicil Kaydı
mersis.gtb.gov.tr adresinde işletmenizi sorgulayarak kayıtlı NACE kodunuzu görüntüleyebilirsiniz.

### Yöntem 3: Muhasebeci
Muhasebeci veya mali müşaviriniz size kayıtlı kodu bildirip doğru mu olduğunu kontrol edebilir.

## Kodunuz Yanlışsa Ne Yapmalısınız?

Ticaret sicilinizde veya vergi levhanızda yanlış NACE kodu kayıtlıysa bunu KOSGEB başvurusundan **önce** düzeltmeniz gerekir.

Düzeltme için:
1. Bağlı bulunduğunuz Ticaret Odası'na başvurun (faaliyet belgesi güncelleme)
2. Vergi dairesine mükellef bilgileri güncelleme formu doldurun
3. İşlem tamamlandıktan sonra güncel belgeleri alın ve KOSGEB başvurusunu yapın

Bu işlem genellikle 3–5 iş günü sürmektedir.

## Hangi NACE Kodu Size Uygun?

Seyahat acentesi işletiyorsanız → **N79** (Seyahat acentesi faaliyetleri)
Yazılım geliştiriyorsanız → **J62** (Bilgisayar programlama faaliyetleri)
Tekstil imalatçısıysanız → **C13-C15** (Tekstil ve giyim imalatı)
Restoran veya kafe işletiyorsanız → **I56** (Yiyecek ve içecek hizmeti)
E-ticaret yapıyorsanız → **G47.91** (İnternet üzerinden perakende)

## Birden Fazla Faaliyet Alanı Varsa?

Ana faaliyet konunuzu belirleyip o koda göre başvurmanız gerekir. Birden fazla kod kayıtlıysa KOSGEB başvuruda hangi kodu referans alacağınızı sorar ya da sistematik olarak ana faaliyet kodunu kullanır.

---

**kosgebhibe.com üzerindeki NACE sorgulama aracıyla kodunuzu ücretsiz kontrol edebilirsiniz.**
    `,
  },

  'kosgeb-kaydi-nasil-yapilir': {
    title: 'KOSGEB Kaydı Nasıl Yapılır? (e-Devlet Üzerinden Adım Adım)',
    description: 'KOSGEB başvurusu için veri tabanı kaydı zorunlu. e-Devlet ile nasıl kayıt olunur, kaydınız pasifse ne yapılır?',
    category: 'Teknik Rehber',
    readMin: 4,
    dateStr: 'Mart 2026',
    content: `
## KOSGEB Kaydı Neden Zorunlu?

Herhangi bir KOSGEB programına başvurabilmek için işletmenizin KOSGEB veri tabanına kayıtlı olması **zorunludur**. Kayıt olmadan yapılan başvurular sisteme alınmaz.

## Kayıt Koşulları

Aşağıdaki koşulları taşıyan işletmeler KOSGEB'e kayıt yaptırabilir:

- Türkiye'de kurulmuş, tüzel ya da gerçek kişi olarak ticari faaliyet gösteren işletmeler
- KOBİ tanımına uyan firmalar (250'den az çalışan ve yıllık ciroya göre)
- Aktif vergi mükellefi olanlar

## e-Devlet Üzerinden Kayıt Adımları

### Adım 1: KOSGEB Portalına Giriş

edevlet.kosgeb.gov.tr adresine gidin ve "e-Devlet ile Giriş" butonuna tıklayın. e-Devlet kimliğiniz yoksa e-Devlet'e PTT şubelerinden kayıt yaptırabilirsiniz.

### Adım 2: İşletme Bilgilerini Girme

Giriş yaptıktan sonra "İşletme Kaydı" bölümünü seçin. Buraya şu bilgileri girmeniz gerekir:

- TC Kimlik Numarası (işletme sahibi)
- Vergi Kimlik Numarası
- NACE Kodu (ticaret sicilinden)
- İşletme adresi ve iletişim bilgileri
- Çalışan sayısı ve ciro bilgisi

### Adım 3: Belge Yükleme

Sistemin istediği belgeleri tarayıp yükleyin:
- İmza sirküleri (noter onaylı)
- Vergi levhası
- Ticaret sicil belgesi

### Adım 4: Onay Bekleme

KOSGEB yetkilileri başvurunuzu inceler. Onay süreci genellikle **5–10 iş günü** sürer. Onay e-postası kayıtlı adresinize gönderilir.

## Kaydım Pasif — Ne Yapmalıyım?

Bir süre KOSGEB sistemiyle etkileşime girmediyseniz kaydınız "pasif" statüsüne düşmüş olabilir. Bu durumda:

1. edevlet.kosgeb.gov.tr'ye gidin
2. "Kaydımı Güncelle" veya "Kaydımı Aktif Et" seçeneğini bulun
3. İşletme bilgilerinizi güncelleyerek formu gönderin
4. Güncellenen bilgiler KOSGEB tarafından onaylandıktan sonra durumunuz "aktif" olur

## Kayıt ile Başvuru Tarihi Arasında Yeterli Süre Bırakın

Kaydın onaylanması 5–10 iş günü sürdüğü için başvuru dönemine yakın kayıt yaptırırsanız başvuruyu yetiştiremeyebilirsiniz. **Başvuru döneminden en az 15 gün önce** kayıt durumunuzu kontrol edin.

## Sık Sorulan Sorular

**Birden fazla işletmem var, hepsini kayıt ettirebilir miyim?**
Evet. Her işletme için ayrı kayıt gereklidir.

**Şahıs şirketi de kayıt olabilir mi?**
Evet. Şahıs firmaları da KOSGEB'e kayıt yaptırabilir.

**Kayıt ücreti var mı?**
Hayır, KOSGEB kaydı tamamen ücretsizdir.

---

**Kaydınız aktifse sıradaki adım başvuru dosyanızı hazırlamak. kosgebhibe.com ile 3–5 dakikada hazır dosya, 499 ₺.**
    `,
  },

  'kosgeb-hibe-miktarlari-2026': {
    title: 'KOSGEB Hibe Miktarları 2026 — Tüm Destekler ve Limitler Tablosu',
    description: '2026 yılı KOSGEB destek programları ve üst limitleri. İş Geliştirme Desteği, KOBİGEL, Kapasite Geliştirme karşılaştırması.',
    category: 'Bilgi',
    readMin: 4,
    dateStr: 'Mart 2026',
    content: `
## 2026 KOSGEB Hibe Miktarları

KOSGEB, 2026 yılı için destek üst limitlerini yeniden belirlemiştir. Aşağıdaki tabloda tüm ana programlara ait güncel limitler ve temel koşullar yer almaktadır.

## Program Karşılaştırma Tablosu

### İş Geliştirme Desteği (İGD)

- **Maksimum Destek:** 1.500.000 ₺
- **Özel Kategori Ek Desteği:** +150.000 ₺ (kadın/genç/engelli/şehit-gazi)
- **Toplam Maksimum:** 1.650.000 ₺
- **İşletme Yaşı:** 0–3 yıl
- **Ödeme Tipi:** Geri ödemesiz hibe
- **Başvuru Türü:** Bireysel değerlendirme

### KOBİGEL — KOBİ Gelişim Destek Programı

- **Maksimum Destek:** 5.000.000 ₺
- **İşletme Yaşı:** Koşul yok (KOBİ olması yeterli)
- **Ödeme Tipi:** Geri ödemesiz hibe (geri ödemeli bileşen de olabilir)
- **Başvuru Türü:** Jüri değerlendirmeli, rekabetçi

### Kapasite Geliştirme Destek Programı

- **Maksimum Destek:** 20.000.000 ₺
- **Destek Türü:** Kredi faiz desteği (geri ödemeli)
- **Ödeme Tipi:** Faiz gideri ödenir, anapar geri ödenir
- **Başvuru Türü:** Bankalar aracılığıyla

### Girişimcilik Desteği

- **Maksimum Destek:** 100.000 ₺
- **Kapsam:** İşyeri kirası + makine-teçhizat
- **İşletme Yaşı:** Yeni kurulan işletmeler için
- **Ödeme Tipi:** Geri ödemesiz hibe

## Hangi Program Size Daha Uygun?

| Kriter | İGD | KOBİGEL | Kapasite |
|---|---|---|---|
| Kurulu 3 yıldan az | ✓ | ✓ | ✓ |
| Kurulu 3 yıldan fazla | ✗ | ✓ | ✓ |
| Geri ödemesiz | ✓ | ✓ | ✗ |
| Yüksek tutar | — | ✓ (5M ₺) | ✓ (20M ₺) |
| Jüri gerekiyor | ✗ | ✓ | ✗ |

## Önemli Notlar

- Limitler **üst sınırı** göstermektedir. Uygunluk, harcama miktarı ve proje kalitesine göre gerçek destek daha az olabilir.
- KOBİGEL'de desteklerin tamamı tek seferde ödenmez; harcama belgelerine göre kısım kısım ödeme yapılır.
- Kapasite Geliştirme desteği anapara değil, faiz giderini karşılar.

## 2026 Toplam Bütçe

KOSGEB'in 2026 yılı için toplam destek bütçesi geçen yıla göre artırılmış olup tahmini olarak **3–4 milyar ₺** düzeyindedir. Ancak bu bütçe yıl boyunca 3 döneme bölünür.

---

**Hangi programa uygun olduğunuzu öğrenmek için kosgebhibe.com ücretsiz uygunluk testini yapın. Başvuru dosyanızı 499 ₺'ye hazırlayın.**
    `,
  },

  'kosgeb-2026-destekleri': {
    title: 'KOSGEB 2026 Destekleri: İşletmenize Uygun Programı Nasıl Seçersiniz?',
    description: 'İşletme yaşınız, sektörünüz ve projenize göre 2026 KOSGEB programları karşılaştırması. Doğru programı seçin, başvurunuzu güçlendirin.',
    category: 'Başvuru Rehberi',
    readMin: 7,
    dateStr: 'Mart 2026',
    content: `
## KOSGEB 2026: Hangi Programı Seçmelisiniz?

KOSGEB, 2026 yılında farklı işletme profillerine yönelik çok sayıda destek programı sunmaktadır. Yanlış program seçimi hem zaman kaybettirir hem de başvurunuzu baştan reddettirilebilir.

Bu rehber, işletme profilinize göre doğru programı seçmenize yardımcı olmak için hazırlanmıştır.

## Eğer İşletmeniz 3 Yıldan Genç İse

İlk tercihiniz **İş Geliştirme Desteği (İGD)** olmalıdır.

- Maksimum 1.500.000 ₺ geri ödemesiz hibe
- Jüri gerekmez, bireysel değerlendirme
- Makine, yazılım, tanıtım ve işletme giderleri desteklenir
- Başvuru süreci diğer programlara göre daha basit

Kadın, genç (18-35) veya engelli girişimciyseniz ek 150.000 ₺ hak edebilirsiniz.

## Eğer İşletmeniz 3 Yıldan Eski İse

İGD'ye başvuramazsınız. Alternatif seçenekler:

### KOBİGEL — KOBİ Gelişim Programı
Büyük ölçekli ve yenilikçi projeler için. Maksimum 5.000.000 ₺. Jüri değerlendirmesi var. 2026 öncelikleri: dijital dönüşüm, yeşil üretim, ihracat.

### Kapasite Geliştirme Destek Programı
Kredi faiz desteği arıyorsanız. Maksimum 20.000.000 ₺ kredi limitine kadar faiz giderleriniz karşılanır. Anaparanızı geri ödersiniz.

## Sektörünüze Göre Program Kısıtlamaları

Bazı sektörler belirli programlara başvuramaz:

- **Tarım ve hayvancılık (A grubu NACE):** Bazı İGD bileşenlerinden yararlanamaz
- **Finans ve sigortacılık (K grubu):** KOBİGEL'e başvuramaz
- **Silah, alkol, tütün:** Tüm programlar için yasaklı

Enerji, imalat, teknoloji ve hizmet sektörleri genel olarak tüm programlara açıktır.

## Projenizin Büyüklüğüne Göre Program Seçimi

Küçük ölçekli projeler (100.000–500.000 ₺): İGD veya Girişimcilik Desteği
Orta ölçekli projeler (500.000–2.000.000 ₺): İGD (3 yıldan genç) veya KOBİGEL
Büyük ölçekli projeler (2.000.000 ₺+): KOBİGEL veya Kapasite Geliştirme

## Başvuru Öncesi Yapabileceğiniz Hızlı Kontrol

Aşağıdaki 5 soruyu yanıtlayın:

1. İşletmeniz kaç yıllık? (3 yıl altı → İGD avantajlı)
2. KOSGEB kaydınız aktif mi? (Değilse önce aktifleştirin)
3. Vergi veya SGK borcunuz var mı? (Varsa önce ödeyin)
4. NACE kodunuz uygun mu? (Sorgulayın)
5. Son 3 yılda başka şirkette %25+ ortaklığınız var mıydı? (İGD için değerlendirme konusu)

## 2026 Başvuru Dönemleri

Her program yılda 3 dönem açılır:

- **1. Dönem:** Mart–Nisan 2026 (şu an aktif)
- **2. Dönem:** Haziran–Temmuz 2026
- **3. Dönem:** Ekim–Kasım 2026

1. dönemi kaçıranlar 2. dönemi bekleyebilir. Ancak dönemler arasında programlar ve limitler değişebilir.

## Özet: Karar Ağacı

İşletме yaşı < 3 yıl **→** İş Geliştirme Desteği
İşletme yaşı ≥ 3 yıl + yenilikçi proje **→** KOBİGEL
Büyük finansman ihtiyacı var **→** Kapasite Geliştirme
Yeni kurulan + küçük ölçekli **→** Girişimcilik Desteği

---

**kosgebhibe.com ile 2 dakikada uygunluk testi yapın ve en uygun KOSGEB programını belirleyin. Başvuru dosyanızı 499 ₺'ye hazırlayın.**
    `,
  },

}

export async function generateStaticParams() {
  return Object.keys(CONTENT).map(slug => ({ slug }))
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params
  const post = CONTENT[slug]
  if (!post) return {}
  return {
    title: post.title,
    description: post.description,
    openGraph: {
      title: post.title,
      description: post.description,
      type: 'article',
      locale: 'tr_TR',
    },
  }
}

function renderContent(md: string): string {
  const lines = md.split('\n')
  const out: string[] = []
  let inTable = false
  let tableHeaderDone = false

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()

    // Detect table row
    if (line.startsWith('|') && line.endsWith('|')) {
      const cols = line.slice(1, -1).split('|').map(c => c.trim())

      // Separator row: |---|---|
      if (cols.every(c => /^[-: ]+$/.test(c))) {
        if (!tableHeaderDone) tableHeaderDone = true
        continue
      }

      if (!inTable) {
        out.push('<div class="blog-table-wrap"><table class="blog-table"><thead><tr>')
        cols.forEach(c => out.push(`<th>${c}</th>`))
        out.push('</tr></thead><tbody>')
        inTable = true
        tableHeaderDone = false
      } else {
        out.push('<tr>')
        cols.forEach(c => out.push(`<td>${c}</td>`))
        out.push('</tr>')
      }
      continue
    }

    // Close table if we were in one
    if (inTable) {
      out.push('</tbody></table></div>')
      inTable = false
      tableHeaderDone = false
    }

    // Headings
    if (line.startsWith('## ')) { out.push(`<h2>${line.slice(3)}</h2>`); continue }
    if (line.startsWith('### ')) { out.push(`<h3>${line.slice(4)}</h3>`); continue }
    // HR
    if (line === '---') { out.push('<hr />'); continue }
    // List items
    if (line.startsWith('- ')) { out.push(`<li>${line.slice(2).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')}</li>`); continue }
    // Empty line
    if (line === '') { out.push('<br />'); continue }
    // Paragraph text
    const text = line.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    out.push(`<p>${text}</p>`)
  }

  if (inTable) out.push('</tbody></table></div>')

  return out.join('\n')
}

export default async function BlogPostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = CONTENT[slug]
  if (!post) notFound()

  const pageUrl = `https://kosgebhibe.com/blog/${slug}`
  const graph: Record<string, unknown>[] = [
    {
      '@type': 'Article',
      headline: post!.title,
      description: post!.description,
      inLanguage: 'tr-TR',
      author: { '@type': 'Organization', name: 'kosgebhibe.com', url: 'https://kosgebhibe.com' },
      publisher: {
        '@type': 'Organization',
        name: 'kosgebhibe.com',
        logo: { '@type': 'ImageObject', url: 'https://kosgebhibe.com/icon.png' },
      },
      mainEntityOfPage: pageUrl,
    },
    {
      '@type': 'BreadcrumbList',
      itemListElement: [
        { '@type': 'ListItem', position: 1, name: 'Ana Sayfa', item: 'https://kosgebhibe.com/' },
        { '@type': 'ListItem', position: 2, name: 'Blog', item: 'https://kosgebhibe.com/blog' },
        { '@type': 'ListItem', position: 3, name: post!.title, item: pageUrl },
      ],
    },
  ]
  if (post!.faq && post!.faq.length > 0) {
    graph.push({
      '@type': 'FAQPage',
      mainEntity: post!.faq.map((f) => ({
        '@type': 'Question',
        name: f.q,
        acceptedAnswer: { '@type': 'Answer', text: f.a },
      })),
    })
  }
  const jsonLd = { '@context': 'https://schema.org', '@graph': graph }

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <Header />
      <article className={styles.article}>
        <div className="container" style={{ maxWidth: '740px' }}>
          <div className={styles.breadcrumb}>
            <Link href="/">Ana Sayfa</Link>
            <span>›</span>
            <Link href="/blog">Blog</Link>
            <span>›</span>
            <span>{post!.category}</span>
          </div>

          <div className={styles.articleHeader}>
            <span className="badge badge-muted">{post!.category}</span>
            <h1 className="section-title" style={{ marginTop: '12px', lineHeight: '1.3' }}>{post!.title}</h1>
            <div className={styles.articleMeta}>
              <span className="fs-xs text-muted">kosgebhibe.com ekibi</span>
              <span className="fs-xs text-muted">·</span>
              <span className="fs-xs text-muted">{post!.readMin} dk okuma</span>
              <span className="fs-xs text-muted">·</span>
              <span className="fs-xs text-muted">{post!.dateStr}</span>
            </div>
          </div>

          <div
            className={styles.content}
            dangerouslySetInnerHTML={{ __html: renderContent(post!.content) }}
          />

          {post!.faq && post!.faq.length > 0 && (
            <div className={styles.content} style={{ marginTop: '32px' }}>
              <h2>Sıkça Sorulan Sorular</h2>
              {post!.faq.map((f, i) => (
                <div key={i} style={{ marginBottom: '16px' }}>
                  <h3>{f.q}</h3>
                  <p>{f.a}</p>
                </div>
              ))}
            </div>
          )}

          <div className={styles.ctaBox}>
            <div className="card-title">Başvurunuzu Hemen Hazırlayın</div>
            <p className="text-secondary fs-sm" style={{ marginTop: '8px' }}>
              Danışmanlara 5.000–20.000 ₺ ödemeden başvurunuzu 499 ₺&apos;ye hazırlayın.
            </p>
            <div style={{ display: 'flex', gap: '12px', marginTop: '16px', flexWrap: 'wrap' }}>
              <Link href="/uygunluk-testi" className="btn btn-secondary">
                Ücretsiz Uygunluk Testi
              </Link>
              <Link href="/uye-ol" className="btn btn-primary">
                Başvuru Hazırla — 499 ₺
              </Link>
            </div>
          </div>

          <div className="legal-note" style={{ marginTop: '32px' }}>
            Bu makale bilgilendirme amaçlıdır. Güncel bilgi için{' '}
            <a href="https://kosgeb.gov.tr" target="_blank" rel="noopener noreferrer">kosgeb.gov.tr</a>{' '}
            ziyaret edin. Destek tutarları ve koşullar KOSGEB kararıyla değişebilir.
          </div>
        </div>
      </article>
      <Footer />
    </>
  )
}
