"""
Site içeriği servisi: ana sayfa hero rozeti ve istatistikleri DB'den türetir.
Hero rozeti, admin override boşsa programlardaki en yakın başvuru son tarihinden
otomatik üretilir — böylece "30 Nisan" gibi sabit tarihler güncel kalır.
"""
from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import KosgebProgram, SiteContent

_TR_MONTHS = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
              "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]


def _tr_date(d: date) -> str:
    return f"{d.day} {_TR_MONTHS[d.month]} {d.year}"


async def get_next_deadline_badge(db: AsyncSession) -> str:
    """Aktif programlar içinde bugünden sonraki en yakın son başvuru tarihi."""
    today = date.today()
    result = await db.execute(
        select(KosgebProgram).where(KosgebProgram.is_active == True)
    )
    programs = result.scalars().all()

    candidates = []
    for p in programs:
        deadline = p.application_period_end or p.application_period_start
        if deadline and deadline >= today:
            candidates.append((deadline, p.program_name))

    year = today.year
    if not candidates:
        return f"{year} Güncel • Başvuru dönemleri için takvimi inceleyin"

    candidates.sort(key=lambda x: x[0])
    deadline, name = candidates[0]
    short = name.split("—")[0].strip()
    if len(short) > 40:
        short = short[:40].rstrip() + "…"
    return f"{year} Güncel • {short} son başvuru: {_tr_date(deadline)}"


async def get_home_content(db: AsyncSession) -> dict:
    """Ana sayfa için hero rozeti + istatistikler."""
    # Hero rozeti: override varsa onu, yoksa türetilmiş tarihi kullan
    override_res = await db.execute(
        select(SiteContent).where(SiteContent.key == "hero_badge_override")
    )
    override = override_res.scalar_one_or_none()
    if override and (override.value or "").strip():
        hero_badge = override.value.strip()
    else:
        hero_badge = await get_next_deadline_badge(db)

    stats_res = await db.execute(
        select(SiteContent).where(SiteContent.group == "stats").order_by(SiteContent.sort_order)
    )
    stats = [
        {"key": s.key, "label": s.label, "value": s.value}
        for s in stats_res.scalars().all()
    ]

    return {"hero_badge": hero_badge, "stats": stats}
