from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import Contact

router = APIRouter()


class ContactSubmission(BaseModel):
    name: str
    email: EmailStr
    phone: str
    message: str


@router.post("/contact")
async def submit_contact_form(submission: ContactSubmission, db: AsyncSession = Depends(get_db)):
    """Handle contact form submissions"""
    try:
        contact = Contact(**submission.dict())
        db.add(contact)
        await db.commit()

        return {
            "success": True,
            "message": "Thank you for contacting us! We'll get back to you soon."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/contacts")
async def get_all_contacts(db: AsyncSession = Depends(get_db)):
    """Get all contact submissions (admin use)"""
    try:
        result = await db.execute(select(Contact).order_by(Contact.submitted_at.desc()))
        contacts = result.scalars().all()
        return {
            "success": True,
            "contacts": [
                {
                    "name": c.name,
                    "email": c.email,
                    "phone": c.phone,
                    "message": c.message,
                    "status": c.status,
                    "submitted_at": c.submitted_at.isoformat(),
                }
                for c in contacts
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
