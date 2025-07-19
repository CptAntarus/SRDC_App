import os
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton


class PhotoScreen(Screen):
    def on_enter(self):
        photoList = os.listdir("images")

        grid = self.ids.photoGrid
        grid.clear_widgets()

        for photo in photoList:
            justFileName = os.path.splitext(photo)[0]
            btn = MDRaisedButton(
                text=justFileName,
                on_release= lambda btn, p=photo: self.changePicture("images/" + p)
            )
            grid.add_widget(btn)

    def changePicture(self, newPicture):
        source = MDApp.get_running_app().root.get_screen("home")
        source.ids.HomeScreenPicture.source = newPicture
