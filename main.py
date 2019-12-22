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

import pickle

import sock_communication as sc

from os import environ
from platform import system

if system() == 'Linux':
    #for remote desktop
    environ['DISPLAY'] = ":0.0"


#connecting to the server
host = 'localhost'
port = 8000
addr = (host, port)

request = {}


data = [
    {
        'game_name': 'Sekiro',
        'game_genre': 'action',
        'year': 2019,
        'developer': 'Fromsoftware'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    },
    {
        'game_name': 'The binding of Isaac',
        'game_genre': 'rogue-like',
        'year': '2017',
        'developer': 'Edmund MacMillan'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    },
    {
        'game_name': 'the Witcher 3',
        'game_genre': 'rpg',
        'year': 2015,
        'developer': 'CD Projekt Red'
    }
]

def get_response(request):
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    tcp_socket.connect(addr)
    sc.send_msg(tcp_socket, request)
    response = sc.recv_msg(tcp_socket)
    tcp_socket.close()
    response = pickle.loads(response)
    print(response)
    return response

class SearchEngine(BoxLayout):
    pass


class MenuBar(BoxLayout):
    loged_in = BooleanProperty(False)
    login = ObjectProperty(None)
    password = ObjectProperty(None)

    def log_in(self, login, password):
        request = {}
        request['type'] = 'login'
        request['login'] = login
        request['password'] = password

        response = get_response(request)

        if response != {}:
            if response['status'] == 'success':
                client.loged_in = True
                self.loged_in = True
                client.user_login = login
                #self.size_hint_y = None
                #self.height = 0
                if response['group'] == 'admin':
                    client.admin = True
                else:
                    client.admin = False
    
    def register(self, login, password, password2):
        if password != password2:
            return None

#Отображение имя пользователя и кнопки выхода
class UserField(RelativeLayout):
    pass

#форма входа
class LoginField(RelativeLayout):
    pass

#форма регистрации
class RegisterField(RelativeLayout):
    pass


class GamePage(Screen):
    
    def __init__(self, **kwargs):
        super(GamePage, self).__init__(**kwargs)


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
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        if is_selected:
            #don't know how make it more elegant
            rv.parent.parent.go_to_game_page()
            rv.pepega.clear_selection()
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class AdminPanel(RelativeLayout):
    pass


class NewGamePage(BoxLayout, Screen):
    pass


#list of games
class RV(RecycleView):
    pepega = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{
                'game_name':    x['game_name'],
                'game_genre':   x['game_genre'],
                'year':         str(x['year'])}
                    for x in data]


class RootWidget(BoxLayout, Screen):
    sm = ObjectProperty(None)


class MyScreenManager(ScreenManager):
 
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)

    def go_to_game_page(self):
        self.current = 'game_page'

    def go_to_main_page(self):
        self.current = 'main_page'

    def go_to_new_game_page(self):
        self.current = 'new_game_page'


class clientApp(App):

    loged_in = BooleanProperty(False)
    admin = BooleanProperty(False)

    user_login = StringProperty('')

    def __init__(self, **kwargs):
        super(clientApp, self).__init__(**kwargs)

    def build(self):
        self.sm = MyScreenManager()
        return self.sm

    def load_game_page(self, name, selected):
        if selected:
            self.sm.go_to_game_page()

client = clientApp()
client.run()
