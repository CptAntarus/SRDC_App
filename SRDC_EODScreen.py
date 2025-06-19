import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from datetime import datetime



class EODScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # self.passwords = pd.read_excel("SRDCPasswords.xlsx")
        self.passwords = pd.read_excel("C:/VS_Code/Python/Kivy_Testing/SRDCPasswords.xlsx")
        self.selectedCamper = None

    # Shows Output Based on search input
    def showData(self):
        userInput = self.ids.nameInput.text.strip().lower()
        output_string = 'Name Not Found'

        if userInput == "":
            output_string = 'No Name Entered'
            closeButton = MDFlatButton(text='Close', on_release=self.closeDialog)
            self.dialog = MDDialog(title='Password:',text=output_string,
                            buttons=[closeButton])

        else:
            for index, row in self.passwords.iterrows():
                if str(row['LastNames']).strip().lower() == userInput:
                    output_string = str(row['Passwords'])
                    self.selectedCamper=row

                    closeButton = MDFlatButton(text='Close', on_release=self.closeDialog)
                    addToList_button = MDFlatButton(text='Add', on_release=self.addToList)
                    self.dialog = MDDialog(title='Password:',text=output_string,
                            buttons=[closeButton, addToList_button])
                    break
                else:
                    closeButton = MDFlatButton(text='Close', on_release=self.closeDialog)
                    self.dialog = MDDialog(title='Password:',text=output_string,
                            buttons=[closeButton])
        
        self.dialog.open()
        self.ids.nameInput.text = ''

    # Closes Dialog box
    def closeDialog(self, obj):
        self.dialog.dismiss()

    # Push Name&Password to GoogleDoc
    def addToList(self, obj):
        if self.selectedCamper is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Google Sheets API setup
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("C:\VS_Code\Python\Kivy_Testing\creds.json", scope)
            client = gspread.authorize(creds)

            # Open the spreadsheet and sheet
            sheet = client.open("SignedOutCampers").worksheet("Campers")

            # Append the data
            sheet.append_row([
                str(self.selectedCamper['LastNames']),
                str(self.selectedCamper['Passwords']),
                timestamp
            ])

        self.dialog.dismiss()