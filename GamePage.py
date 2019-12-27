from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang.builder import Builder

import MenuBar

print('here')

Builder.load_file('gamepage.kv')

class AdminPanel(RelativeLayout):
    pass

class GamePage(Screen):
    pass

# class GamePageApp(App):

#     def __init__(self, **kwargs):
#         super(GamePageApp, self).__init__(**kwargs)

#     def build(self):
#         return GamePage()


# app = GamePageApp()
# app.run()