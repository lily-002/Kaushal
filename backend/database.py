import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')


def build_database_url(driver: str = 'asyncpg') -> str:
    """Build a SQLAlchemy connection URL.

    Uses DATABASE_URL directly if set, otherwise assembles it from the
    separate DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME variables
    (password is percent-encoded since it may contain URL-special characters).
    """
    if os.environ.get('DATABASE_URL'):
        return os.environ['DATABASE_URL']

    user = os.environ['DB_USER']
    password = quote_plus(os.environ['DB_PASSWORD'])
    host = os.environ['DB_HOST']
    port = os.environ['DB_PORT']
    name = os.environ['DB_NAME']
    return f'postgresql+{driver}://{user}:{password}@{host}:{port}/{name}'


DATABASE_URL = build_database_url()

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
