from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import auth, businesses, eligibility, nace, programs, applications, payments
from app.services.seed import seed_programs
from app.database import AsyncSessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: tabloları oluştur + seed
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        await seed_programs(db)

    yield

    # Shutdown
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


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "kosgebhibe-api"}
