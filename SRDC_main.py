###################################################################
#
#       - File: SRDC_main.py
#       - Author: Dylan Hendrix
#       - Discription: Main file that controls the flow of the app
#
###################################################################

# KivyMD Imports
from kivymd.app import MDApp

# Kivy Imports
from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition

# Import Screens
from SRDC_GSM import GlobalScreenManager, GSM
from SRDC_LoginScreen import LoginScreen
from SRDC_HomeScreen import HomeScreen
from SRDC_EODScreen import EODScreen
from SRDC_SelectionScreen import SelectionScreen

Builder.load_file("SRDC_Format.kv") # ABS PATH: C:/VS_Code/Python/Kivy_Testing/

# Init the screens
class SRDCApp(MDApp):
    def build(self):
        self.sm = GlobalScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(EODScreen(name='EOD'))
        self.sm.add_widget(SelectionScreen(name='selectionScreen'))

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.theme_palette = "BlueGray"
        self.sm.transition = NoTransition()

        return self.sm

    def on_start(self):
        GSM().switchScreen('login')


if __name__ == "__main__":
    SRDCApp().run()