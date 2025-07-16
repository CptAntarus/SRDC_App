from kivy.uix.screenmanager import Screen
from SRDC_GSM import GlobalScreenManager, GSM

class HomeScreen(Screen):   # EOD page, Extended Care,
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_enter(self):
        GlobalScreenManager.SCREEN_HIST.clear()
        GlobalScreenManager.SCREEN_HIST.append("login")
