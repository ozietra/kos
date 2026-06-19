from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, businesses, eligibility, nace, programs, applications, payments, admin, content
from app.services.seed import seed_programs, bootstrap_admin, seed_site_content, seed_pricing_plans, clear_legacy_seed_dates
from app.utils.migrations import run_lightweight_migrations
from app.database import AsyncSessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: tabloları oluştur + eksik kolonları ekle + seed
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await run_lightweight_migrations(conn)

    async with AsyncSessionLocal() as db:
        await seed_programs(db)
        await clear_legacy_seed_dates(db)
        await seed_site_content(db)
        await seed_pricing_plans(db)
        await bootstrap_admin(db)

    # KOSGEB program oto-güncelleme zamanlayıcısı
    from app.services.scheduler import start_scheduler, stop_scheduler
    start_scheduler()

    yield

    # Shutdown
    stop_scheduler()
    await engine.dispose()


app = FastAPI(
    title="kosgebhibe.com API",
    description="KOSGEB hibe başvuru hazırlık platformu",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(businesses.router)
app.include_router(eligibility.router)
app.include_router(nace.router)
app.include_router(programs.router)
app.include_router(applications.router)
app.include_router(payments.router)
app.include_router(admin.router)
app.include_router(content.router)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "kosgebhibe-api"}
