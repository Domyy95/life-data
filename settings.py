import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

#Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)

# Fetch the sheet Example
# sheet = client.open('2021_action_activity').sheet1
# python_sheet = sheet.get_all_records()
# pp = pprint.PrettyPrinter()
# pp.pprint(python_sheet)

#Update Cell
# cell = sheet.cell(3,3)
print('Cell Before Update: ', cell.value)
sheet.update_cell(3,3,'O MY FUCKING GOD')
cell = sheet.cell(3,3)
print('Cell After Update: ', cell.value)
