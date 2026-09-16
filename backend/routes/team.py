from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import TeamMember

router = APIRouter()


@router.get("/team")
async def get_team_members(db: AsyncSession = Depends(get_db)):
    """Get all team members"""
    try:
        result = await db.execute(select(TeamMember).order_by(TeamMember.id))
        team = result.scalars().all()
        return {
            "success": True,
            "team": [
                {"id": t.id, "name": t.name, "role": t.role, "description": t.description, "image": t.image}
                for t in team
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
