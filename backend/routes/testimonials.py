from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import Testimonial

router = APIRouter()


@router.get("/testimonials")
async def get_testimonials(db: AsyncSession = Depends(get_db)):
    """Get all testimonials"""
    try:
        result = await db.execute(select(Testimonial).order_by(Testimonial.id))
        testimonials = result.scalars().all()
        return {
            "success": True,
            "testimonials": [
                {
                    "id": t.id,
                    "name": t.name,
                    "role": t.role,
                    "content": t.content,
                    "rating": t.rating,
                    "image": t.image,
                }
                for t in testimonials
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
