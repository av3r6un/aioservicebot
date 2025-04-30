from yaml import safe_load
from typing import List

class Text:
  lang: str = None
  text: str = None

  def __init__(self, lang, text):
    self.text = text
    self.lang = lang
    
  def __repr__(self):
    return f'<Lang={self.lang} Text={self.text}>'
  
class LanguagedText(List[Text]):
  def __init__(self, *args):
    for arg in args:
      self.append(Text(*arg))
  
  def __getitem__(self, value):
    for item in self:
      if item.lang == value:
        return item.text


class Message:
  _text: Text = None
  parse_mode: str = None
  disable_notification: bool = None
  protect_content: bool = None
  disable_web_page_preview: bool = None
  message_effect_id: int = None

  def __init__(self, text: dict, parse_mode = None, disable_notification = None, protect_content = None, disable_web_page_preview=None, message_effect_id = None, **kwargs):
    self._text = LanguagedText(*text.items())
    self.parse_mode = parse_mode
    self.disable_notification = disable_notification
    self.protect_content = protect_content
    self.disable_web_page_preview = disable_web_page_preview
    self.message_effect_id = message_effect_id

  def __call__(self, lang):
    self._lang = lang
    self.text = self._text[lang]
    return self
  
  @property
  def general(self):
    return dict(parse_mode=self.parse_mode, disable_notification=self.disable_notification, protect_content=self.protect_content, disable_web_page_preview=self.disable_web_page_preview, message_effect_id=self.message_effect_id)

  @property
  def m(self):
    return dict(text=self.text, **self.general)
  
  @property
  def c(self):
    return dict(caption=self.text, **self.general)
  
  def __repr__(self):
    return f'<Message lang={self._lang}>'

class Messages:
  def __init__(self, path) -> None:
    self.LANG = 'ru'
    self._load_messages(path)

  def _load_messages(self, path) -> None:
    with open(path, 'r', encoding='utf-8') as f:
      data = safe_load(f)
      for name, kwargs in data.items():
        self.__dict__[name] = Message(**kwargs)

  @property
  def lang(self):
    return self.LANG
  
  @lang.setter
  def lang(self, value):
    self.LANG = value
  
  def __getitem__(self, message_name) -> Message:
    if message_name in self.__dict__:
      return self.__dict__[message_name](self.LANG)
    else:
      return Message('')

