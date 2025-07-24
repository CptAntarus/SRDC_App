from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from SRDC_GSM import GlobalScreenManager, GSM

class HomeScreen(Screen):   # EOD page, Extended Care,
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_enter(self):
        GlobalScreenManager.SCREEN_HIST.clear()

    def openMenu(self,caller):
        options = ["In", "Out"]

        menu_items = [ {"text": i,"on_release": lambda x=i: self.selectOption(x)}
            for i in options ]

        self.menu = MDDropdownMenu(
            caller=caller,
            items=menu_items,
            width_mult=3,
        )
        self.menu.open()

    def selectOption(self, text):
        if text == 'In':
            GlobalScreenManager.SCREEN_FLAG = "ECAI"
            GSM().switchScreen('searchScreen')
        elif text == 'Out':
            GlobalScreenManager.SCREEN_FLAG = "ECAO"
            GSM().switchScreen('searchScreen')
        else:
            print("Error with ECA Dropdown selection")
        self.menu.dismiss()

    def switchToExtCareMorning(self):
        GlobalScreenManager.SCREEN_FLAG = "ECM"
        GSM().switchScreen('searchScreen')

    def switchToEOD(self):
        GlobalScreenManager.SCREEN_FLAG = "EOD"
        GSM().switchScreen("searchScreen")

    # def switchToExtCareAfternoon(self):
    #     GlobalScreenManager.SCREEN_FLAG = "ECA"
    #     GSM().switchScreen('searchScreen')