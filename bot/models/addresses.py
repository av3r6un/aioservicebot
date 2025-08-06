from sqlalchemy import Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Address(Base):
  __tablename__ = 'adressess'
  
  uid: Mapped[str] = mapped_column(String(7), primary_key=True)
  uuid: Mapped[str] = mapped_column(String(6), ForeignKey('users.uid'), nullable=False)
  assigned: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
  config: Mapped[str] =mapped_column(String(255), nullable=False)
  
  def __init__(self, uid, uuid, assigned, config, **kwargs) -> None:
    self.uid = uid
    self.uuid = uuid
    self.assigned = assigned
    self.config = config
  
  @property
  def json(self):
    return dict(uid=self.uid, uuid=self.uuid, assigned=self.assigned, config=self.config)
