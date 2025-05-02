from aiogram.filters.callback_data import CallbackData
from typing import Optional
from .base import BaseKeyboard

class QRRequest(BaseKeyboard):
  buttons = [
    { 'name': 'QR-code', 'callback': 'showQR' },
  ]

  def __init__(self) -> None:
    super().__init__('qrr')
    self.kb = self.create_kb(self.buttons, row_width=1)

  def add_instance(self, chat_id, service, original, instance):
    self.instance = instance
    self.service_messages[chat_id] = service
    self.original = original
    self.messages.add(chat_id, original)

  def extract_action(self, data: str):
    filter = f'{self.prefix}:'
    if filter in data:
      data = data.replace(filter, '')
      return data
    return None
