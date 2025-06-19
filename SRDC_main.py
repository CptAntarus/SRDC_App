###################################################################
#
#       - File: SRDC_main.py
#       - Author: Dylan Hendrix
#       - Discription: Main file that controls the flow of the app
#
###################################################################

# KivyMD Imports
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

# Kivy Imports
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, NoTransition

# Import Screens
#from SRDC_GSM import GlobalScreenManager
from SRDC_LoginScreen import LoginScreen
from SRDC_HomeScreen import HomeScreen
from SRDC_EODScreen import EODScreen
# class ExtCareScreen(Screen):
#     pass

Builder.load_file("SRDC_Format.kv") # ABS PATH: C:/VS_Code/Python/Kivy_Testing/

# Init the screens
class SRDCApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.theme_palette = "BlueGray"
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(EODScreen(name='EOD'))

        sm.current = 'home'

        return sm
    
if __name__ == "__main__":
    SRDCApp().run()