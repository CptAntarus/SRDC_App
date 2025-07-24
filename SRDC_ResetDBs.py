import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

def main():
    scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/drive"
            ]
            # creds = ServiceAccountCredentials.from_json_keyfile_name("C:\VS_Code\Python\Kivy_Testing\SRDC_Creds.json", scope)
    creds_path = os.getenv("SRDC_CREDS_PATH")

    if creds_path:
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    else:
        print("Google credentials path is not set!")
    client = gspread.authorize(creds)

    
    print("Cleaning End Of Day Log...")
    sheet = client.open("SRDC_DB").worksheet("EndOfDayLog")
    header = sheet.row_values(1) # Save the headers
    sheet.clear()                # Clear the DB
    sheet.insert_row(header, 1)  # Replace the headers

    print("Cleaning Extended Care Morning Log...")
    sheet = client.open("SRDC_DB").worksheet("ExtCareMorningLog")
    header = sheet.row_values(1) # Save the headers
    sheet.clear()                # Clear the DB
    sheet.insert_row(header, 1)  # Replace the headers

    print("Cleaning Extended Care AfternoonIn Logs...")
    sheet = client.open("SRDC_DB").worksheet("ExtCareAfternoonIn")
    header = sheet.row_values(1) # Save the headers
    sheet.clear()                # Clear the DB
    sheet.insert_row(header, 1)  # Replace the headers
    
    print("Cleaning Extended Care AfternoonOut Logs...")
    sheet = client.open("SRDC_DB").worksheet("ExtCareAfternoonOut")
    header = sheet.row_values(1) # Save the headers
    sheet.clear()                # Clear the DB
    sheet.insert_row(header, 1)  # Replace the headers

    print("============== Database Clean ==============")

if __name__ == "__main__":
    main()