import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


def main():
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    creds_path = os.getenv("SRDC_CREDS_PATH")

    if creds_path:
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    else:
        print("Google credentials path is not set!")
    client = gspread.authorize(creds)

###################################################################
#   Save Current Time and Open Database
###################################################################
    time = datetime.now()
    timeStamp = time.strftime('%m/%d/%Y')
    DB = client.open("SRDC_DB")

###################################################################
#   Save data to History and Clear log
###################################################################
    LogSheets = ["EndOfDayLog", "ExtCareMorningLog", "ExtCareAfternoonIn", "ExtCareAfternoonOut"]
    HistSheets = ["EODHistory", "MorningHistory", "Afternoon_In_History", "Afternoon_Out_History"]

    for Log, Hist in zip(LogSheets, HistSheets):
        print(f"\n======== Begining copy for {Log} ========")
        logSheet = DB.worksheet(Log)
        historySheet = DB.worksheet(Hist)

        data = logSheet.get_all_values()
        startRow = len(historySheet.get_all_values()) + 2

        # Combine current date and Log data
        data_package = [[timeStamp]] + data

        # Calculate where to put the new data
        end_col = 'D'
        end_row = startRow + len(data_package) - 1
        cell_range = f"A{startRow}:{end_col}{end_row}"

        # Copy data over to history sheet
        print(f"Copying {Log} to {Hist}...")
        historySheet.update(data_package, cell_range)

        # Clear Logs
        print(f"Cleaning {Log}...")
        header = logSheet.row_values(1) # Save the headers
        logSheet.clear()                # Clear the DB
        logSheet.insert_row(header, 1)  # Replace the headers
        
        print(f"======== Done with {Log} ========\n")

    print("\n============== History Saved & Databases Cleaned ==============\n")

if __name__ == "__main__":
    main()