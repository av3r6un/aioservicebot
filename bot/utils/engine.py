from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from bot.models.base import Base
import os

engine = create_async_engine(os.getenv('DB_URL'), echo=False) # connect_args=dict(connect_timeout=30), pool_recycle=280, pool_pre_ping=True
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

