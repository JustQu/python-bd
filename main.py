'''
Course work for databases discipline

Задача программы получать информацию об компьютерных играх,
подключаясь к серверу
Пользователь может оставлять оценку и отзывы об играх и читать 
отзывы других пользователей

Sedenkov Nikita 2019
'''

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
import ReviewsPage
import WriteReviewPage

if system() == 'Linux':
    #for remote desktop
    environ['DISPLAY'] = ":0.0"

from error_popup import error_popup

class SearchEngine(BoxLayout):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last = BooleanProperty(True)


#one game in the list
class GameRow(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        print(1)
        self.index = index
        return super(GameRow, self).refresh_view_attrs(
            rv, index, data)

    def on_press(self):
        print('Selected: {}'.format(self.id))

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(GameRow, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            print('Selected: {}'.format(self.index))
            client.load_game_page(self.game_id)
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        if is_selected:
            #don't know how make it more elegant
            client.rw.sm.go_to_game_page()
            rv.pepega.clear_selection()
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class AdminPanel(RelativeLayout):
    pass


class NewGamePage(BoxLayout, Screen):

    def add_game(self, **kwargs):
        request = {}
        request['type'] = 'add_game'
        request['game_name'] = kwargs['game_name']
        request['genres'] = {x.strip() for x in kwargs['genres'].split(';')}
        request['developer'] = kwargs['developer']
        request['publishers'] = {x.strip() for x in kwargs['publishers'].split(';')}
        request['platforms'] = {x.strip() for x in kwargs['platforms'].split(';')}
        request['rating'] = kwargs['rating']
        request['release_date'] = kwargs['release_date']
        request['description'] = kwargs['description']
        response = get_response(request)
        if response['status'] != 'success':
            print("Fail")

class InputFileDropDown(BoxLayout):
    pass

#list of games
class RV(RecycleView):
    pepega = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.search()
        # self.data = [{
        #         'game_name':    x['game_name'],
        #         'game_genre':   x['game_genre'],
        #         'game_year':         str(x['game_year'])}
        #             for x in data]

    def search(self, **kwargs):
        request = {}
        request['type'] = 'search'
        if kwargs is not None:
            request.update(kwargs) 
        #print(request['kwargs'])
        try:
            response = get_response(request)
        except:
            popup = Popup(title='Test popup', content=Label(text='Hello world'),
              auto_dismiss=False)
            popup.open()
            return

        if response['status'] == 'success':
            self.data = []
            for game_info in response['game_list']:
                self.data.append({'game_id': game_info[0],
                             'game_name': game_info[1],
                             'game_year': str(game_info[2]),
                             'game_score': str(game_info[3])})
        else:
            self.popup = Popup(title='Test popup',
                    content=Label(text='Hello world'),
                    size_hint=(None, None), size=(400, 400))
            self.popup.open(animation=False)


class MainPage(BoxLayout, Screen):
    sm = ObjectProperty(None)
    rv = ObjectProperty(None)


class RootWidget(BoxLayout):
    sm = ObjectProperty(None)
    mb = ObjectProperty(None)

class MyScreenManager(ScreenManager):
    rvws = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

    def go_to_game_page(self):
        self.current = 'game_page'

    def go_to_main_page(self):
        self.current = 'main_page'

    def go_to_new_game_page(self):
        self.current = 'new_game_page'

    def go_to_write_review(self):
        if not self.parent.mb.loged_in:
            error_popup('Чтобы оставить отзыв вы должны быть авторизованы.')
        else:
            self.current = 'write_review_page'

    def go_to_reviews_page(self, game_id):
        self.rvws.rv.get_reviews(game_id)
        self.current = 'reviews_page'


class clientApp(App):

    loged_in = BooleanProperty(False)
    admin = BooleanProperty(False)

    game_name = StringProperty('')
    release_date = StringProperty('')
    game_score = StringProperty('')
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
        return self.rw

    def write_review(self, text, score):
        request = {}
        request['type'] = 'write_review'
        request['game_id'] = self.game_id
        request['text'] = text
        request['score'] = score
        request['auth_token'] = self.rw.mb.auth_token
        response = get_response(request)

    def load_game_page(self, game_id):
        self.game_id = game_id
        print(game_id)
        request = {}
        request['type'] = 'get_game_info'
        request['game_id'] = game_id
        response = get_response(request)
        print(response)
        if response['status'] == 'success':
            self.game_name = response['game_name']
            self.release_date = str(response['release_date'])
            self.game_score = str(response['game_score'])
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
        self.rw.sm.go_to_game_page()


client = clientApp()
client.run()
