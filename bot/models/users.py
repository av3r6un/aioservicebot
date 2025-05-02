from sqlalchemy import Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class BotUser(Base):
  __tablename__ = 'users'

  uid: Mapped[str] = mapped_column(String(6), primary_key=True)
  id: Mapped[int] = mapped_column(Integer, nullable=False)
  first_name: Mapped[str] = mapped_column(String(100), nullable=True)
  last_name: Mapped[str] = mapped_column(String(100), nullable=True)
  username: Mapped[str] = mapped_column(String(100), nullable=True)
  language_code: Mapped[str] = mapped_column(String(2), nullable=False)
  is_premium: Mapped[bool] = mapped_column(Boolean, nullable=False)
  config: Mapped[str] = mapped_column(String(255), nullable=True)
  assigned_addr: Mapped[str] = mapped_column(String(15), nullable=True)
  
  def __init__(self, uid, id, language_code, is_premium, first_name=None, last_name=None, username=None, **kwargs) -> None:
    self.uid = uid
    self.id = id
    self.language_code = language_code
    self.is_premium = is_premium
    self.first_name = first_name
    self.last_name = last_name
    self.username = username
  
  @property
  def json(self):
    return dict(uid=self.uid, id=self.id, first_name=self.first_name, last_name=self.last_name, language_code=self.language_code, is_premium=self.is_premium)

  def __repr__(self):
    return f'<User #{self.uid}>'
