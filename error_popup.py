from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang.builder import Builder


Builder.load_file('error_popup.kv')

class MyLabel(Label):
    def __init__(self, **kwargs):
        super(MyLabel, self).__init__(**kwargs)

def error_popup(error_message):
    popup = Popup(title='Ошибка',
                content=MyLabel(text=error_message),
                auto_dismiss=True,
                size = (300, 300),
                size_hint = (None, None))
    popup.open()