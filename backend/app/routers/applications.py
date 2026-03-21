"""
Başvuru Router — AI üretim akışı + SSE streaming
"""
import uuid
import asyncio
import json
from datetime import datetime
from typing import AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db, get_redis
from app.models import Application, ApplicationInput, Business, User
from app.schemas import ApplicationCreate, ApplicationInputSubmit, ApplicationResponse, MessageResponse
from app.utils.deps import get_current_user
from app.services.ai_generator import (
    generate_project_summary, generate_business_plan_chunked,
    generate_financial_projection, generate_timeline,
    generate_document_checklist,
)
from app.services.pdf_service import generate_pdf, PDF_DIR
import os

router = APIRouter(prefix="/api/applications", tags=["applications"])


# ─── Yardımcı: SSE mesaj formatı ─────────────────────────────────────────────

def _sse_msg(data: dict) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


async def _update_progress(application_id: str, progress: int, text: str, db: AsyncSession):
    result = await db.execute(select(Application).where(Application.id == uuid.UUID(application_id)))
    app = result.scalar_one_or_none()
    if app:
        app.generation_progress = progress
        app.generation_status_text = text
        await db.commit()


# ─── CRUD ────────────────────────────────────────────────────────────────────

@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # İşletme sahipliği kontrolü
    biz = await db.execute(
        select(Business).where(Business.id == data.business_id, Business.user_id == current_user.id)
    )
    if not biz.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="İşletme bulunamadı.")

    application = Application(
        business_id=data.business_id,
        program_type=data.program_type,
        application_year=data.application_year or datetime.now().year,
        application_period=data.application_period,
        status="draft",
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)
    return application


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application)
        .join(Business)
        .where(Application.id == application_id, Business.user_id == current_user.id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı.")
    return app


@router.put("/{application_id}/inputs", response_model=MessageResponse)
async def save_inputs(
    application_id: uuid.UUID,
    data: ApplicationInputSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Yetki kontrolü
    result = await db.execute(
        select(Application).join(Business)
        .where(Application.id == application_id, Business.user_id == current_user.id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı.")

    # Mevcut input'ları güncelle veya ekle
    fields = data.model_dump(exclude_none=True)
    for field_name, field_value in fields.items():
        existing = await db.execute(
            select(ApplicationInput).where(
                ApplicationInput.application_id == application_id,
                ApplicationInput.field_name == field_name,
            )
        )
        inp = existing.scalar_one_or_none()
        if inp:
            inp.field_value = str(field_value)
        else:
            db.add(ApplicationInput(
                application_id=application_id,
                field_name=field_name,
                field_value=str(field_value),
            ))

    # Proje başlığını application'a da kaydet
    if data.project_title:
        app.project_title = data.project_title

    await db.commit()
    return {"message": "Bilgiler kaydedildi."}


# ─── ANA: Üretim endpoint'i (POST başlatır, GET SSE izler) ───────────────────

@router.post("/{application_id}/generate", response_model=MessageResponse)
async def start_generation(
    application_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Üretimi arka planda başlat (SSE ile takip et)"""
    result = await db.execute(
        select(Application).join(Business)
        .where(Application.id == application_id, Business.user_id == current_user.id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı.")

    if app.status == "generating":
        return {"message": "Üretim zaten devam ediyor."}

    app.status = "generating"
    app.generation_progress = 0
    await db.commit()

    return {"message": "Üretim başlatıldı. /progress endpoint'inden takip edebilirsiniz."}


@router.get("/{application_id}/progress")
async def stream_progress(
    application_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """SSE ile üretim ilerlemesini aktar ve metinleri üret"""

    result = await db.execute(
        select(Application).join(Business)
        .where(Application.id == application_id, Business.user_id == current_user.id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı.")

    # Input'ları topla
    inputs_result = await db.execute(
        select(ApplicationInput).where(ApplicationInput.application_id == application_id)
    )
    raw_inputs = inputs_result.scalars().all()
    inputs_dict = {inp.field_name: inp.field_value for inp in raw_inputs}

    # İşletme bilgilerini ekle
    biz_result = await db.execute(select(Business).where(Business.id == app.business_id))
    business = biz_result.scalar_one_or_none()
    if business:
        from datetime import date
        age_months = (
            (date.today().year - business.founding_date.year) * 12 +
            (date.today().month - business.founding_date.month)
        ) if business.founding_date else 0

        inputs_dict.update({
            "business_name": business.business_name,
            "nace_code": business.nace_code or "",
            "nace_description": business.nace_description or "",
            "city": business.city or "",
            "business_age_months": str(age_months),
            "special_category": ", ".join(filter(None, [
                "Kadın girişimci" if business.is_woman_entrepreneur else "",
                "Genç girişimci" if business.is_young_entrepreneur else "",
                "Engelli girişimci" if business.is_disabled else "",
                "Şehit/Gazi yakını" if business.is_veteran else "",
            ])) or "Standart",
        })

    async def event_stream() -> AsyncGenerator[str, None]:
        try:
            yield _sse_msg({"progress": 5, "text": "Hazırlanıyor..."})
            await asyncio.sleep(0.1)

            # 1. Proje özeti
            yield _sse_msg({"progress": 10, "text": "Proje özeti hazırlanıyor..."})
            summary = await generate_project_summary(inputs_dict)
            app.project_summary = summary
            await db.commit()
            yield _sse_msg({"progress": 30, "text": "Proje özeti tamamlandı.", "field": "project_summary", "value": summary})

            # 2. İş planı
            yield _sse_msg({"progress": 35, "text": "İş planı alt bölümlerine ayrılıyor..."})
            business_plan_parts = []
            chunk_progress = 35
            async for section_name, section_text in generate_business_plan_chunked(inputs_dict):
                chunk_progress += 7
                yield _sse_msg({"progress": chunk_progress, "text": f"'{section_name}' bölümü yazıldı ve kalite kontrolünden geçti..."})
                business_plan_parts.append(f"## {section_name}\n\n{section_text}")
            
            business_plan = "\n\n".join(business_plan_parts)
            app.business_plan = business_plan
            await db.commit()
            yield _sse_msg({"progress": 58, "text": "Kapsamlı İş Planı tamamlandı.", "field": "business_plan", "value": business_plan})

            # 3. Finansal projeksiyon
            yield _sse_msg({"progress": 60, "text": "Finansal tablo hazırlanıyor..."})
            financial = await generate_financial_projection(inputs_dict)
            app.financial_projection = financial
            await db.commit()
            yield _sse_msg({"progress": 72, "text": "Finansal projeksiyon tamamlandı.", "field": "financial_projection", "value": financial})

            # 4. Takvim
            yield _sse_msg({"progress": 75, "text": "Proje takvimi oluşturuluyor..."})
            timeline = await generate_timeline(inputs_dict)
            app.timeline = timeline
            await db.commit()
            yield _sse_msg({"progress": 85, "text": "Takvim tamamlandı.", "field": "timeline", "value": timeline})

            # 5. Belge listesi
            yield _sse_msg({"progress": 88, "text": "Belge listesi hazırlanıyor..."})
            docs = generate_document_checklist(app.program_type or "IGD")
            app.document_checklist = docs
            await db.commit()
            yield _sse_msg({"progress": 92, "text": "Belge listesi hazır."})

            # 6. PDF
            yield _sse_msg({"progress": 95, "text": "PDF hazırlanıyor..."})
            pdf_url = await generate_pdf(app, inputs_dict.get("business_name", ""), docs)
            app.pdf_url = pdf_url
            app.status = "completed"
            app.generation_progress = 100
            await db.commit()
            yield _sse_msg({"progress": 100, "text": "Hazır!", "pdf_url": pdf_url, "done": True})

        except Exception as e:
            app.status = "error"
            await db.commit()
            yield _sse_msg({"progress": 0, "text": f"Hata: {str(e)}", "error": True})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/{application_id}/pdf")
async def download_pdf(
    application_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application).join(Business)
        .where(Application.id == application_id, Business.user_id == current_user.id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı.")

    pdf_path = os.path.join(PDF_DIR, f"{application_id}.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PDF henüz oluşturulmamış.")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"kosgeb-basvurusu-{application_id}.pdf",
    )


@router.get("/{application_id}/documents")
async def get_documents(
    application_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Application).join(Business)
        .where(Application.id == application_id, Business.user_id == current_user.id)
    )
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Başvuru bulunamadı.")
    return app.document_checklist or []
