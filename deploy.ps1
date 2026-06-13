# ===========================================================================
#  kosgebhibe.com — Otomatik Dağıtım (Deploy) Script'i
#  Windows sunucuda çalıştırılır. GitHub'dan son sürümü çeker, Docker ile
#  yeniden kurar ve yayına alır. Cloudflare Tunnel domaini otomatik bağlar.
#
#  Kullanım: PowerShell'i bu klasörde açıp şunu yazın:  .\deploy.ps1
# ===========================================================================

$ErrorActionPreference = "Stop"
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ProjectDir

$Compose = "docker-compose.prod.yml"

function Yaz($msg, $color = "Cyan") { Write-Host "==> $msg" -ForegroundColor $color }

Yaz "kosgebhibe.com dağıtımı başlıyor..."

# 1) .env kontrolü
if (-not (Test-Path ".env")) {
    Write-Host "HATA: .env dosyası bulunamadı." -ForegroundColor Red
    Write-Host "Çözüm: .env.example dosyasını .env adıyla kopyalayıp doldurun." -ForegroundColor Yellow
    exit 1
}

# 2) Docker çalışıyor mu?
try { docker info | Out-Null } catch {
    Write-Host "HATA: Docker Desktop çalışmıyor. Lütfen Docker Desktop'ı başlatın." -ForegroundColor Red
    exit 1
}

# 3) GitHub'dan son sürümü çek
Yaz "GitHub'dan güncellemeler alınıyor..."
git fetch --all --prune
git reset --hard origin/master

# 4) Docker imajlarını derle
Yaz "Uygulama derleniyor (birkaç dakika sürebilir)..."
docker compose -f $Compose build

# 5) Yayına al
Yaz "Servisler başlatılıyor..."
docker compose -f $Compose up -d

# 6) Eski imajları temizle
Yaz "Eski Docker imajları temizleniyor..."
docker image prune -f | Out-Null

# 7) Sağlık kontrolü (backend hazır mı?)
Yaz "Sağlık kontrolü yapılıyor..."
$ok = $false
for ($i = 1; $i -le 20; $i++) {
    Start-Sleep -Seconds 3
    try {
        $health = docker compose -f $Compose exec -T nginx wget -qO- http://backend:8000/api/health 2>$null
        if ($health -match "ok") { $ok = $true; break }
    } catch {}
    Write-Host "   ...bekleniyor ($i/20)" -ForegroundColor DarkGray
}

Write-Host ""
if ($ok) {
    Yaz "BAŞARILI! Site yayında: https://kosgebhibe.com" "Green"
} else {
    Write-Host "UYARI: Sağlık kontrolü yanıt vermedi. Logları kontrol edin:" -ForegroundColor Yellow
    Write-Host "   docker compose -f $Compose logs --tail=50" -ForegroundColor Yellow
}

Yaz "Çalışan servisler:"
docker compose -f $Compose ps
