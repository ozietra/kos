# kosgebhibe.com — Windows Sunucu Kurulum Rehberi

Bu rehber, projeyi Windows sunucunuzda sıfırdan yayına almanız için **adım adım** hazırlandı. Teknik bilgi gerektirmez; yazdığım komutları aynen kopyalayıp yapıştırmanız yeterli. Takıldığınız her adımda ekrandaki mesajı bana iletmeniz yeterli.

> **Genel mantık:** Her şey "Docker" denen bir kutu sisteminde çalışır. Domaini "Cloudflare Tunnel" ile bağlarız (modem/port ayarı gerektirmez). GitHub'a kod gönderdiğinizde sunucu kendini otomatik günceller.

---

## 1. Gerekli Programları Kurun (tek seferlik)

### 1.1 Docker Desktop
1. Şu adrese girin: https://www.docker.com/products/docker-desktop/
2. **Download for Windows** butonuna tıklayın, inen dosyayı çalıştırın.
3. Kurulum bitince bilgisayarı yeniden başlatın.
4. Docker Desktop'ı açın. Sağ altta **balina ikonu** yeşil/sabit olunca hazırdır.

### 1.2 Git
1. Şu adrese girin: https://git-scm.com/download/win
2. İnen dosyayı çalıştırın, hep **Next** diyerek kurun (ayar değiştirmeyin).

### 1.3 (Cloudflare hesabı — domain için, 4. adımda kullanacağız)
- https://dash.cloudflare.com/sign-up adresinden **ücretsiz** hesap açın.

---

## 2. Projeyi Sunucuya İndirin (tek seferlik)

1. Başlat menüsünden **PowerShell**'i açın.
2. Projeyi koyacağınız yere gidin (örnek: C sürücüsü):
   ```powershell
   cd C:\
   ```
3. Projeyi indirin (GitHub adresinizi yazın):
   ```powershell
   git clone https://github.com/KULLANICI-ADINIZ/kosgeb.git
   cd kosgeb
   ```
   > Not: Repo'nuz özelse, kullanıcı adı + şifre (veya "personal access token") isteyebilir.

---

## 3. Ayar Dosyasını (.env) Hazırlayın (tek seferlik)

Bu dosya şifreleri ve anahtarları tutar. İçindeki örnek dosyayı kopyalayıp dolduracağız.

1. PowerShell'de (kosgeb klasöründeyken):
   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```
2. Açılan Not Defteri'nde aşağıdaki satırları doldurun. Her birinin ne olduğu:

   | Satır | Ne yazmalı / nereden alınır |
   |-------|------------------------------|
   | `SECRET_KEY` | Rastgele uzun bir yazı (örn. klavyeden 40+ karakter karışık). |
   | `ENCRYPTION_KEY` | **Tam 32 karakter** uzunluğunda bir yazı. |
   | `POSTGRES_PASSWORD` | Veritabanı için güçlü bir şifre belirleyin. |
   | `GROQ_API_KEY` | https://console.groq.com/keys → ücretsiz anahtar oluşturun, yapıştırın. |
   | `ADMIN_EMAIL` | Sizin e-posta adresiniz (yönetici olacak hesap). |
   | `CF_TUNNEL_TOKEN` | **4. adımda** Cloudflare'den alacağız, şimdilik boş bırakın. |
   | `SMTP_*` | E-posta gönderimi için (şifre sıfırlama vb.). Yoksa şimdilik boş bırakabilirsiniz. |
   | `IYZICO_*` | iyzico mağaza panelinizden (ödeme almak için). Test için boş + `IYZICO_SANDBOX=true`. |
   | `PAYTR_*` | PayTR mağaza panelinizden. Test için boş + `PAYTR_SANDBOX=true`. |

3. Kaydedip kapatın (Ctrl+S, sonra pencereyi kapatın).

> **Önemli:** Ödeme anahtarlarını henüz almadıysanız sorun değil. Site yine açılır; ödeme adımı, anahtarları girip yeniden başlattığınızda çalışır.

---

## 4. Domaini Bağlayın — Cloudflare Tunnel (tek seferlik)

Sunucunuz özel port arkasında olduğu için klasik yöntem yerine **Cloudflare Tunnel** kullanıyoruz. Hiçbir modem/port ayarı gerekmez.

### 4.1 Domaini Cloudflare'e ekleyin
1. https://dash.cloudflare.com → **Add a site** → `kosgebhibe.com` yazın → **Free** planı seçin.
2. Cloudflare size **2 adet nameserver** verir (örn. `xxx.ns.cloudflare.com`).
3. Domaini aldığınız firmanın (GoDaddy, Natro, İsimtescil vb.) panelinde, domainin **nameserver** ayarını bu ikisiyle değiştirin. (Bu değişiklik birkaç saat içinde aktifleşir.)

### 4.2 Tüneli oluşturun
1. Cloudflare panelinde sol menüden **Zero Trust**'a girin (ilk girişte ücretsiz plan seçin).
2. **Networks → Tunnels → Create a tunnel** → tür olarak **Cloudflared** seçin → bir isim verin (örn. `kosgebhibe`).
3. Karşınıza bir **token** (uzun bir `eyJ...` yazısı) çıkar. Bu token'ı kopyalayın.
4. `.env` dosyasını tekrar açıp (`notepad .env`) `CF_TUNNEL_TOKEN=` satırına yapıştırın, kaydedin.

### 4.3 Public hostname (hangi adres nereye gidecek)
Aynı tünel ekranında **Public Hostnames → Add a public hostname**:
- **Subdomain:** (boş bırakın)
- **Domain:** `kosgebhibe.com`
- **Type:** `HTTP`
- **URL:** `nginx:80`
- Kaydedin. Sonra **www** için de aynısını ekleyin (Subdomain: `www`, URL: `nginx:80`).

> Bu, "kosgebhibe.com'a gelen herkesi içerideki nginx'e yönlendir" demektir. SSL (kilit işareti) Cloudflare tarafından otomatik sağlanır.

---

## 5. Siteyi Yayına Alın

PowerShell'de, **kosgeb** klasöründeyken tek komut:

```powershell
.\deploy.ps1
```

Bu komut:
- GitHub'dan en son sürümü çeker,
- uygulamayı derler (ilk seferde 5–10 dk sürebilir),
- tüm servisleri başlatır,
- sağlık kontrolü yapar.

Sonunda **"BAŞARILI! Site yayında: https://kosgebhibe.com"** yazısını görmelisiniz. Tarayıcıda `https://kosgebhibe.com` adresini açıp kontrol edin.

