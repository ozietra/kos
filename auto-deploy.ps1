# ===========================================================================
#  Otomatik Dağıtım Bekçisi — Windows Task Scheduler ile periyodik çalışır.
#  GitHub'da yeni commit varsa deploy.ps1'i tetikler, yoksa hiçbir şey yapmaz.
#
#  Kurulum: Görev Zamanlayıcı'da bu script'i örn. her 5 dakikada bir çalıştırın
#  (bkz. KURULUM.md). Manuel test:  .\auto-deploy.ps1
# ===========================================================================

$ErrorActionPreference = "Stop"
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ProjectDir

git fetch origin master --quiet
$local = (git rev-parse HEAD).Trim()
$remote = (git rev-parse origin/master).Trim()

if ($local -ne $remote) {
    Write-Host "Yeni sürüm bulundu ($remote). Dağıtım başlatılıyor..." -ForegroundColor Cyan
    & "$ProjectDir\deploy.ps1"
} else {
    Write-Host "Güncel. Yapılacak bir şey yok." -ForegroundColor DarkGray
}
