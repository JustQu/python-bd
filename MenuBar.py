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
from kivy.lang.builder import Builder

import pickle

import sock_communication as sc
from sock_communication import get_response

from os import environ
from platform import system

if system() == 'Linux':
    #for remote desktop
    environ['DISPLAY'] = ":0.0"

Builder.load_file('MenuBar.kv')

class MenuBar(BoxLayout):
    admin = BooleanProperty(False)

    loged_in = BooleanProperty(False)
    login = ObjectProperty(None)
    password = ObjectProperty(None)

    user_field = ObjectProperty(None)
    login_field = ObjectProperty(None)
    register_field = ObjectProperty(None)

    def log_in(self, login, password):
        request = {}
        request['type'] = 'login'
        request['login'] = login
        request['password'] = password

        response = get_response(request)

        if response != {}:
            if response['status'] == 'success':
               # client.loged_in = True
                self.loged_in = True
              #  client.user_login = login
                self.user_login = login


                self.login_field.hide()
                self.user_field.show()
                #self.size_hint_y = None
                #self.height = 0
                if response['group'] == 'admin':
                   # client.admin = True
                   self.admin = True
                else:
                    #client.admin = False
                    self.admin = False

    
    def register(self, login, password, password2):
        if password != password2:
            error_popup('Ошибка. Пароли не совпадают')
            return None
        
        if len(login) < 2:
            error_popup('Ошибка. Имя пользователя должно быть не меньше двух символов')
            return
        if len(password) > 20 or len(password) < 6:
            error_popup('Ошибка. Пароль должен быть от 6 до 20 символов в длину')
            return

        request = {}
        request['type'] = 'register'
        request['login'] = login
        request['password'] = password

        response = get_response(request)
        if response['status'] == 'fail':
            error_popup(response['message'])
            return
        
        self.register_field.hide()
        self.login_field.show()

    def show_register(self):
        self.login_field.hide()
        self.register_field.show()

    def show_login(self):
        self.register_field.hide()
        self.login_field.show() 


#Отображение имя пользователя и кнопки выхода
class UserField(RelativeLayout):

    def hide(self):
        self.saved_attr = self.size_hint_y, self.height, self.opacity
        self.size_hint_y = None
        self.height = 0
        self.opacity = 0

    def show(self):
        #self.size_hint_y, self.height, self.opacity = self.saved_attr
        self.size_hint_y = 1
        self.opacity = 1


#форма входа
class LoginField(RelativeLayout):
    
    def hide(self):
        self.saved_attr = self.size_hint_y, self.height, self.opacity
        self.size_hint_y = None
        self.height = 0
        self.opacity = 0

    def show(self):
        #self.size_hint_y, self.height, self.opacity = self.saved_attr
        self.size_hint_y = 1
        self.opacity = 1


#форма регистрации
class RegisterField(RelativeLayout):

    def hide(self):
        self.saved_attr = self.size_hint_y, self.height, self.opacity
        self.size_hint_y = None
        self.height = 0
        self.opacity = 0

    def show(self):
       # self.size_hint_y, self.height, self.opacity = self.saved_attr
        self.size_hint_y = 1
        self.opacity = 1