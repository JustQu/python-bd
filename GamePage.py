from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang.builder import Builder
from os import environ
from platform import system

import MenuBar

print('here')
if system() == 'Linux':
    #for remote desktop
    environ['DISPLAY'] = ":0.0"

class AdminPanel(RelativeLayout):
    pass

class GamePage(Screen):
    pass

class GamePageApp(App):

    def __init__(self, **kwargs):
        super(GamePageApp, self).__init__(**kwargs)

    def build(self):
        return GamePage()


app = GamePageApp()
app.run()