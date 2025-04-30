from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from .utils import DatabaseMiddleware, Messages
from dotenv import load_dotenv, find_dotenv
from aiogram import Dispatcher, Bot
from .config import Settings
from .routes import routers
from aiohttp import web
import asyncio
import sys

load_dotenv('config/.env')
settings = Settings()
messages = Messages(settings.MESSAGE_PATH)

async def on_startup(bot: Bot) -> None:
  from .utils.engine import create_db
  await bot.delete_webhook(drop_pending_updates=True)
  if sys.platform == 'linux':
    await bot.set_webhook(f'{settings.BASE_WH_URL}{settings.WH_PATH}', drop_pending_updates=True)
  await create_db()
  await bot.set_my_commands(commands=settings.COMMANDS)


class PlatformHandler:
  def win32(self, dp: Dispatcher):
    asyncio.run(dp.start_polling(bot))

  def linux(self, dp: Dispatcher):
    app = web.Application()
    webhook_req_handler = SimpleRequestHandler(dp, bot)
    webhook_req_handler.register(app, path=settings.WH_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=settings.WS_HOST, port=settings.WS_PORT)

def start():
  from .utils.engine import session_maker
  dp = Dispatcher()
  dp.update.middleware(DatabaseMiddleware(session=session_maker))
  dp.include_routers(*routers)
  dp.startup.register(on_startup)
  global bot
  bot = Bot(settings.TOKEN)

  getattr(PlatformHandler(), sys.platform)(dp)
