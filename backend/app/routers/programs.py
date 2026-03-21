from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import KosgebProgram
from app.schemas import ProgramResponse

router = APIRouter(prefix="/api/programs", tags=["programs"])


@router.get("", response_model=list[ProgramResponse])
async def list_programs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(KosgebProgram).where(KosgebProgram.is_active == True).order_by(KosgebProgram.program_name)
    )
    return result.scalars().all()


@router.get("/{program_id}", response_model=ProgramResponse)
async def get_program(program_id: str, db: AsyncSession = Depends(get_db)):
    from fastapi import HTTPException, status
    import uuid
    result = await db.execute(
        select(KosgebProgram).where(KosgebProgram.id == uuid.UUID(program_id))
    )
    program = result.scalar_one_or_none()
    if not program:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Program bulunamadı.")
    return program
