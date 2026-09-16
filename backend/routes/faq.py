from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import FAQ

router = APIRouter()


@router.get("/faqs")
async def get_faqs(db: AsyncSession = Depends(get_db)):
    """Get all FAQs"""
    try:
        result = await db.execute(select(FAQ).order_by(FAQ.id))
        faqs = result.scalars().all()
        return {
            "success": True,
            "faqs": [{"id": f.id, "question": f.question, "answer": f.answer} for f in faqs],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
