############################################################################
#
#       - File: SRDC_UpdatePwdList.py
#       - Author: Dylan Hendrix
#       - Discription: Pulls data from excel sheet generated by Campwise
#                       into password sheet on google drive
#
############################################################################


import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def main():
    directory_path = "C:\VS_Code\Python\Kivy_Testing\OtherStuff"  # Update with your directory path
    newest_file = get_newest_file(directory_path)

    excelPath = os.path.join(directory_path, newest_file)

    pattern = r"[^a-zA-Z0-9\s]"

    # Open Excel file
    print("Getting Excel List...")
    excelSheet = pd.read_excel(excelPath)
    lastNames = excelSheet.iloc[:,[0,1,2]]

    print("Filtering values...")
    lastNames['combined'] = lastNames.apply(lambda row: ' '.join(row.astype(str)).strip(), axis=1)

########################## Uncomment to see skiped rows ############################
    # rows_to_skip = lastNames[lastNames['combined'].str.contains(pattern)]
    # print("Rows that will be removed:")
    # print(rows_to_skip)
####################################################################################

    # Delete Bad Values
    lastNames_cleaned = lastNames[~lastNames['combined'].str.contains(pattern)]
    lastNames_cleaned = lastNames_cleaned.drop(columns=['combined'])

    headers = lastNames_cleaned.columns.tolist()
    package = [headers] + lastNames_cleaned.values.tolist()

    # Authorize/Connect to google sheet
    print("Accessing Google Sheet...")
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
    creds_path = os.getenv("SRDC_CREDS_PATH")

    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope) if creds_path else print("Google credentials path is not set")
    client = gspread.authorize(creds)

    # Open the sheet & push the new data
    DB = client.open("SRDC_DB")
    passwordSheet = DB.worksheet("Passwords")

    print("Google sheet Authorized. Inserting values...")
    numRows = len(lastNames_cleaned) + 1           # +1 to account for header row
    numCols = len(lastNames_cleaned.iloc[0])
    blockToUpdate = f"A1:{chr(64 + numCols)}{numRows}"

    passwordSheet.clear()
    passwordSheet.update(package, blockToUpdate)

    print("\n============== Passwords Updated In Google Sheet ==============\n")

def get_newest_file(directory_path):

    files = os.listdir(directory_path)

    # Get the full file path and their last modified time
    files_with_timestamp = [
        (file, os.path.getmtime(os.path.join(directory_path, file))) for file in files
        if os.path.isfile(os.path.join(directory_path, file))  # Only consider files
    ]
    
    # Find the file with the most recent timestamp
    newest_file = max(files_with_timestamp, key=lambda x: x[1])
    
    return newest_file[0]

if __name__ == "__main__":
    main()
