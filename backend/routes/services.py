from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import Service

router = APIRouter()


def _serialize(service: Service) -> dict:
    return {
        "id": service.id,
        "title": service.title,
        "subtitle": service.subtitle,
        "description": service.description,
        "icon": service.icon,
        "videoUrl": service.video_url,
        "fullDescription": service.full_description,
    }


@router.get("/services")
async def get_all_services(db: AsyncSession = Depends(get_db)):
    """Get all services"""
    try:
        result = await db.execute(select(Service).order_by(Service.id))
        services = result.scalars().all()
        return {"success": True, "services": [_serialize(s) for s in services]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/services/{service_id}")
async def get_service_by_id(service_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single service by ID"""
    try:
        result = await db.execute(select(Service).where(Service.id == service_id))
        service = result.scalar_one_or_none()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        return {"success": True, "service": _serialize(service)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
