from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from SRDC_GSM import GlobalScreenManager, GSM

class EditThemeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.themeStatus = "Dark"

    def on_enter(self):
        self.makeButtons()

    def toggleLightDark(self):
        if self.themeStatus == "Dark":
            self.themeStatus = "Light"
        else:
            self.themeStatus = "Dark"
        MDApp.get_running_app().theme_cls.theme_style = self.themeStatus


    def makeButtons(self):
        listColors = ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 
                      'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 
                      'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']

        grid = self.ids.colorGrid
        grid.clear_widgets()

        for color in listColors:
            btn = MDRaisedButton(
                text=color,
                on_release=lambda instance, c = color: self.changeColor(c),
                size_hint=(None,None),
                size=("400dp","40dp")
            )
            grid.add_widget(btn)


    def changeColor(self, newColor):
        MDApp.get_running_app().theme_cls.primary_palette = newColor

    def changePicture(self, newPicture):
        source = MDApp.get_running_app().root.get_screen("home")
        source.ids.HomeScreenPicture.source = newPicture