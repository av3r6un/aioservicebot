from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from datetime import datetime as dt
from typing import List, Optional
from aiogram import F


class SimpleMessage:
  _text: str = None
  date: dt = None
  chat_id: int = None
  user_id: int = None
  username: str = None
  business_connection_id: int = None
  id: int = None

  def __init__(self, original: Message) -> None:
    self._text = original.text
    self.chat_id = original.chat.id
    self.user_id = original.from_user.id
    self.username = original.from_user.username
    self.business_connection_id = original.business_connection_id
    self.id = original.message_id
    
  @property
  def text(self):
    return self._text
  
  @text.setter
  def text(self, value):
    self._text = value
  
  @property
  def information(self):
    return f'<b>New complaint:</b>\n@{self.username} [{self.date.strftime("%d.%m.%Y %H:%M:%S")}]: {self.text}'


class ReceivedMessage:
  chat_id: int = None
  message: SimpleMessage = None

  def __init__(self, chat_id, message: Message, **kwargs) -> None:
    self.chat_id = chat_id
    self.message = SimpleMessage(message)
  

class ReceivedMessages(List[ReceivedMessage]):
  def __init__(self, *args):
    for arg in args:
      self.append(ReceivedMessage(*arg))
    
  def add(self, chat_id, message) -> None:
    self.append(ReceivedMessage(chat_id, message))

  def __getitem__(self, chat_id) -> SimpleMessage:
    return [i for i in self if i.chat_id == chat_id][0].message

class BaseKeyboard:
  messages: ReceivedMessages = None
  service_messages: dict = {}
  prefix = None

  def __init__(self, prefix, f):
    self.prefix = prefix
    self.F = f
    self.messages = ReceivedMessages()
    self.service_messages = {}

  def create_kb(self, buttons_info, row_width=1) -> InlineKeyboardMarkup:
    buttons = [
      InlineKeyboardButton(text=button['name'], callback_data=f'{self.prefix}{button["callback"]}')
      for button in buttons_info
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons], row_width=row_width)
