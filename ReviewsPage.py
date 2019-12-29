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


from sock_communication import get_response

import MenuBar

Builder.load_file('ReviewsPage.kv')


class ViewReview(BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(False)

    login_label = ObjectProperty(None)
    text_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ViewReview, self).__init__(**kwargs)
        self.ids.text.bind(height=self.update)
       # self.update()

    # def refresh_view_attrs(self, rv, index, data):
    #     #self.height = self.ids.login.texture_size[1] + self.ids.text.texture_size[1]
    #     super(ViewReview, self).refresh_view_attrs(rv, index, data)
    
    def update(self, *args):
        print(self.ids.login.texture_size[1], self.ids.text.texture_size[1])
        self.height = self.ids.login.texture_size[1] + self.ids.text.texture_size[1] + self.ids.rating.texture_size[1]
        #return self.height


class RV1(RecycleView):
    
    def __init__(self, **kwargs):
        super(RV1, self).__init__(**kwargs)
        self.data = []

    def get_reviews(self, game_id):
        self.data =[]
        request = {}
        request['type'] = 'get_reviews'
        request['game_id'] = game_id
        response = get_response(request)
        print(response)
        for review in response['reviews']:
            self.data.append({'login': review[0], 'rating': str(review[1]), 'review_text': review[2]})
        #self.data = [{'text': str(x)} for x in range(100)]
        

# class ReviewsPageApp(App):
#     def build(self):
#         self.rv = RV1()
#         return RV1()

class ReviewsPage(Screen):
    rv = ObjectProperty(None)
    pass

# if __name__ == '__main__':
#     ReviewsPageApp().run()
