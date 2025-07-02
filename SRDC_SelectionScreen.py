import pandas as pd
import gspread
from datetime import datetime
from kivymd.uix.list import OneLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from oauth2client.service_account import ServiceAccountCredentials
from SRDC_GSM import GlobalScreenManager, GSM

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class SelectionScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.delayedInit,0.1)
        self.ids.toggleAllBtn.text = "Select All"


    def delayedInit(self, dt):
        self.ExcelList = pd.read_excel("C:/VS_Code/Python/Kivy_Testing/SRDCPasswords.xlsx")

        self.ids.familyName.text = GlobalScreenManager.FAMILY_NAME
        self.ids.familyPassword.text = GlobalScreenManager.FAMILY_PASSWORD

        self.showOptions()

    def showOptions(self):
        container = self.ids.familyList
        container.clear_widgets()
        tempFirstNames = []
        self.checkboxes = []

        # Create simlified list of first names
        for _, row in self.ExcelList.iterrows():
            tempLName = str(row["LastName"]).strip().lower()
            if tempLName.lower() == GlobalScreenManager.FAMILY_NAME.lower():
                firstName = str(row["FirstName"]).strip()
                tempFirstNames.append(str(firstName))
                self.selectedCamper = row
                item = OneLineAvatarIconListItem(text=firstName)
                checkbox = RightCheckbox()
                item.add_widget(checkbox)
                container.add_widget(item)
                self.checkboxes.append((firstName,checkbox))

    def selectAll(self):
        anyUnchecked = any(not cb.active for _, cb in self.checkboxes)
        for _, cb, in self.checkboxes:
            cb.active = anyUnchecked

        if anyUnchecked:
                self.ids.toggleAllBtn.text = "Deselect All"
        else:
            self.ids.toggleAllBtn.text = "Select All"
                
    # # Push Name&Password to GoogleDoc
    def addToList(self):
        if self.selectedCamper is not None:
            timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            # Google Sheets API setup
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("C:\VS_Code\Python\Kivy_Testing\creds.json", scope)
            client = gspread.authorize(creds)

            # Open the spreadsheet and sheet
            sheet = client.open("SignedOutCampers").worksheet("Campers")

            for name, checkbox in self.checkboxes:
                if checkbox.active:
                    match = self.ExcelList[
                        (self.ExcelList["LastName"].str.strip().str.lower() == GlobalScreenManager.FAMILY_NAME.lower()) &
                        (self.ExcelList["FirstName"].str.strip() == name)
                    ]

                    if not match.empty:
                        row = match.iloc[0]
                        sheet.append_row([
                            str(row["FirstName"]),
                            str(row["LastName"]),
                            str(row["Passwords"]),
                            timestamp
                        ])

        GSM().switchScreen("EOD")
