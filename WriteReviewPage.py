from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.uix.recycleview.layout import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.screenmanager import Screen

import MenuBar

Builder.load_file('writereview.kv')

class WriteReviewPage(Screen):
    pass


# class testApp(App):
#     def build(self):
#         return WriteReviewPage()

# if __name__ == '__main__':
#     testApp().run()
