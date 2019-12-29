from kivy.uix.recycleview import RecycleView
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.stencilview import StencilView
from kivy.app import App
from kivy.metrics import sp, dp
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.recycleview import RecycleView
import random
from kivy.animation import Animation

from os import environ
environ['DISPLAY'] = ':0.0'

Builder.load_string("""
<ListItem>:
    title: title
    subtitle: subtitle
    long: long
    canvas.before:
        Color:
            rgba: (.25, .25, .25, 1) if self.index % 2 else (.125, .125, .125, 1)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: dp(10),
        Color:
            rgba: 0, 0, 0, 1
        Line:
            rounded_rectangle: [self.pos[0], self.pos[1], self.size[0], self.size[1], 5]
    Label:
        id: title
        size_hint: None, None
        halign: 'left'
        text: root.titletext
    Label:
        id: subtitle
        size_hint: None, None
        halign: 'left'
        text: root.subtitletext
    Label:
        id: long
        size_hint: None, None
        halign: 'left'
        text: root.longtext

# app example
<RootWidget>:
    rv: rv
    orientation: "vertical"
    RecycleView:
        id: rv
""")

class ListItem(RecycleView, FloatLayout, StencilView):
    index = NumericProperty(0)
    titletext = StringProperty('')
    subtitletext = StringProperty('')
    longtext = StringProperty('')
    rv = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.height == dp(40):
                target_height = dp(40 + self.long.texture_size[1])
            else:
                target_height = dp(40)
            anim = Animation(height=int(target_height), d=0.2)
            anim.start(self)
            return True
        return super(ListItem, self).on_touch_down(touch)

    def refresh_view_layout(self, rv, index, pos, size, viewport):
        # title will be 20 pixels, subtitle 20 pixels, and longtext takes
        # the rest
        base_y = pos[1] + size[1] - dp(40)
        self.title.pos = (int(dp(10)), int(base_y + dp(20)))
        self.subtitle.pos = (int(dp(10)), int(base_y))
        self.title.size = (int(size[0] - dp(20)), int(dp(20)))
        self.subtitle.size = (int(size[0] - dp(20)), int(dp(20)))
        self.long.text_size = (int(size[0] - dp(20)), None)
        self.long.texture_update()
        self.long.size = (int(size[0] - dp(20)), int(self.long.texture_size[1]))
        self.long.pos = (int(dp(10)), int(base_y - self.long.height))
        super(ListItem, self).refresh_view_layout(rv, index, pos, size, viewport)

    def on_height(self, instance, value):
        if self.rv:
            if self.rv.data[self.index]['height'] != value:
                self.rv.data[self.index]['height'] = value
                self.rv.refresh_views(data=True)

class RootWidget(BoxLayout):
    pass

class RecycleViewApp(App):
    def build(self):
        self.root = RootWidget()
        rv = self.root.rv
        rv.key_viewclass = "viewclass"
        rv.key_size = "height"
        self.generate_new_data()
        return self.root

    def generate_new_data(self):
        # Create a data set
        data = []
        names = ["Robert", "George", "Joseph", "Donald", "Mark", "Anthony", "Gary"]
        titles = ["Dr.", "Mr.", "Sir", "M.D.", "Professor", "Great Exalted One"]
        lengthy_text = """Sed ut perspiciatis unde omnis iste natus error sit
voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa
quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt
explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut
fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi
nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet,
consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut
labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam,
quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid
ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea
voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem
eum fugiat quo voluptas nulla pariatur?"""
        for x in range(1000):
            data.append({
                "index": x,
                "viewclass": "ListItem",
                "titletext": random.choice(titles),
                "subtitletext": random.choice(names),
                "longtext": lengthy_text,
                "height": dp(40),
                "rv": self.root.rv
            })

        self.root.rv.data = data

RecycleViewApp().run()