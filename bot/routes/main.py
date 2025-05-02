from bot.utils import create_config, assign_next_ip
from aiogram.types import Message, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters import Command
from bot.models import BotUser
from aiogram import Router, F

main = Router()


@main.message(Command('start'))
async def welcome(m: Message, session: AsyncSession):
  from bot import messages
  try:
    lang = m.from_user.language_code
    messages.lang = lang
    message = messages['welcome']
    users = await BotUser.get_column_values(session, 'id')
    if m.from_user.id not in users:
      uid = await BotUser.create_uid(session)
      user = BotUser(uid, m.from_user.id, lang, m.from_user.is_premium, m.from_user.first_name, m.from_user.last_name, m.from_user.username)
      await user.save(session)
    await m.answer(**message.m)
  except Exception as e:
    raise e


@main.message(Command('conf'))
async def new_handler(m: Message, session: AsyncSession):
  from bot import messages
  try:
    messages.lang = m.from_user.language_code
    message = messages['successfully_created']
    user = await BotUser.get_one(session, id=m.from_user.id)
    if not user.assigned_addr:
      addresses = await BotUser.get_column_values(session, 'assigned_addr')
      ip = assign_next_ip(addresses)
      created, config, qr = create_config(ip, f'u{m.from_user.id}')
      await user.update(session, assigned_addr=ip, config=config)
    else:
      config = user.config
    if created:
      await m.answer_photo(FSInputFile(qr, 'wg_connection.png'), **message.c)
    else:
      await m.answer(**messages['not_created'].m)
  except Exception as e:
    raise e

# @main.message(F)
# async def effect_handler(m: Message):
#   effect_id = m.effect_id
#   print(effect_id)
#   return await m.answer(text=m.text, message_effect_id=effect_id)
