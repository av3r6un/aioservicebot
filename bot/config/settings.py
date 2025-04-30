from aiogram.types import BotCommand
from yaml import safe_load
import os


class Settings:
  ROOT = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..'))
  MESSAGE_PATH = os.path.join(ROOT, 'config', 'messages.yaml')

  def __init__(self):
    self.TOKEN = os.getenv('BOT_TOKEN')
    self.WH_PATH = os.getenv('WH_PATH')
    self.BASE_WH_URL = os.getenv('SERVER_ADDR')
    self.WS_HOST = os.getenv('WS_HOST', '127.0.0.1')
    self.WS_PORT = int(os.getenv('WS_PORT', 8090))

    self.raw_config = self._load_settings()

    self.COMMANDS = self._init_commands(self.raw_config['commands'])

  def _load_settings(self):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings.yaml')) as f:
      data = safe_load(f)
    dd = data.copy()
    dd.pop('commands')

    self.__dict__.update(dd)

    return data

  def _init_commands(self, commands: dict):
    return [BotCommand(command=command, description=description) for command, description in commands.items()] 
