# kosgebhibe.com — Deploy Rehberi

**Stack:** Vercel (Frontend) · Render (Backend) · Supabase (PostgreSQL) · Upstash (Redis)

---

## Adım 1 — Supabase (PostgreSQL) Kurulumu

1. [supabase.com](https://supabase.com) → **New Project** oluşturun
2. Proje oluştuktan sonra **Settings → Database → Connection string** altında şunu kopyalayın:

```
postgresql+asyncpg://postgres.[ref]:[ŞIFRE]@aws-0-eu-central-1.pooler.supabase.com:5432/postgres
```

> ⚠️ **Transaction Mode pooler** URL'ini alın (port 5432). Direct URL değil.

3. Bu URL'i bir yere not alın — backend env değişkeni olarak kullanacaksınız.

---

## Adım 2 — Upstash (Redis) Kurulumu

1. [upstash.com](https://upstash.com) → **Create Database** tıklayın
2. Region: **EU-West-1** (Frankfurt, Supabase ile yakın)
3. Database oluştuktan sonra **REST URL** değil, **Redis URL** formatını alın:

```
rediss://default:[ŞIFRE]@[host].upstash.io:6379
```

4. Bu URL'i not alın.

---

## Adım 3 — Render (Backend) Kurulumu

### 3.1 — GitHub'a Push

```bash
# Henüz repo yoksa
git init
git remote add origin https://github.com/KULLANICI/kosgeb.git
git add .
git commit -m "initial"
git push -u origin main
```

### 3.2 — Render'da Web Service Oluşturma

1. [render.com](https://render.com) → **New → Web Service**
2. GitHub reposu bağlayın
3. **Root Directory:** `backend`
4. **Runtime:** Docker (Dockerfile var)
5. **Region:** Frankfurt (EU)
6. **Plan:** Free (başlangıç için)

> ⚠️ **Önemli:** Render Free tier 15 dk inaktiviteden sonra uyku moduna geçer. Aşağıdaki Keep-Alive çözümü bunu önler.

### 3.3 — Backend Environment Variables (Render Dashboard)

**Settings → Environment Variables** bölümüne şunları girin:

| Değişken | Değer |
|---|---|
| `DEBUG` | `false` |
| `SECRET_KEY` | Güçlü rastgele bir string (min 32 karakter) |
| `DATABASE_URL` | Supabase connection string (asyncpg formatı) |
| `REDIS_URL` | Upstash Redis URL (rediss://...) |
| `GEMINI_API_KEY` | Google AI Studio'dan alın |
| `GEMINI_MODEL` | `gemini-2.5-flash` |
| `IYZICO_API_KEY` | iyzico panelinden |
| `IYZICO_SECRET_KEY` | iyzico panelinden |
| `IYZICO_SANDBOX` | `false` (canlıda) |
| `IYZICO_BASE_URL` | `https://api.iyzipay.com` |
| `SMTP_HOST` | SMTP sunucunuz |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | E-posta adresiniz |
| `SMTP_PASS` | E-posta şifreniz |
| `SMTP_FROM` | `noreply@kosgebhibe.com` |
| `FROM_EMAIL` | `noreply@kosgebhibe.com` |
| `FROM_NAME` | `kosgebhibe.com` |
| `FRONTEND_URL` | `https://kosgebhibe.com` |
| `ENCRYPTION_KEY` | Tam 32 karakter şifreleme anahtarı |
| `PAYMENT_REQUIRED` | `true` |

### 3.4 — Veritabanı Migration

Render'da servis deploy olduktan sonra **Shell** sekmesine girin:

```bash
cd /app
alembic upgrade head
```

### 3.5 — Backend URL'ini Not Alın

Render deploy tamamlandığında URL şu formatta olur:
```
https://kosgeb-backend-xxxx.onrender.com
```

---

## Adım 4 — Vercel (Frontend) Kurulumu

### 4.1 — Vercel'e Bağlanma

1. [vercel.com](https://vercel.com) → **New Project**
2. GitHub repo'yu import edin
3. **Root Directory:** `frontend`
4. **Framework Preset:** Next.js (otomatik algılar)

### 4.2 — Frontend Environment Variables (Vercel Dashboard)

**Settings → Environment Variables** bölümüne şunları girin:

| Değişken | Değer |
|---|---|
| `NEXT_PUBLIC_API_URL` | `https://kosgeb-backend-xxxx.onrender.com` |

> Render URL'inizi buraya yazın.

### 4.3 — Domain Bağlama

1. Vercel **Settings → Domains** → `kosgebhibe.com` ekleyin
2. Vercel size iki DNS kaydı gösterir:
   - `A` kaydı: `76.76.21.21`
   - `CNAME` kaydı: `cname.vercel-dns.com`
3. Domain kayıt şirketinizde (GoDaddy, Namecheap, vb.) bu kayıtları girin
4. SSL otomatik olarak Vercel tarafından sağlanır

---

## Adım 5 — Render Keep-Alive (Uyku Modunu Önleme)

Render Free tier 15 dakika inaktivitede backend'i uyutur. Bunu önlemek için:

### Yöntem A: UptimeRobot (Ücretsiz)

1. [uptimerobot.com](https://uptimerobot.com) → **Add New Monitor**
2. Monitor Type: **HTTP(s)**
3. URL: `https://kosgeb-backend-xxxx.onrender.com/health`
4. Monitoring Interval: **5 minutes**

Bu kadar — backend her zaman uyanık kalır.

### Yöntem B: GitHub Actions Cron (Alternatif)

```yaml
# .github/workflows/keepalive.yml
name: Keep Render Alive
on:
  schedule:
    - cron: '*/10 * * * *'  # Her 10 dakikada bir
jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - run: curl https://kosgeb-backend-xxxx.onrender.com/health
```

---

## Adım 6 — Son Kontroller

Deploy tamamlandıktan sonra şunları test edin:

- [ ] `https://kosgebhibe.com` → Anasayfa açılıyor mu?
- [ ] `https://kosgebhibe.com/blog` → Blog listesi çalışıyor mu?
- [ ] `https://kosgebhibe.com/uygunluk-testi` → Sayfa açılıyor mu?
- [ ] `https://kosgebhibe.com/uye-ol` → Kayıt formu görünüyor mu?
- [ ] Kayıt ol → E-posta geliyor mu?
- [ ] Google Search Console'da `kosgebhibe.com` ekleyin → sitemap.xml gönderildi mi?

---

## Hızlı Başlangıç Sırası

```
1. Supabase   → PostgreSQL URL al
2. Upstash    → Redis URL al
3. Render     → Backend deploy et, env gir, migration yap
4. Vercel     → Frontend deploy et, NEXT_PUBLIC_API_URL gir
5. Vercel     → kosgebhibe.com domain ekle
6. UptimeRobot → Backend keep-alive kur
```

---

## Sık Karşılaşılan Sorunlar

| Sorun | Çözüm |
|---|---|
| Backend 502 hatası verdi | Render loglarını kontrol et — migration yapılmamış olabilir |
| Frontend "API hatası" | `NEXT_PUBLIC_API_URL` değişkeni doğru girilmemiş |
| E-posta gelmiyor | SMTP ayarlarını ve spam klasörünü kontrol et |
| WeasyPrint PDF hatası | Render'da Docker build logunu kontrol et |
| Supabase connection timeout | Pooler URL yerine direct URL kullanıldı olabilir |
