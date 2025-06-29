from kivy.uix.screenmanager import Screen
from SRDC_GSM import GlobalScreenManager, GSM

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("[LoginScreen] Initialized")

    def on_enter(self):
        self.ids.nameInput.text = ""
        self.ids.passwordInput.text = ""

    def validateCreds(self, name, password):
        print(f"[LoginScreen] Validating: {name} with password: {password}")
        name = name.strip().lower()

        if name in GlobalScreenManager.VALID_USERS and password == GlobalScreenManager.VALID_USERS[name]:            
            GSM().switchScreen('home')
        else:
            print("Incorect Login Information")