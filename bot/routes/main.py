from aiogram.types import Message, FSInputFile, CallbackQuery
from bot.utils import create_config, assign_next_ip
from sqlalchemy.ext.asyncio import AsyncSession
from bot.keyboards.qr_request import QRFilter
from bot.keyboards import QRRequest
from aiogram.filters import Command
from bot.models import BotUser
from aiogram import Router, F

main = Router()
qrr = QRRequest()

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
      created, config, path = create_config(ip, f'u{m.from_user.id}')
      await user.update(session, assigned_addr=ip, config=config)
      if created:
        im = await m.answer_document(FSInputFile(path), reply_markup=qrr.kb, **message.c)
        qrr.add_instance(m.chat.id, im, m, None)
      else:
        await m.answer(**messages['not_created'].m)
    else:
      im = await m.answer_document(FSInputFile(f'{user.config}/wg_connection.zip'), reply_markup=qrr.kb, **message.c)
      qrr.add_instance(m.chat.id, im, m, None)
  except Exception as e:
    raise e

@main.callback_query(qrr.filter)
async def qr_handler(q: CallbackQuery, session: AsyncSession):
  action = qrr.extract_action(q.data)
  try:
    if action == 'showQR':
      user = await BotUser.get_one(session, id=q.from_user.id)
      qr_path = f'{user.config}/u{q.from_user.id}.png'
      await q.message.answer_photo(FSInputFile(qr_path, 'wg_qr.png'))
      await qrr.service_messages[q.from_user.id].delete_reply_markup()
      qrr.service_messages.pop(q.from_user.id)
  except Exception as e:
    raise e
