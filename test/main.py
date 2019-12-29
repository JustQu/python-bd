from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

from os import environ
from platform import system

if system() == 'Linux':
    #for remote desktop
    environ['DISPLAY'] = ":0.0"


class StartWindow(Screen):
    pass


class PortfolioOverview(Screen):
    pass


class Portfolio(Screen):
    pass


class Market(Screen):
    pass


class Economics(Screen):
    pass


class PortfolioTools(Screen):
    pass


class WindowManager(ScreenManager):
    pass


Builder.load_file("main.kv")


class TestApp(App):
    def build(self):
        return WindowManager()


if __name__ == "__main__":
    TestApp().run()