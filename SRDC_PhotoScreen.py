from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

from SRDC_GSM import GlobalScreenManager, GSM


class PhotoScreen(Screen):
    def changePicture(self, newPicture):
        source = MDApp.get_running_app().root.get_screen("home")
        source.ids.HomeScreenPicture.source = newPicture
