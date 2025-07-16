from kivymd.app import MDApp
# from oauth2client.service_account import ServiceAccountCredentials
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from SRDC_GSM import GlobalScreenManager, GSM

class EODScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.delayed_init,0.1)

    def delayed_init(self,dt):
        self.data = MDApp.get_running_app().sheetData

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