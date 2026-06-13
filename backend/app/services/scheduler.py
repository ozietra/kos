"""
KOSGEB program oto-güncelleme zamanlayıcısı (in-process APScheduler).

Uygulama tek uzun-ömürlü container olduğundan, ayrı bir cron servisine gerek
yok. Zamanlanmış iş yalnızca ÖNERİ üretir (canlıya dokunmaz). Asıl/güvenilir
tetikleyici admin panelindeki "Şimdi Güncelle" butonudur; bu haftalık iş bir
emniyet ağıdır.
"""
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import settings
from app.database import AsyncSessionLocal

logger = logging.getLogger("kosgeb.scheduler")

_scheduler: AsyncIOScheduler | None = None


async def _scheduled_scrape():
    from app.services.program_scraper import run_scrape
    try:
        async with AsyncSessionLocal() as db:
            result = await run_scrape(db, triggered_by="schedule")
        logger.info("Zamanlanmış KOSGEB taraması bitti: %s", result)
    except Exception as e:  # zamanlayıcı hiçbir koşulda uygulamayı düşürmesin
        logger.exception("Zamanlanmış tarama hatası: %s", e)


def start_scheduler() -> None:
    global _scheduler
    if not settings.KOSGEB_SCRAPE_ENABLED:
        return
    if _scheduler is not None:
        return
    try:
        _scheduler = AsyncIOScheduler(timezone="Europe/Istanbul")
        _scheduler.add_job(
            _scheduled_scrape,
            CronTrigger(day_of_week=settings.KOSGEB_SCRAPE_CRON_DAY,
                        hour=settings.KOSGEB_SCRAPE_CRON_HOUR, minute=0),
            id="kosgeb_program_scrape",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
        _scheduler.start()
        logger.info("KOSGEB tarama zamanlayıcısı başlatıldı.")
    except Exception as e:
        logger.exception("Zamanlayıcı başlatılamadı: %s", e)
        _scheduler = None


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        try:
            _scheduler.shutdown(wait=False)
        except Exception:
            pass
        _scheduler = None
