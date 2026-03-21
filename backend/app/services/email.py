"""
E-posta Servisi — Postal SMTP (aiosmtplib)
"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


async def _send(to_email: str, subject: str, html_body: str):
    """Tek e-posta gönder."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"kosgebhibe.com <{settings.SMTP_FROM}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    await aiosmtplib.send(
        msg,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASS,
        use_tls=False,
        start_tls=True,
    )


# ── Şablonlar ─────────────────────────────────────────────────────────────────

def _layout(body: str, title: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    body {{ font-family: -apple-system, 'Segoe UI', sans-serif; background: #FAFAF7;
            color: #1A1A18; margin: 0; padding: 40px 20px; }}
    .card {{ background: #fff; border: 1px solid #E4E3DC; border-radius: 8px;
             max-width: 540px; margin: 0 auto; padding: 36px; }}
    .logo {{ font-size: 18px; font-weight: 700; color: #1A1A18; text-decoration: none; }}
    .logo span {{ color: #C0392B; }}
    h2 {{ font-size: 20px; margin-top: 24px; }}
    p {{ font-size: 14px; line-height: 1.7; color: #6B6A62; }}
    .btn {{ display: inline-block; padding: 12px 24px; background: #C0392B; color: #fff;
            border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 14px;
            margin-top: 20px; }}
    .note {{ font-size: 12px; color: #A8A79F; margin-top: 20px; border-top: 1px solid #E4E3DC;
             padding-top: 16px; }}
    .amount {{ font-family: monospace; font-size: 28px; font-weight: 700;
               color: #1E8449; margin: 16px 0; }}
  </style>
</head>
<body>
  <div class="card">
    <a href="https://kosgebhibe.com" class="logo">kosgeb<span>hibe</span>.com</a>
    {body}
    <div class="note">
      Bu e-posta otomatik olarak gönderilmiştir. Sorularınız için{' '}
      <a href="https://kosgebhibe.com/iletisim">kosgebhibe.com/iletisim</a> adresini ziyaret edin.
    </div>
  </div>
</body>
</html>"""


async def send_welcome(email: str, name: str):
    """Üye ol → hoş geldin e-postası."""
    body = f"""
    <h2>Hoş Geldiniz, {name}!</h2>
    <p>kosgebhibe.com'a hoş geldiniz. KOSGEB hibe başvurunuzu danışman olmadan hazırlamaya başlayabilirsiniz.</p>
    <p>İlk adım olarak ücretsiz <strong>uygunluk testini</strong> yapmanızı öneririz.</p>
    <a href="https://kosgebhibe.com/dashboard" class="btn">Panele Git</a>
    """
    await _send(email, "kosgebhibe.com'a Hoş Geldiniz 🎉", _layout(body, "Hoş Geldiniz"))


async def send_payment_confirmation(email: str, name: str, plan: str, amount: float):
    """Başarılı ödeme onayı."""
    plan_label = "Starter" if plan == "starter" else "Pro"
    body = f"""
    <h2>Ödeme Onaylandı ✓</h2>
    <p>Sayın {name}, ödemeniz başarıyla alındı.</p>
    <div class="amount">{int(amount):,} ₺</div>
    <p><strong>Plan:</strong> {plan_label}</p>
    <p>Dashboard'a giderek başvurunuzu tamamlayabilir ve PDF'inizi indirebilirsiniz.</p>
    <a href="https://kosgebhibe.com/dashboard" class="btn">Başvuruma Git</a>
    <p style="margin-top:12px;font-size:12px;color:#A8A79F;">
      Fatura bilgilerini <a href="https://kosgebhibe.com/dashboard/fatura">buradan</a> görüntüleyebilirsiniz.
    </p>
    """
    await _send(email, f"Ödeme Onayı — kosgebhibe.com {plan_label}", _layout(body, "Ödeme Onayı"))


async def send_password_reset(email: str, name: str, reset_url: str):
    """Şifre sıfırlama e-postası."""
    body = f"""
    <h2>Şifre Sıfırlama</h2>
    <p>Merhaba {name}, şifre sıfırlama talebinizi aldık.</p>
    <p>Aşağıdaki butona tıklayarak yeni şifrenizi belirleyebilirsiniz. Bu bağlantı 1 saat geçerlidir.</p>
    <a href="{reset_url}" class="btn">Şifremi Sıfırla</a>
    <p style="margin-top:12px;font-size:12px;color:#A8A79F;">
      Eğer bu talebi siz yapmadıysanız bu e-postayı görmezden gelebilirsiniz.
    </p>
    """
    await _send(email, "Şifre Sıfırlama — kosgebhibe.com", _layout(body, "Şifre Sıfırlama"))


async def send_new_period_notification(email: str, name: str, program_name: str):
    """Yeni dönem bildirimi (aboneler)."""
    body = f"""
    <h2>📢 Yeni Başvuru Dönemi Açıldı!</h2>
    <p>Merhaba {name}, {program_name} için yeni başvuru dönemi açıldı!</p>
    <p>Başvurunuzu şimdi hazırlamak için panele gidin.</p>
    <a href="https://kosgebhibe.com/kosgeb-programlari" class="btn">Programlara Bak</a>
    """
    await _send(
        email,
        f"📢 {program_name} Başvuruları Açıldı!",
        _layout(body, "Yeni Dönem Bildirimi"),
    )
