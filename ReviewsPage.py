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


from os import environ

import MenuBar

environ['DISPLAY'] = ':0.0'

Builder.load_file('ReviewsPage.kv')

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


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
        self.height = self.ids.login.texture_size[1] + self.ids.text.texture_size[1]
        #return self.height


class RV(RecycleView):
    
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.get_reviews()

    def get_reviews(self):
        self.data = [{'login': 'pepega',
                        'review_text': 'REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE.Replace with long text later and test. \n' * 20},
                      {'login': 'pupa', 
                        'review_text': 'zalupa'},
                        {'login': 'pupa', 
                        'review_text': 'zalupa'},
                        {'login': 'pupa', 
                        'review_text': 'zalupa'},
                        {'login': 'pupa', 
                        'review_text': 'zalupa'}]
        #self.data = [{'text': str(x)} for x in range(100)]
        

class ReviewsPageApp(App):
    def build(self):
        self.rv = RV()
        return RV()

class ReviewsPage(Screen):
    pass

if __name__ == '__main__':
    ReviewsPageApp().run()
