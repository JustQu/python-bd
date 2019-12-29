from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.lang.builder import Builder

from sock_communication import get_response

from error_popup import error_popup

Builder.load_file('MenuBar.kv')

class MenuBar(BoxLayout):
    sm = ObjectProperty(None)
    a = ObjectProperty(None)
    admin = BooleanProperty(False)

    main_page = StringProperty('')

    user_login = StringProperty('')
    loged_in = BooleanProperty(False)

    user_field = ObjectProperty(None)
    login_field = ObjectProperty(None)
    register_field = ObjectProperty(None)
    change_password_field = ObjectProperty(None)

    def log_in(self, login, password):
        request = {}
        request['type'] = 'login'
        request['login'] = login
        request['password'] = password

        response = get_response(request)

        if response != {}:
            if response['status'] == 'success':
                self.a.loged_in = True
                self.loged_in = True
                self.user_login = login
                self.auth_token = response['auth_token']

                self.login_field.hide()
                self.user_field.show()
    
                if response['group'] == 'admin':
                   self.a.admin = True
                   self.admin = True
                else:
                    self.a.admin = False
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

    def show_user_field(self):
        self.user_field.show()
        self.change_password_field.hide()
    
    def show_change_password(self):
        self.user_field.hide()
        self.change_password_field.show()

    def log_out(self):
        self.loged_in = False
        self.a.loged_in = False
        self.a.admin = False
        self.user_login = ''
        self.auth_token = None
        self.show_login()

    def change_password(self, old_pw, new_pw):
        if (old_pw == new_pw):
            error_popup('Пароли совпадают. Введите новый пароль')
        request = {}
        request['type'] = 'change_password'
        request['login'] = self.user_login
        request['old_password'] = old_pw
        request['new_password'] = new_pw
        response = get_response(request)
        if response == None:
            error_popup('Произошла ошибка при смене пароля') 
            return 
        if response['status'] == 'fail':
            if 'message' in response:
                error_popup(response['message'])
            else:
                error_popup('Произошла ошибка при смене пароля') 
        elif response['status'] == 'success':
            self.user_field.show()
            self.change_password_field.hide()


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


class ChangePassword(RelativeLayout):

    def hide(self):
        self.saved_attr = self.size_hint_y, self.height, self.opacity
        self.size_hint_y = None
        self.height = 0
        self.opacity = 0

    def show(self):
        self.size_hint_y = 1
        self.opacity = 1