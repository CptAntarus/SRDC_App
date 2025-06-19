from kivy.uix.screenmanager import Screen

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("[LoginScreen] Initialized")

    def validateCreds(self, name, password):
        print(f"[LoginScreen] Validating: {name} with password: {password}")

        if name == "Dylan" and password == "1234":
            self.manager.current = 'home'
