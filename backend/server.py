from fastapi import FastAPI, APIRouter, Depends
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import os
import logging
from pydantic import BaseModel
from typing import List

from database import engine, get_db
from models.orm import StatusCheck
from routes.blogs import router as blogs_router
from routes.services import router as services_router
from routes.packages import router as packages_router
from routes.team import router as team_router
from routes.testimonials import router as testimonials_router
from routes.faq import router as faq_router
from routes.contact import router as contact_router


# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheckCreate(BaseModel):
    client_name: str


class StatusCheckOut(BaseModel):
    id: str
    client_name: str
    timestamp: str


# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheckOut)
async def create_status_check(input: StatusCheckCreate, db: AsyncSession = Depends(get_db)):
    status_obj = StatusCheck(client_name=input.client_name)
    db.add(status_obj)
    await db.commit()
    await db.refresh(status_obj)
    return {
        "id": status_obj.id,
        "client_name": status_obj.client_name,
        "timestamp": status_obj.timestamp.isoformat(),
    }

@api_router.get("/status", response_model=List[StatusCheckOut])
async def get_status_checks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StatusCheck))
    checks = result.scalars().all()
    return [
        {"id": c.id, "client_name": c.client_name, "timestamp": c.timestamp.isoformat()}
        for c in checks
    ]

# Include all routes
api_router.include_router(blogs_router, tags=["blogs"])
api_router.include_router(services_router, tags=["services"])
api_router.include_router(packages_router, tags=["packages"])
api_router.include_router(team_router, tags=["team"])
api_router.include_router(testimonials_router, tags=["testimonials"])
api_router.include_router(faq_router, tags=["faq"])
api_router.include_router(contact_router, tags=["contact"])

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    await engine.dispose()
