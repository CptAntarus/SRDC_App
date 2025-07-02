import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from kivymd.uix.screen import Screen
from kivymd.uix.list import OneLineListItem
from kivymd.uix.textfield import MDTextField
from SRDC_GSM import GlobalScreenManager, GSM
from kivy.clock import Clock



class EODScreen(Screen):
    def on_enter(self):
        self.ExcelList = pd.read_excel("C:/VS_Code/Python/Kivy_Testing/SRDCPasswords.xlsx")
        self.matchingLastNames = self.ids.matchingLastNames
        self.ids.nameInput.bind(text=self.onTextSearch)
        self.matchingLastNames.clear_widgets()
        self.ids.nameInput.text = ""
        self.ids.matchingLastNames.clear_widgets()
        Clock.schedule_once(self.setFocus,0.1)

    def setFocus(self, dt):
        self.ids.nameInput.focus = True

    def onTextSearch(self, instance, value):
        self.updateList(value)

    def updateList(self, searchText):
        container = self.ids.matchingLastNames
        container.clear_widgets()
        addedNames = set()

        for index, row in self.ExcelList.iterrows():
            name = str(row["LastName"]).strip()
            if searchText.lower() in name.lower() and name.lower() not in addedNames:
                item = OneLineListItem(text=name)
                item.bind(on_release=lambda instance, name=name: self.findPassword(name))

                container.add_widget(item)
                addedNames.add(name.lower())

    # Shows Output Based on search input
    def findPassword(self, familyName=None):
        if familyName:
            userInput = familyName.strip().lower()
        else:
            userInput = self.ids.nameInput.text.strip().lower()

        for index, row in self.ExcelList.iterrows():
            if str(row['LastName']).strip().lower() == userInput.lower():
                familyPassowrd = str(row['Passwords'])
                self.changeScreen(familyName, familyPassowrd)
                break

    # Save Globals and switch to selction screen
    def changeScreen(self, familyName, familyPassword):
        GlobalScreenManager.FAMILY_NAME = familyName.strip() #str(f"Family:   {familyName}")
        GlobalScreenManager.FAMILY_PASSWORD = familyPassword.strip() #str(f"Password:   {familyPassword}")
        GSM().switchScreen('selectionScreen')
