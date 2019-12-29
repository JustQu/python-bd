from socket import socket, AF_INET, SOCK_STREAM

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.label import Label
from kivy.uix.popup import Popup

import pickle

import sock_communication as sc
from sock_communication import get_response

from os import environ
from platform import system

import MenuBar
import GamePage

if system() == 'Linux':
    #for remote desktop
    environ['DISPLAY'] = ":0.0"


class mainApp(App):
    loged_in = BooleanProperty(False)
    admin = BooleanProperty(False)

    game_name = StringProperty('')
    genres = StringProperty('')
    platforms = StringProperty('')
    developer = StringProperty('')
    publishers = StringProperty('')
    score = StringProperty('')
    description = StringProperty('')

    user_login = StringProperty('')

    def __init__(self, **kwargs):
        super(clientApp, self).__init__(**kwargs)

    def build(self):
        self.rw = RootWidget()
        return RootWidget()
        #self.sm = MyScreenManager()
       # return self.sm

    def load_game_page(self, game_id):
        print(game_id)
        request = {}
        request['type'] = 'get_game_info'
        request['game_id'] = game_id
        response = get_response(request)
        print(response)
        if response['status'] == 'success':
            self.game_name = response['game_name']
            genres = []
            platforms = []
            publishers = []

            for genre in response['genres']:
                genres.append(genre[0])
            self.genres = ', '.join(genres)

            for platform in response['platforms']:
                platforms.append(platform[0])
            self.platforms = ', '.join(platforms)

            for publisher in response['publishers']:
                publishers.append(publisher[0])
            self.publishers = ', '.join(publishers)

            self.developer = response['developer']

            self.score = str(response['game_score'])

            self.description = response['description']
        self.rw.go_to_game_page()