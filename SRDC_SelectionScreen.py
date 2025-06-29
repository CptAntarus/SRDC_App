import pandas as pd
import gspread
from kivymd.uix.list import OneLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from SRDC_GSM import GlobalScreenManager

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class SelectionScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.delayedInit,0.1)


    def delayedInit(self, dt):
        self.ExcelList = pd.read_excel("C:/VS_Code/Python/Kivy_Testing/SRDCPasswords.xlsx")

        print(self.ExcelList)

        self.ids.familyName.text = GlobalScreenManager.FAMILY_NAME
        self.ids.familyPassword.text = GlobalScreenManager.FAMILY_PASSWORD

        self.showOptions()

    def showOptions(self):
        container = self.ids.familyList
        container.clear_widgets()
        tempFirstNames = []

        # Create simlified list of first names
        for i, row in self.ExcelList.iterrows():
            tempLName = str(row["LastName"]).strip().lower()
            if tempLName.lower() == GlobalScreenManager.FAMILY_NAME.lower():
                firstNames = str(row["FirstName"]).strip()
                tempFirstNames.append(str(firstNames))

        for name in tempFirstNames:
            item = OneLineAvatarIconListItem(text=name)
            checkbox = RightCheckbox()
            item.add_widget(checkbox)
            container.add_widget(item)

  


    # # Push Name&Password to GoogleDoc
    # def addToList(self, obj):
    #     if self.selectedCamper is not None:
    #         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #         # Google Sheets API setup
    #         scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    #         creds = ServiceAccountCredentials.from_json_keyfile_name("C:\VS_Code\Python\Kivy_Testing\creds.json", scope)
    #         client = gspread.authorize(creds)

    #         # Open the spreadsheet and sheet
    #         sheet = client.open("SignedOutCampers").worksheet("Campers")

    #         # Append the data
    #         sheet.append_row([
    #             str(self.selectedCamper['LastNames']),
    #             str(self.selectedCamper['Passwords']),
    #             timestamp
    #         ])

    #     self.dialog.dismiss()
