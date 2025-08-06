from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, inspect, or_
from sqlalchemy import DateTime, func
import secrets
import string

class Base(DeclarativeBase):
  created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
  updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    
  @property
  def created_ts(self):
    return int(self.created.timestamp())

  @classmethod
  async def create_uid(cls, session: AsyncSession):
    existing = await session.execute(select(cls.uid))
    uids = set(existing.scalars().all())
    alp = string.ascii_letters + string.digits
    while True:
      uid = ''.join(secrets.choice(alp) for _ in range(cls.__table__.c.uid.type.length))
      if uid not in uids:
        return uid
      
  @classmethod
  async def get(cls, session: AsyncSession, **filters):
    query = select(cls)
    for rel in inspect(cls).relationships:
      query = query.options(selectinload(getattr(cls, rel.key)))
    query = query.filter_by(**filters)
    result = await session.execute(query)
    return result.scalars().all()
  
  @classmethod
  async def first(cls, session: AsyncSession, **filters):
    query = select(cls)
    for rel in inspect(cls).relationships:
      query = query.options(selectinload(getattr(cls, rel.key)))
    query = query.filter_by(**filters)
    result = await session.execute(query)
    return result.scalars().one_or_none()
  
  @classmethod
  async def get_column_values(cls, session: AsyncSession, column_name):
    query = await session.execute(select(getattr(cls, column_name)))
    values = set(query.scalars().all())
    return values  

  @classmethod
  async def get_json(cls, session: AsyncSession, **filters):
    all = await cls.get(session, **filters)
    return [a.json for a in all]
  
  @classmethod
  async def update(cls, seasion: AsyncSession, key, **kwargs):
    pk_column = cls.__mapper__.primary_key[0].name
    query = update(cls).where(getattr(cls, pk_column) == key).values(**kwargs).execution_options(synchronize_session='fetch')
    await seasion.execute(query)
    await seasion.commit()
    return True
  
  async def update(self, session: AsyncSession, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)
    await session.commit()
    return True

  async def save(self, session: AsyncSession):
    self.updated = func.now()
    session.add(self)
    await session.commit()
