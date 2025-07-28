###################################################################
#
#       - File: SRDC_main.py
#       - Author: Dylan Hendrix
#       - Discription: Main file that controls the flow of the app
#
###################################################################

# Standard Imports
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

# KivyMD Imports
from kivymd.app import MDApp

# Kivy Imports
from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition

# Import Screens
from SRDC_GSM import GlobalScreenManager, GSM
#from SRDC_LoginScreen import LoginScreen
from SRDC_HomeScreen import HomeScreen
from SRDC_SearchScreen import SearchScreen
from SRDC_SelectionScreen import SelectionScreen
from SRDC_EditThemeScreen import EditThemeScreen
from SRDC_PhotoScreen import PhotoScreen

Builder.load_file("SRDC_Format.kv")

# Init the screens
class SRDCApp(MDApp):
    def build(self):
        self.sm = GlobalScreenManager()
        #self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(SearchScreen(name='searchScreen'))
        self.sm.add_widget(SelectionScreen(name='selectionScreen'))
        self.sm.add_widget(EditThemeScreen(name='editThemeScreen'))
        self.sm.add_widget(PhotoScreen(name='photoScreen'))

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.sm.transition = NoTransition()

        return self.sm

    def on_start(self):
        self.GenNamePasswordList()
        GSM().switchScreen('home')


    def GenNamePasswordList(self):
        scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
        creds_path = os.getenv("SRDC_CREDS_PATH")

        if creds_path:
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        else:
            print("Google credentials path is not set!")
        client = gspread.authorize(creds)

        print("Getting EOD Records")
        EODsheet = client.open("SRDC_DB").worksheet("Passwords")
        self.EODsheetData = EODsheet.get_all_records()


    def UpdateAfternoonList(self):
        scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
        creds_path = os.getenv("SRDC_CREDS_PATH")

        if creds_path:
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        else:
            print("Google credentials path is not set!")
        client = gspread.authorize(creds)

        print("Getting Afternoon Records")
        AfternoonInSheet = client.open("SRDC_DB").worksheet("ExtCareAfternoonIn")
        self.AfternoonInSheetData = AfternoonInSheet.get_all_records()


if __name__ == "__main__":
    SRDCApp().run()