> İlk kez "deploy.ps1 çalıştırılamıyor" uyarısı alırsanız, şu komutu bir kez çalıştırın, sonra tekrar deneyin:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

---

## 6. Kendinizi Yönetici (Admin) Yapın

1. Siteye normal şekilde **üye olun** (https://kosgebhibe.com/uye-ol) — `.env`'deki `ADMIN_EMAIL` ile **aynı** e-postayı kullanın.
2. Uygulamayı bir kez yeniden başlatın:
   ```powershell
   docker compose -f docker-compose.prod.yml restart backend
   ```
3. Artık https://kosgebhibe.com/admin adresine girebilirsiniz.

---

## 7. Otomatik Güncelleme (kod değişince site kendini yenilesin)

Bilgisayarınıza kod gönderdiğinizde (GitHub'a push) sunucunun kendini otomatik güncellemesi için **Görev Zamanlayıcı** kuralım:

1. Başlat → **Görev Zamanlayıcı** (Task Scheduler) açın.
2. Sağdan **Temel Görev Oluştur** → isim: `kosgebhibe-oto-deploy`.
3. Tetikleyici: **Günlük** seçin, sonra oluşturduktan sonra özelliklerinden "her 5 dakikada bir tekrarla" yapabilirsiniz (Tetikleyiciler sekmesi → Düzenle → "Görevi şu sıklıkta yinele: 5 dakika").
4. Eylem: **Program başlat**:
   - Program/komut dosyası: `powershell.exe`
   - Bağımsız değişkenler: `-ExecutionPolicy Bypass -File "C:\kosgeb\auto-deploy.ps1"`
5. Kaydedin.

Artık GitHub'a her kod gönderdiğinizde, sunucu en geç 5 dakika içinde kendini günceller.

---

## 8. Günlük Kullanım (Admin Paneli)

https://kosgebhibe.com/admin adresinden:

- **Program Güncellemeleri:** "Şimdi Güncelle" butonu KOSGEB sitesinden güncel program bilgilerini çeker ve **size onay için** listeler. Onayladıklarınız siteye yansır. (Sistem haftada bir kez de kendiliğinden kontrol eder.) Hero'daki "son başvuru tarihi" otomatik en yakın programdan gelir.
- **Fiyatlandırma:** Plan fiyatlarını TL olarak değiştirebilir, **kampanya/indirim** fiyatı ve tarih aralığı girebilirsiniz. Değişiklik birkaç dakika içinde sitedeki fiyatlara yansır.
- **Site İçeriği:** Ana sayfadaki istatistikleri ve hero rozetini düzenleyebilirsiniz. Hero rozetini **boş bırakırsanız** tarih otomatik üretilir.

---

## 9. Sık Karşılaşılan Sorunlar

| Sorun | Çözüm |
|-------|-------|
| `.env dosyası bulunamadı` | 3. adımı yapın (`Copy-Item .env.example .env`). |
| `Docker Desktop çalışmıyor` | Docker Desktop'ı açın, balina ikonu yeşil olana kadar bekleyin. |
| Site açılmıyor | Logları görün: `docker compose -f docker-compose.prod.yml logs --tail=50` |
| Domain açılmıyor | Nameserver değişikliği birkaç saat sürebilir. Cloudflare'de tünelin **Healthy** olduğunu kontrol edin. |
| Tüm servisleri görmek | `docker compose -f docker-compose.prod.yml ps` |
| Sadece yeniden başlatmak | `docker compose -f docker-compose.prod.yml restart` |
| Tamamen durdurmak | `docker compose -f docker-compose.prod.yml down` |
| Veritabanı yedeği almak | `docker compose -f docker-compose.prod.yml exec postgres pg_dump -U kosgebhibe kosgebhibe > yedek.sql` |

---

## 10. Özet Komutlar

```powershell
# Yayına al / güncelle
.\deploy.ps1

# Durum
docker compose -f docker-compose.prod.yml ps

# Loglar
docker compose -f docker-compose.prod.yml logs --tail=50

# Yeniden başlat
docker compose -f docker-compose.prod.yml restart
```

Herhangi bir adımda takılırsanız, ekrandaki kırmızı/sarı mesajı bana iletin; birlikte çözeriz.
