from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import Package

router = APIRouter()


def _serialize(package: Package) -> dict:
    return {
        "id": package.id,
        "name": package.name,
        "subtitle": package.subtitle,
        "sessions": package.sessions,
        "price": package.price,
        "description": package.description,
        "ideal": package.ideal,
        "features": package.features,
        "popular": package.popular,
    }


@router.get("/packages")
async def get_all_packages(db: AsyncSession = Depends(get_db)):
    """Get all packages"""
    try:
        result = await db.execute(select(Package).order_by(Package.id))
        packages = result.scalars().all()
        return {"success": True, "packages": [_serialize(p) for p in packages]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/packages/{package_id}")
async def get_package_by_id(package_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single package by ID"""
    try:
        result = await db.execute(select(Package).where(Package.id == package_id))
        package = result.scalar_one_or_none()
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")
        return {"success": True, "package": _serialize(package)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
