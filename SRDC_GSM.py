from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

class GlobalScreenManager(ScreenManager):
    SCREEN_HIST = []

    FAMILY_NAME = ""
    FAMILY_PASSWORD = ""


    VALID_USERS = {
        "dylan"  : "7567",
        "taylor" : "5555",
        "april"  : "1409",
        "beth"   : "0316"
    }
    
    def switchScreen(self, newScren):
        GlobalScreenManager.SCREEN_HIST.append(self.current)
        self.current = newScren

    def backButton(self, *args):
        self.current = GlobalScreenManager.SCREEN_HIST.pop()

    def reset(self):
        GlobalScreenManager.SCREEN_HIST.clear()

        loginScreen = self.get_screen('login')
        loginScreen.ids.nameInput.text = ""
        loginScreen.ids.passwordInput.text = ""

def GSM():
    return MDApp.get_running_app().root