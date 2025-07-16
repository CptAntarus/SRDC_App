###################################################################
#
#       - File: SRDC_main.py
#       - Author: Dylan Hendrix
#       - Discription: Main file that controls the flow of the app
#
###################################################################

# Standard Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
from SRDC_EditThemeScreen import EditThemeScreen

Builder.load_file("SRDC_Format.kv") # ABS PATH: C:/VS_Code/Python/Kivy_Testing/

# Init the screens
class SRDCApp(MDApp):
    def build(self):
        self.sm = GlobalScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(EODScreen(name='EOD'))
        self.sm.add_widget(SelectionScreen(name='selectionScreen'))
        self.sm.add_widget(EditThemeScreen(name='editThemeScreen'))

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.sm.transition = NoTransition()

        return self.sm

    def on_start(self):
        self.GenNamePasswordList()
        GSM().switchScreen('home')


    def GenNamePasswordList(self):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name("SRDCPasswords.json", scope)
        client = gspread.authorize(creds)

        sheet = client.open("SRDCPasswords").sheet1

        self.sheetData = sheet.get_all_records()



if __name__ == "__main__":
    SRDCApp().run()