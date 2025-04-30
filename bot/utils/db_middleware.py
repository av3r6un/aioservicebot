from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import Callable, Dict, Awaitable, Any
from aiogram.types import TelegramObject
from aiogram import BaseMiddleware


class DatabaseMiddleware(BaseMiddleware):
  def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
    self.session = session

  async def __call__(
      self,
      handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
      event: TelegramObject,
      data: dict[str, Any]
  ) -> Any:
    async with self.session() as session:
      try:
        data['session'] = session
        response = await handler(event, data)
        await session.commit()
        return response
      except Exception as ex:
        await session.rollback()
        raise
