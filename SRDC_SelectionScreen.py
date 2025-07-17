import gspread
from kivymd.app import MDApp
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
        self.data = MDApp.get_running_app().sheetData

        self.ids.familyName.text = GlobalScreenManager.FAMILY_NAME
        self.ids.familyPassword.text = GlobalScreenManager.FAMILY_PASSWORD

        self.showOptions()

    def showOptions(self):
        container = self.ids.familyList
        container.clear_widgets()
        self.checkboxes = []

        # Create simlified list of first names
        for row in self.data:
            tempLName = str(row.get("LastName", "")).strip().lower()
            if tempLName.lower() == GlobalScreenManager.FAMILY_NAME.lower():
                firstName = str(row.get("FirstName", "")).strip()
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
                
    # Push Name&Password to GoogleDoc
    def addToList(self):
        if self.selectedCamper is not None:
            timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

            # Google Sheets API setup
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("C:\VS_Code\Python\Kivy_Testing\SRDC_Creds.json", scope)
            client = gspread.authorize(creds)

            # Open the spreadsheet and sheet
            sheet = client.open("SRDC_DB").worksheet("EndOfDay")

            for name, checkbox in self.checkboxes:
                if checkbox.active:
                    for row in self.data:
                        if (row.get("LastName", "").strip().lower() == GlobalScreenManager.FAMILY_NAME.lower() and
                            row.get("FirstName", "").strip() == name):
                            sheet.append_row([
                                str(row.get("FirstName", "")),
                                str(row.get("LastName", "")),
                                str(row.get("Passwords", "")),
                                timestamp
                            ])
                            break

        GSM().switchScreen("EOD")
