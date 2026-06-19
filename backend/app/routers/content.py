"""
Public içerik uçları — frontend'in ana sayfa & fiyatlandırmayı dinamik
çekmesi için. Kimlik doğrulama gerektirmez.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.site_content import get_home_content, get_seo_settings
from app.services.pricing import get_active_plans

router = APIRouter(prefix="/api/content", tags=["content"])


@router.get("/home")
async def home_content(db: AsyncSession = Depends(get_db)):
    return await get_home_content(db)


@router.get("/seo")
async def seo_content(db: AsyncSession = Depends(get_db)):
    """Public: Google Analytics ID + Search Console doğrulama kodu (site head'i için)."""
    return await get_seo_settings(db)


@router.get("/pricing")
async def pricing_content(db: AsyncSession = Depends(get_db)):
    return {"plans": await get_active_plans(db)}
