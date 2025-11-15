from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
Window.size = (350, 600)
kv =
MDFloatLayout:
md_bg_color: 1, 1, 1, 1
Eclass WeatherApp (MDApp):
def build(self):
return Builder.load_string(kv)