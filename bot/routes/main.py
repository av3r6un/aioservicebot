from aiogram.types import Message, FSInputFile, CallbackQuery
from bot.utils import create_config, assign_next_ip, make_zip
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models import BotUser, Address
from bot.keyboards import QRRequest
from aiogram.filters import Command
from aiogram import Router, F
import os

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
    user = await BotUser.first(session, id=m.from_user.id)
    user_address = await Address.first(session, uuid=user.uid)
    if not user_address:
      addresses = await Address.get_column_values(session, 'assigned')
      ip = assign_next_ip(addresses)
      created, config = create_config(ip, f'u{m.from_user.id}')
      if created:
        addr_uid = await Address.create_uid(session)
        addr = Address(addr_uid, user.uid, ip, config)
        try:
          path = make_zip(config)
        except FileNotFoundError:
          return await m.answer(**messages['not_created'].m)
        im = await m.answer_document(FSInputFile(path), reply_markup=qrr.kb, **message.c)
        qrr.add_instance(m.chat.id, im, m, None)
        await addr.save(session)
      else:
        await m.answer(**messages['not_created'].m)
    else:
      im = await m.answer_document(FSInputFile(f'{user_address.config}/wg_connection.zip'), reply_markup=qrr.kb, **message.c)
      qrr.add_instance(m.chat.id, im, m, None)
  except Exception as e:
    raise e

@main.callback_query(qrr.filter)
async def qr_handler(q: CallbackQuery, session: AsyncSession):
  from bot import messages
  messages.lang = q.from_user.language_code
  message = messages['your_png']
  action = qrr.extract_action(q.data)
  try:
    if action == 'showQR':
      user = await BotUser.first(session, id=q.from_user.id)
      address = await Address.first(session, uuid=user.uid)
      qr_path = f'{user.config}/u{q.from_user.id}.png'
      await q.message.answer_photo(FSInputFile(qr_path, 'wg_qr.png'), **message.c)
      await qrr.service_messages[q.from_user.id].delete_reply_markup()
      qrr.service_messages.pop(q.from_user.id)
  except Exception as e:
    raise e
