"""
WeasyPrint ile profesyonel, markasız KOSGEB başvuru dosyası üretimi.

Çıktı, bir danışmanın KOBİ için hazırladığı resmi başvuru dosyası kalitesindedir:
kapak sayfası, numaralı bölümler, sayfa numaraları, nötr kurumsal tipografi.
Hiçbir marka / logo / platform adı içermez.
"""
import os
import re
import html as html_lib
from datetime import datetime

try:
    from weasyprint import HTML as WeasyHTML
    WEASYPRINT_AVAILABLE = True
except OSError:
    # Windows geliştirme ortamında WeasyPrint GTK kütüphaneleri gerektirir.
    # Production'da Docker (Linux) üzerinde sorunsuz çalışır.
    WEASYPRINT_AVAILABLE = False
    WeasyHTML = None

from app.models import Application


# Docker'da /app/pdfs; lokalde PDF_DIR env'i ile override edilebilir
PDF_DIR = os.getenv("PDF_DIR", "/app/pdfs")

# Türkçe ay adları
_TR_MONTHS = [
    "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık",
]


def _tr_date(d: datetime) -> str:
    return f"{d.day} {_TR_MONTHS[d.month]} {d.year}"


def _format_currency(value) -> str:
    try:
        return f"{int(value):,} ₺".replace(",", ".")
    except Exception:
        return str(value)


# ─── Markdown → HTML mini dönüştürücü ────────────────────────────────────────
# AI çıktısı "## Başlık", "**kalın**", "- madde" üretir. Bunları gerçek HTML'e
# çevirir (aksi halde düz <p> olarak basılıyordu).

def _inline(text: str) -> str:
    """Satır içi: önce kaçış, sonra **kalın** ve *italik*."""
    text = html_lib.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    return text


def _markdown_to_html(text: str) -> str:
    if not text:
        return ""
    lines = text.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    para: list[str] = []

    def flush_para():
        if para:
            out.append(f"<p>{_inline(' '.join(para))}</p>")
            para.clear()

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_para()
            close_list()
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush_para()
            close_list()
            level = min(len(m.group(1)), 4)
            tag = "h3" if level <= 2 else "h4"  # bölüm başlıkları zaten h2; iç başlıklar h3/h4
            out.append(f"<{tag}>{_inline(m.group(2))}</{tag}>")
            continue
        if re.match(r"^[-*•]\s+", line):
            flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline(re.sub(r'^[-*•]\s+', '', line))}</li>")
            continue
        # numaralı liste maddesi → paragraf gibi ama satır kırılmasın
        para.append(line)

    flush_para()
    close_list()
    return "".join(out)


# ─── HTML şablonu ────────────────────────────────────────────────────────────

