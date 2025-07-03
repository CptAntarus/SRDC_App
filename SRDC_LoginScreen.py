from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from SRDC_GSM import GlobalScreenManager, GSM

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.themeStatus = "Dark"
        print("[LoginScreen] Initialized")

    def on_enter(self):
        self.ids.nameInput.text = ""
        self.ids.passwordInput.text = ""

    def validateCreds(self, name, password):
        print(f"[LoginScreen] Validating: {name} with password: {password}")
        name = (name or "").strip().lower()
        password = password or ""

        if not name or not password:
            MDSnackbar(
                MDLabel(text="Missing Input", theme_text_color="Custom", text_color="#F0FF18"),
                duration=.7
                ).open()
            return

        if name in GlobalScreenManager.VALID_USERS and password == GlobalScreenManager.VALID_USERS[name]:            
            GSM().switchScreen('home')
        else:
            MDSnackbar(
                MDLabel(text="Invalid Login Information", theme_text_color="Custom", text_color="#FF0D0D"),
                duration=.7
            ).open()
            self.ids.nameInput.text = ""
            self.ids.passwordInput.text = ""