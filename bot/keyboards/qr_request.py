from aiogram.filters.callback_data import CallbackData
from typing import Optional
from .base import BaseKeyboard


class QRFilter(CallbackData, prefix='qrr'):
  action: str
  value: Optional[str] = None


class QRRequest(BaseKeyboard):
  buttons = [
    { 'name': 'QR-code', 'callback': 'showQR' },
  ]

  def __init__(self) -> None:
    super().__init__('qrr_', QRFilter)
    self.kb = self.create_kb(self.buttons, row_width=1)

  def add_instance(self, chat_id, service, original, instance):
    self.instance = instance
    self.service_messages[chat_id] = service
    self.original = original
    self.messages.add(chat_id, original)