def _build_html(ctx: dict) -> str:
    sections: list[str] = []
    n = 0

    def add_section(title: str, body_html: str):
        nonlocal n
        if not body_html:
            return
        n += 1
        sections.append(
            f'<section class="section"><h2><span class="sec-no">{n}.</span> {html_lib.escape(title)}</h2>{body_html}</section>'
        )

    add_section("Yönetici Özeti", _markdown_to_html(ctx.get("project_summary")))
    add_section("İş Planı", _markdown_to_html(ctx.get("business_plan")))
    add_section("Finansal Projeksiyon", _markdown_to_html(ctx.get("financial_projection")))
    add_section("Proje Takvimi", _markdown_to_html(ctx.get("timeline")))

    # Bütçe tablosu (budget_breakdown JSON'undan)
    budget = ctx.get("budget_breakdown") or {}
    items = budget.get("items") if isinstance(budget, dict) else None
    if items and isinstance(items, list):
        rows = ""
        for it in items:
            name = html_lib.escape(str(it.get("name", "")))
            amount = _format_currency(it.get("amount", 0))
            rows += f"<tr><td>{name}</td><td class='num'>{amount}</td></tr>"
        total = budget.get("total_amount")
        if total is not None:
            rows += f"<tr class='total'><td>Toplam</td><td class='num'>{_format_currency(total)}</td></tr>"
        n += 1
        sections.append(
            f'<section class="section"><h2><span class="sec-no">{n}.</span> Bütçe Tablosu</h2>'
            f'<table class="budget"><thead><tr><th>Gider Kalemi</th><th class="num">Tutar</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></section>'
        )

    # NOT: "Gerekli Belgeler" kontrol listesi başvuru dosyasından kaldırıldı
    # (kullanıcı talebi). Belge listesi artık PDF'e basılmaz.

    sections_html = "".join(sections)

    meta_rows = ""
    for label, value in [
        ("İşletme Ünvanı", ctx.get("business_name")),
        ("Faaliyet Kodu (NACE)", _nace_line(ctx)),
        ("Şehir", ctx.get("city")),
        ("Başvurulan Program", ctx.get("program_type")),
        ("Talep Edilen Destek", _format_currency(ctx["requested_amount"]) if ctx.get("requested_amount") else None),
    ]:
        if value:
            meta_rows += f'<div class="cover-row"><span class="cover-label">{label}</span><span class="cover-value">{html_lib.escape(str(value))}</span></div>'

    project_title = ctx.get("project_title") or ctx.get("program_type") or "KOSGEB Destek Başvurusu"

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600;700&family=Source+Sans+3:wght@400;600&display=swap');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html {{ font-size: 11pt; }}
  body {{ font-family: 'Source Sans 3', 'Segoe UI', Arial, sans-serif; color: #1a1a1a; line-height: 1.65; }}

  @page {{
    size: A4;
    margin: 22mm 20mm 20mm 20mm;
    @bottom-center {{
      content: "{html_lib.escape(str(project_title))}";
      font-family: 'Source Sans 3', sans-serif; font-size: 8pt; color: #8a8a8a;
    }}
    @bottom-right {{
      content: "Sayfa " counter(page) " / " counter(pages);
      font-family: 'Source Sans 3', sans-serif; font-size: 8pt; color: #8a8a8a;
    }}
  }}
  @page :first {{
    margin: 0;
    @bottom-center {{ content: none; }}
    @bottom-right {{ content: none; }}
  }}

  /* ── Kapak ── */
  .cover {{ height: 297mm; padding: 45mm 28mm; display: flex; flex-direction: column; page-break-after: always; }}
  .cover-kicker {{ font-size: 10pt; letter-spacing: 3px; text-transform: uppercase; color: #555; border-bottom: 2px solid #1a1a1a; padding-bottom: 10px; }}
  .cover-title {{ font-family: 'Source Serif 4', Georgia, serif; font-size: 30pt; font-weight: 700; line-height: 1.2; margin-top: 60mm; color: #111; }}
  .cover-subtitle {{ font-size: 13pt; color: #444; margin-top: 14px; }}
  .cover-meta {{ margin-top: auto; border-top: 1px solid #d8d8d8; padding-top: 18px; }}
  .cover-row {{ display: flex; padding: 5px 0; font-size: 10.5pt; }}
  .cover-label {{ width: 200px; color: #777; }}
  .cover-value {{ font-weight: 600; color: #1a1a1a; }}
  .cover-date {{ font-size: 10pt; color: #777; margin-top: 18px; }}

  /* ── İçerik ── */
  .content {{ padding: 0; }}
  h2 {{ font-family: 'Source Serif 4', Georgia, serif; font-size: 16pt; font-weight: 700; color: #111;
       margin: 26px 0 12px; padding-bottom: 7px; border-bottom: 1.5px solid #1a1a1a; }}
  h2 .sec-no {{ color: #777; font-weight: 600; }}
  h3 {{ font-size: 12.5pt; font-weight: 600; color: #1a1a1a; margin: 18px 0 7px; }}
  h4 {{ font-size: 11pt; font-weight: 600; color: #333; margin: 14px 0 6px; }}
  .section {{ margin-bottom: 14px; }}
  .section:not(:first-child) h2 {{ page-break-before: auto; }}
  p {{ margin-bottom: 10px; text-align: justify; }}
  ul {{ margin: 6px 0 12px 20px; }}
  li {{ margin-bottom: 5px; }}

  table.budget {{ width: 100%; border-collapse: collapse; margin: 10px 0 14px; font-size: 10.5pt; }}
  table.budget th {{ text-align: left; border-bottom: 2px solid #1a1a1a; padding: 8px 10px; }}
  table.budget td {{ border-bottom: 1px solid #e2e2e2; padding: 8px 10px; }}
  table.budget .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  table.budget tr.total td {{ font-weight: 700; border-top: 2px solid #1a1a1a; border-bottom: none; }}

  .doc-list {{ list-style: none; }}
  .doc-item {{ padding: 9px 12px; border: 1px solid #e2e2e2; border-radius: 3px; margin-bottom: 7px; }}
  .doc-name {{ font-weight: 600; }}
  .cb {{ display: inline-block; width: 11px; height: 11px; border: 1.3px solid #555; border-radius: 2px; margin-right: 8px; vertical-align: middle; }}
  .doc-where {{ font-size: 9.5pt; color: #666; margin-top: 2px; }}
  .doc-note {{ font-size: 9.5pt; color: #999; }}
</style>
</head>
<body>
  <div class="cover">
    <div class="cover-kicker">KOSGEB Destek Başvuru Dosyası</div>
    <div class="cover-title">{html_lib.escape(str(project_title))}</div>
    <div class="cover-subtitle">{html_lib.escape(str(ctx.get('business_name') or ''))}</div>
    <div class="cover-meta">
      {meta_rows}
      <div class="cover-date">Hazırlanma Tarihi: {ctx.get('prepared_date')}</div>
    </div>
  </div>
  <div class="content">
    {sections_html}
  </div>
</body>
</html>"""


def _nace_line(ctx: dict) -> str:
    code = (ctx.get("nace_code") or "").strip()
    desc = (ctx.get("nace_description") or "").strip()
    if code and desc:
        return f"{code} — {desc}"
    return code or desc or ""


async def generate_pdf(
    application: Application,
    business_name: str,
    documents: list[dict],
    meta: dict | None = None,
) -> str:
    """
    Profesyonel, markasız PDF üret, dosyayı kaydet ve indirme URL'i dön.
    `meta`: kapak için ek bilgi (nace_code, nace_description, city, project_title).
    """
    os.makedirs(PDF_DIR, exist_ok=True)
    meta = meta or {}

    ctx = {
        "business_name": business_name or meta.get("business_name"),
        "program_type": application.program_type or "KOSGEB Destek Programı",
        "project_title": application.project_title or meta.get("project_title"),
        "nace_code": meta.get("nace_code"),
        "nace_description": meta.get("nace_description"),
        "city": meta.get("city"),
        "requested_amount": None,
        "project_summary": application.project_summary,
        "business_plan": application.business_plan,
        "financial_projection": application.financial_projection,
        "timeline": application.timeline,
        "budget_breakdown": application.budget_breakdown,
        "documents": documents,
        "prepared_date": _tr_date(datetime.now()),
    }

    if application.budget_breakdown:
        try:
            ctx["requested_amount"] = application.budget_breakdown.get("total_amount")
        except Exception:
            pass

    html_content = _build_html(ctx)

    file_path = os.path.join(PDF_DIR, f"{application.id}.pdf")

    if WEASYPRINT_AVAILABLE and WeasyHTML:
        WeasyHTML(string=html_content, base_url="").write_pdf(file_path)
    else:
        # Windows dev ortamı: PDF üretilemiyor, HTML olarak kaydet (debug)
        with open(file_path.replace(".pdf", ".html"), "w", encoding="utf-8") as f:
            f.write(html_content)

    return f"/api/applications/{application.id}/pdf"
