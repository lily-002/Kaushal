from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.orm import Blog

router = APIRouter()


def _serialize(blog: Blog) -> dict:
    return {
        "id": blog.id,
        "slug": blog.slug,
        "title": blog.title,
        "excerpt": blog.excerpt,
        "author": blog.author,
        "date": blog.date,
        "readTime": blog.read_time,
        "category": blog.category,
        "image": blog.image,
        "content": blog.content,
    }


@router.get("/blogs")
async def get_all_blogs(db: AsyncSession = Depends(get_db)):
    """Get all blog posts"""
    try:
        result = await db.execute(select(Blog).order_by(Blog.id.desc()))
        blogs = result.scalars().all()
        return {"success": True, "blogs": [_serialize(b) for b in blogs]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blogs/{slug}")
async def get_blog_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    """Get a single blog post by slug"""
    try:
        result = await db.execute(select(Blog).where(Blog.slug == slug))
        blog = result.scalar_one_or_none()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog post not found")
        return {"success": True, "blog": _serialize(blog)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blogs/category/{category}")
async def get_blogs_by_category(category: str, db: AsyncSession = Depends(get_db)):
    """Get blog posts by category"""
    try:
        stmt = select(Blog).order_by(Blog.id.desc())
        if category.lower() != "all":
            stmt = stmt.where(Blog.category == category)
        result = await db.execute(stmt)
        blogs = result.scalars().all()
        return {"success": True, "blogs": [_serialize(b) for b in blogs]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/blogs/related/{slug}")
async def get_related_blogs(slug: str, limit: int = 3, db: AsyncSession = Depends(get_db)):
    """Get related blog posts (excluding current one)"""
    try:
        result = await db.execute(
            select(Blog).where(Blog.slug != slug).limit(limit)
        )
        blogs = result.scalars().all()
        return {"success": True, "blogs": [_serialize(b) for b in blogs]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
