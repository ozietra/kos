"""
WeasyPrint ile PDF üretimi
"""
import os
import uuid
from datetime import datetime

try:
    from weasyprint import HTML as WeasyHTML
    WEASYPRINT_AVAILABLE = True
except OSError:
    # Windows geliştirme ortamında WeasyPrint libgobject gerektirir.
    # Production'da Docker (Linux) üzerinde çalışır.
    WEASYPRINT_AVAILABLE = False
    WeasyHTML = None

from jinja2 import Environment
from app.models import Application


PDF_DIR = "/app/pdfs"

PDF_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600&display=swap');
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Source Sans 3', Arial, sans-serif; font-size: 13px; color: #1A1A18; line-height: 1.7; background: #fff; }
  .page { padding: 40px 50px; max-width: 800px; margin: auto; }
  .header { border-bottom: 3px solid #C0392B; padding-bottom: 16px; margin-bottom: 28px; }
  .header-title { font-size: 22px; font-weight: 700; color: #003366; }
  .header-sub { font-size: 13px; color: #6B6A62; margin-top: 4px; }
  .meta-box { background: #F4F3EE; border-left: 4px solid #C0392B; padding: 12px 16px; margin-bottom: 24px; border-radius: 4px; }
  .meta-row { display: flex; gap: 16px; flex-wrap: wrap; }
  .meta-item { font-size: 12px; color: #6B6A62; }
  .meta-item strong { color: #1A1A18; }
  h2 { font-size: 15px; font-weight: 700; color: #003366; margin: 28px 0 10px; border-bottom: 1px solid #E4E3DC; padding-bottom: 6px; }
  p { margin-bottom: 12px; }
  .section { margin-bottom: 24px; }
  .amount { font-family: monospace; font-size: 20px; font-weight: 700; color: #1E8449; }
  .doc-list { margin: 0; padding-left: 0; list-style: none; }
  .doc-item { padding: 8px 12px; border: 1px solid #E4E3DC; border-radius: 4px; margin-bottom: 6px; background: #fff; }
  .doc-item .doc-name { font-weight: 600; font-size: 13px; }
  .doc-item .doc-where { font-size: 11px; color: #6B6A62; margin-top: 2px; }
  .doc-item .doc-note { font-size: 11px; color: #A8A79F; }
  .warning { background: #FEF9E7; border-left: 4px solid #D68910; padding: 10px 14px; border-radius: 4px; font-size: 12px; margin-bottom: 10px; }
  .footer { margin-top: 40px; padding-top: 16px; border-top: 1px solid #E4E3DC; font-size: 10px; color: #A8A79F; text-align: center; }
  @page { size: A4; margin: 0; }
</style>
</head>
<body>
<div class="page">
  <div class="header">
    <div class="header-title">KOSGEB Başvuru Dosyası</div>
    <div class="header-sub">kosgebhibe.com tarafından hazırlanmıştır — {{ prepared_date }}</div>
  </div>

  <div class="meta-box">
    <div class="meta-row">
      <div class="meta-item"><strong>İşletme:</strong> {{ business_name }}</div>
      <div class="meta-item"><strong>Program:</strong> {{ program_type }}</div>
      {% if requested_amount %}
      <div class="meta-item"><strong>Talep:</strong> {{ requested_amount | format_currency }}</div>
      {% endif %}
    </div>
  </div>

  {% if project_summary %}
  <div class="section">
    <h2>Proje Özeti</h2>
    {{ project_summary | paragraphs }}
  </div>
  {% endif %}

  {% if business_plan %}
  <div class="section">
    <h2>İş Planı</h2>
    {{ business_plan | paragraphs }}
  </div>
  {% endif %}

  {% if financial_projection %}
  <div class="section">
    <h2>Finansal Projeksiyon Gerekçesi</h2>
    {{ financial_projection | paragraphs }}
  </div>
  {% endif %}

  {% if timeline %}
  <div class="section">
    <h2>Proje Takvimi</h2>
    {{ timeline | paragraphs }}
  </div>
  {% endif %}

  {% if documents %}
  <div class="section">
    <h2>Belge Kontrol Listesi</h2>
    <ul class="doc-list">
      {% for doc in documents %}
      <li class="doc-item">
        <div class="doc-name">☐ {{ doc.name }}</div>
        <div class="doc-where">Nereden alınır: {{ doc.where_to_get }}</div>
        {% if doc.description %}
        <div class="doc-note">{{ doc.description }}</div>
        {% endif %}
      </li>
      {% endfor %}
    </ul>
  </div>
  {% endif %}

  <div class="warning">
    Bu belge bilgilendirme ve hazırlık amaçlıdır. Güncel program şartları için kosgeb.gov.tr ziyaret ediniz.
    Onay garantisi verilmez. Başvuruyu e-Devlet üzerinden siz gönderirsiniz.
  </div>

  <div class="footer">
    kosgebhibe.com — Hazırlık tarihi: {{ prepared_date }} &nbsp;|&nbsp; Bu belgede yer alan metinler girdiğiniz bilgilere göre oluşturulmuştur.
  </div>
</div>
</body>
</html>
"""


def _format_currency(value):
    try:
        return f"{int(value):,} ₺".replace(",", ".")
    except Exception:
        return str(value)


def _paragraphs(text: str) -> str:
    if not text:
        return ""
    from markupsafe import Markup, escape
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    return Markup("".join(f"<p>{escape(p)}</p>" for p in paragraphs))


def _render_html(context: dict) -> str:
    from jinja2 import Environment
    env = Environment()
    env.filters["format_currency"] = _format_currency
    env.filters["paragraphs"] = _paragraphs
    template = env.from_string(PDF_HTML_TEMPLATE)
    return template.render(**context)


async def generate_pdf(application: Application, business_name: str, documents: list[dict]) -> str:
    """
    WeasyPrint ile PDF üret, dosyayı kaydet ve URL dön.
    """
    os.makedirs(PDF_DIR, exist_ok=True)

    context = {
        "business_name": business_name,
        "program_type": application.program_type or "İş Geliştirme Desteği",
        "requested_amount": None,
        "project_summary": application.project_summary,
        "business_plan": application.business_plan,
        "financial_projection": application.financial_projection,
        "timeline": application.timeline,
        "documents": documents,
        "prepared_date": datetime.now().strftime("%d/%m/%Y"),
    }

    # Budget breakdown'dan toplam tutarı çek
    if application.budget_breakdown:
        try:
            context["requested_amount"] = application.budget_breakdown.get("total_amount")
        except Exception:
            pass

    html_content = _render_html(context)

    file_name = f"{application.id}.pdf"
    file_path = os.path.join(PDF_DIR, file_name)

    if WEASYPRINT_AVAILABLE and WeasyHTML:
        WeasyHTML(string=html_content, base_url="").write_pdf(file_path)
    else:
        # Windows dev ortamı: HTML içeriğini .html olarak kaydet (debug için)
        html_path = file_path.replace(".pdf", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    return f"/api/applications/{application.id}/pdf"
