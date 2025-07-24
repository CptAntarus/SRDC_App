from kivymd.app import MDApp
# from oauth2client.service_account import ServiceAccountCredentials
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from SRDC_GSM import GlobalScreenManager, GSM

class SearchScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.keyboardBuilt = False

    def on_enter(self):
        Clock.schedule_once(self.delayed_init,0.1)

    def delayed_init(self,dt):
        if not self.keyboardBuilt:
            grid = self.ids.SelectionKeyBoard
            keys = ["Q","W","E","R","T","Y","U","I","O","P",
                    "A","S","D","F","G","H","J","K","L","-",
                    "Z","X","C","V","B","N","M"]
            otherKeys = ["Space","Back","Clear"]

            for text in keys:
                btn = MDRaisedButton(
                    text=text,
                    font_size="28sp",
                    on_release= lambda btn, t=text: self.editText(t.lower())
                )
                grid.add_widget(btn)

            for text in otherKeys:
                btn = MDRaisedButton(
                    text=text,
                    on_release= lambda btn, t=text: self.editText(t)
                )
                grid.add_widget(btn)
            
            self.keyboardBuilt = True
        
        # If the afternoonIn list is out of date update it
        if not GlobalScreenManager.AfternoonListUpToDate:
            MDApp.get_running_app().UpdateAfternoonList()
            GlobalScreenManager.AfternoonListUpToDate = True
        
        ##################################################
        #
        # - Can adjust the lists later if needed
        # - Currently using one DB for names/passwords
        #
        ##################################################
        if GlobalScreenManager.SCREEN_FLAG == "ECM":
            self.data = MDApp.get_running_app().EODsheetData #ECMsheetData
            self.ids.selectionScreenTopBar.title = "Morning Ext Care"
            self.ids.nameInput.icon_right = "death-star"
            
        if GlobalScreenManager.SCREEN_FLAG == "EOD":
            self.data = MDApp.get_running_app().EODsheetData
            self.ids.selectionScreenTopBar.title = "End Of Day Sign Out"
            self.ids.nameInput.icon_right = "death-star-variant"

        if GlobalScreenManager.SCREEN_FLAG == "ECAI":
            self.data = MDApp.get_running_app().EODsheetData #ECAsheetData
            self.ids.selectionScreenTopBar.title = "Afternoon Checkin"
            self.ids.nameInput.icon_right = "alphabet-aurebesh"
        if GlobalScreenManager.SCREEN_FLAG == "ECAO":
            self.data = MDApp.get_running_app().AfternoonInSheetData #ECAsheetData
            self.ids.selectionScreenTopBar.title = "Afternoon Checkout"
            self.ids.nameInput.icon_right = "alphabet-aurebesh"

        self.matchingLastNames = self.ids.matchingLastNames
        self.ids.nameInput.bind(text=self.onTextSearch)
        self.matchingLastNames.clear_widgets()
        self.ids.nameInput.text = ""
        self.matchingLastNames.clear_widgets()
        Clock.schedule_once(self.set_focus, 0.1)

    def set_focus(self, dt):
        self.ids.nameInput.focus = True

    def onTextSearch(self,instance, value):
        self.updateList(value)

    def updateList(self, searchText):
        container = self.ids.matchingLastNames
        container.clear_widgets()
        addedNames = set()

        for row in self.data:
            name = str(row.get("LastName", "")).strip()
            if searchText.lower() in name.lower() and name.lower() not in addedNames:
                item = OneLineListItem(text=name)
                item.bind(on_release=lambda instance, name=name: self.findPassword(name))
                container.add_widget(item)
                addedNames.add(name.lower())

    def findPassword(self, familyName=None):
        if familyName:
            userInput = familyName.strip().lower()
        else:
            userInput = self.ids.nameInput.text.strip().lower()

        for row in self.data:
            if str(row.get('LastName', "")).strip().lower() == userInput.lower():
                familyPassword = str(row.get('Passwords',""))
                self.changeScreen(familyName,familyPassword)
                break
    

    def editText(self, character):
        inputField = self.ids.nameInput

        if character == "Space":
            inputField.text += " "
        elif character == "Back":
            inputField.text = inputField.text[:-1]
        elif character == "Clear":
            inputField.text = ""
        else:
            inputField.text += character



    def changeScreen(self, familyName, familypassword):
        GlobalScreenManager.FAMILY_NAME = familyName.strip()
        GlobalScreenManager.FAMILY_PASSWORD = familypassword.strip()
        GSM().switchScreen('selectionScreen')