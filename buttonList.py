from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.recycleview.layout import RecycleDataViewBehavior

from os import environ
environ['DISPLAY'] = ':0.0'

items = [
    {"color":(1, 1, 1, 1), "font_size": "20sp", "text": "white",     "input_data": ["some","random","data"]},
    {"color":(.5,1, 1, 1), "font_size": "30sp", "text": "lightblue", "input_data": [1,6,3]},
    {"color":(.5,.5,1, 1), "font_size": "40sp", "text": "blue",      "input_data": [64,16,9]},
    {"color":(.5,.5,.5,1), "font_size": "70sp", "text": "gray",      "input_data": [8766,13,6]},
    {"color":(1,.5,.5, 1), "font_size": "60sp", "text": "orange",    "input_data": [9,4,6]},
    {"color":(1, 1,.5, 1), "font_size": "50sp", "text": "yellow",    "input_data": [852,958,123]},
    {"color":(1, 1, 1, 1), "font_size": "50sp", "text": "s",         "input_data": ["some","2","data"]},
    {"color":(1, 1, 1, 1), "font_size": "50sp", "text": "s",         "input_data": ["some","2","data"]},
    {"color":(1, 1, 1, 1), "font_size": "50sp", "text": "s",         "input_data": ["some","2","data"]},
    {"color":(1, 1, 1, 1), "font_size": "50sp", "text": "s",         "input_data": ["some","2","data"]},
    {"color":(1, 1, 1, 1), "font_size": "50sp", "text": "s",         "input_data": ["some","2","data"]}
]

class Test(RecycleDataViewBehavior, BoxLayout):
    def print_data(self,data):
        print(data)

class MyButton(Button):

    def print_data(self,data):
        print(data)

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [item for item in items]

class Root1(BoxLayout):
    pass

class buttonsApp(App):
    def build(self):
        return Root1()

if __name__ == '__main__':
    buttonsApp().run()