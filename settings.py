import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials

data_file_name = '2021_action_activity'
# Daily - Data sheet
daily_data_sheet = 'Daily - Data'
# name: coloumn on sheet, type of data, when to ask (default daily)
daily_data = {'Sleep start': ['B', 'hour'],
              'Awake': ['C', 'hour'],
              'Morning workout': ['D', 'time'],
              'Meditation': ['E', 'time'],
              'Affirmation&Visualization': ['F', 'time'],
              'Read night before': ['G', 'time'],
              'Brush teeth': ['H', 'check'],
              'Happiness': ['I', 'int'],
              'Vote': ['J', 'int'],
              'Weight': ['K', 'int', [7]]
              }

# Daily - Actions sheet + Weekly activities sheet
daily_actions_sheet = 'Daily - Actions'
weekly_activities_sheet = 'Weekly Activities'
# name: coloumn on sheet, type of data, categories if presents
daily_actions_data = {'Sleep': ['I', 'time'],
                      'Work': ['B', 'time'],
                      'Learning': ['D', 'time', {'reading': 13, 'english': 14, 'GCP certifications': 15}],
                      'Sport': ['F', 'time', {'Run': 2,'Football': 3,'Hiking': 4,'Tennis': 5, 'Yoga': 6, 'Other': 8}],
                      'Side projects': ['E', 'time', {'Website': 23, '3d Printing': 24, 'Other': 28}],
                      'Fun': ['G', 'time', {'Martina': 33,'Movies': 34,'Football': 35,'Go out': 36,'Trips': 37,'Chess': 38,'Board games': 39,'Other': 42}],
                      'Phone': ['H', 'time'],
                      'Operations': ['C', 'time'],
                      'Notes': ['K', 'str'],
                      }

hour_format = '.'
check_type = ['x', 'no', 'nope', 'y', 'yes']

margin = ' = = = = =  = = = = =  = = = = =  = = = = =  = = = = =  = = = = = = = =  = = = = = = = =  '
title1 = ' = = = = =  = = = = =  Daily Data     = = = = =  = = = = =  '
title2 = ' = = = = =  = = = = =  Daily Actions  = = = = =  = = = = =  '
ask_sub_data = 'In which category is this action?'

#Authorize the Google API and get gspead client
def google_api_auth():
    scope = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file'
        ]
    file_name = 'client_key.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
    client = gspread.authorize(creds)
    sheet = client.open(data_file_name)
    return sheet


def read_test(sheet):
    python_sheet = sheet.get_all_values()
    pp = pprint.PrettyPrinter()
    pp.pprint(python_sheet)
