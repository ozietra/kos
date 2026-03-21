from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.schemas import NaceSuggestRequest, NaceSuggestResponse
from app.services.ai_generator import suggest_nace

router = APIRouter(prefix="/api/nace", tags=["nace"])

# ─── Statik NACE arama listesi (en sık kullanılanlar) ────────────────────────
NACE_LIST = [
    {"code": "10.01", "description": "Etin işlenmesi ve muhafazası"},
    {"code": "10.61", "description": "Hububat ürünleri imalatı"},
    {"code": "13.10", "description": "Tekstil elyafı hazırlama ve eğirme"},
    {"code": "14.13", "description": "İş giysileri imalatı"},
    {"code": "16.10", "description": "Kereste ve parke imalatı"},
    {"code": "20.41", "description": "Sabun ve deterjan imalatı"},
    {"code": "22.19", "description": "Diğer kauçuk ürünleri imalatı"},
    {"code": "23.61", "description": "Beton yapı elemanları imalatı"},
    {"code": "24.10", "description": "Ham demir ve çelik imalatı"},
    {"code": "25.11", "description": "Metal yapı ve yapı bileşenleri imalatı"},
    {"code": "26.20", "description": "Bilgisayar ve çevre birimlerinin imalatı"},
    {"code": "28.41", "description": "Metal işleme makineleri imalatı"},
    {"code": "31.01", "description": "Büro ve mağaza mobilyaları imalatı"},
    {"code": "32.50", "description": "Tıbbi ve dişçilik aletleri imalatı"},
    {"code": "61.10", "description": "Kablolu telekomünikasyon faaliyetleri"},
    {"code": "62.01", "description": "Bilgisayar programlama faaliyetleri"},
    {"code": "62.02", "description": "Bilgisayar danışmanlık faaliyetleri"},
    {"code": "62.09", "description": "Diğer bilgi teknolojisi ve bilgisayar hizmetleri"},
    {"code": "63.11", "description": "Veri işleme ve barındırma faaliyetleri"},
    {"code": "72.11", "description": "Biyoteknoloji alanında araştırma ve geliştirme"},
    {"code": "72.19", "description": "Diğer doğal bilimler alanında araştırma ve geliştirme"},
]


@router.post("/suggest", response_model=NaceSuggestResponse)
async def nace_suggest(data: NaceSuggestRequest):
    result = await suggest_nace(data.description)
    alt_codes = []
    for c in result.get("alternative_codes", []):
        if isinstance(c, str):
            alt_codes.append({"code": c, "description": "Alternatif Öneri"})
        elif isinstance(c, dict) and "code" in c:
            alt_codes.append(c)

    return NaceSuggestResponse(
        nace_code=str(result.get("nace_code", "")),
        nace_description=str(result.get("nace_description", "")),
        is_kosgeb_eligible=bool(result.get("is_kosgeb_eligible", False)),
        confidence=str(result.get("confidence", "low")),
        alternative_codes=alt_codes,
    )


@router.get("/search")
async def nace_search(q: str = Query("", min_length=1)):
    """NACE kodu metin arama (statik liste üzerinden)"""
    q_lower = q.lower()
    results = [
        n for n in NACE_LIST
        if q_lower in n["code"].lower() or q_lower in n["description"].lower()
    ]
    return results[:10]
