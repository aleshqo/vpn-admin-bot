import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    json_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
    client = gspread.authorize(creds)

    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    sheet_name = os.getenv("SHEET_NAME")
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
    return sheet
