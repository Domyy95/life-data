import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials

data_file_name = '2021_action_activity'
# Daily - Data sheet
daily_data_sheet = 'Daily - Data'
daily_data_start_l = 'B'
# name: coloumn on sheet, type of data, when to ask (default daily)
daily_data = {'Sleep start': ['B', 'hour'],
              'Awake': ['C', 'hour'],
              'Morning workout': ['D', 'time'],
              'Meditation&Affirmation&Visualization': ['E', 'time'],
              'Writing': ['F', 'time'],
              'Read night before': ['G', 'time'],
              'Brush teeth': ['H', 'int'],
              'Happiness': ['I', 'int'],
              'Vote': ['J', 'int'],
              'Weight': ['K', 'float', [7]]
              }

# Daily - Actions sheet + Weekly activities sheet
daily_actions_sheet = 'Daily - Actions'
weekly_activities_sheet = 'Weekly - Activities'
# name: coloumn on sheet, type of data, categories if presents
weekly_activities_start_end_sheet = ['B', 'L']
weekly_activities_order = ['Work', 'Operations', 'Learning', 'Side projects', 'Sport', 'Fun', 'Talking', 'My Tasks', 'Family Tasks', 'Phone', 'Sleep']
weekly_activities_not_in_row = ['Notes']
weekly_activities_with_sub = ['Work', 'Learning', 'Side projects', 'Fun', 'Sport']
daily_actions_data = {'Sleep': ['L', 'time'],
                      'Work': ['B', 'time', {'Reply': 48, 'Ripetizioni': 49, 'Applications / Colloqui': 50, 'Other': 53}],
                      'Learning': ['D', 'time', {'reading': 14, 'english': 15, 'GCP certifications': 16, 'Webinar / Courses': 17, 'Data Science': 18, 'Other': 19}],
                      'Sport': ['F', 'time', {'Run': 2, 'Football': 3, 'Hiking': 4, 'Tennis': 5, 'Yoga': 6, 'Other': 8}],
                      'Side projects': ['E', 'time', {'YouTube': 24, '3d Printing': 25, 'Challenges': 26, 'Other': 29}],
                      'Fun': ['G', 'time', {'Martina': 34, 'Movies': 35, 'Football': 36, 'Go out': 37, 'Trips': 38, 'Chess': 39, 'Board games': 40, 'YouTube':41, 'Other': 43}],
                      'Talking': ['8', 'time'],
                      'Phone': ['K', 'time'],
                      'Operations': ['C', 'time'],
                      'My Tasks': ['I', 'time'],
                      'Family Tasks': ['J', 'time'],
                      'Notes': ['N', 'str'],
                      }

data_for_check = ['Work', 'Learning', 'Sport', 'Side projects', 'Fun', 'Talking', 'Phone', 'Operations', 'Morning workout', 'Meditation&Affirmation&Visualization', 'Writing', 'My Tasks', 'Family Tasks']
hour_format = ' '
yes_check_type = ['x', 'y', 'yes']
check_type = ['no', 'nope'] + yes_check_type

from_n_to_letter = {
    '2': 'B',
    '3': 'C',
    '4': 'D',
    '5': 'E',
    '6': 'F',
    '7': 'G',
    '8': 'H',
    '9': 'I',
    '10': 'J',
    '11': 'K',
    '12': 'L',
    '13': 'M',
    '14': 'N',
    '15': 'O',
    '16': 'P',
    '17': 'Q',
    '18': 'R',
    '19': 'S',
    '20': 'T',
    '21': 'U',
    '22': 'V',
    '23': 'W',
    '24': 'X',
    '25': 'Y',
    '26': 'Z',
    '27': 'AA',
    '28': 'AB',
    '29': 'AC',
    '30': 'AD',
    '31': 'AE',
    '32': 'AF',
    '33': 'AG',
    '34': 'AH',
    '35': 'AI',
    '36': 'AJ',
    '37': 'AK',
    '38': 'AL',
    '39': 'AM',
    '40': 'AN',
    '41': 'AO',
    '42': 'AP',
    '43': 'AQ',
    '44': 'AR',
    '45': 'AS',
    '46': 'AT',
    '47': 'AU',
    '48': 'AV',
    '49': 'AW',
    '50': 'AX',
    '51': 'AY',
    '52': 'AZ'
}

confirm_data = 99
margin = ' = = = = =  = = = = =  = = = = =  = = = = =  = = = = =  = = = = = = = =  '
title1 = ' = = = = =  = = = = =  Daily Data     = = = = =  = = = = =  '
title2 = ' = = = = =  = = = = =  Daily Actions  = = = = =  = = = = =  '
margin2 = ' = = = = =  = = = = = '
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
