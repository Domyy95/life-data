import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials

data_file_name = '2022_action_activity'
# Daily - Data sheet
daily_data_sheet = 'Daily - Data'
daily_data_start_col = 'B'
daily_data_end_col = 'L'
# name: coloumn on sheet, type of data, when to ask (default daily)
daily_data = {'Sleep start': ['B', 'hour'],
              'Awake': ['C', 'hour'],
              'Morning workout': ['D', 'time'],
              'Read before sleep': ['E', 'time'],
              'Brush teeth': ['F', 'int'],
              'Out Home': ['G', 'check'],
              'Eat meet': ['H', 'check'],
              'Happiness': ['I', 'int'],
              'Vote': ['J', 'int'],
              'Notes': ['K', 'str'],
              'Something new?': ['L', 'str'],
              }

# Weekly - Actions sheet
# Asked only once a week
weekly_actions_sheet = 'Weekly - Actions'
weekly_asked_day = 7 # Sunday
weekly_data_start_col = 'AD'
weekly_data_end_col = 'AF'
weekly_data = {
    'Week Notes': ['AD', 'str'],
    'Week Vote': ['AE', 'int'],
    'Weight': ['AF', 'float']
}

# Daily - Actions sheet + Daily activities sheet
daily_actions_sheet = 'Daily - Actions'
daily_sub_activities_sheet = 'Daily - subActions'

# name: coloumn on sheet, type of data, categories if presents
daily_actions_data = {'Sleep': ['L', 'time'],
                      'Personal act': ['B', 'time', {'Planning': 59, 'Writing': 60, 'Meditation': 61, 'Other': 64}],
                      'Work': ['C', 'time', {'TuoTempo': 49, 'Works with IM': 50, 'Reply': 53, 'Other': 54}],
                      'Learning': ['E', 'time', {'reading': 15, 'Webinar / Courses': 16, 'Toblerone': 17, 'Challenges': 18, 'Data Science': 19, 'Other': 20}],
                      'Sport': ['F', 'time', {'Run': 3, 'Football': 4, 'Hiking': 5, 'Tennis': 6, 'Yoga': 7, 'Other': 9}],
                      'Personal projects': ['F', 'time', {'3d Printing': 25, 'MasterMind': 26, 'Other': 30}],
                      'Fun': ['H', 'time', {'Martina': 35, 'Movies': 36, 'Football': 37, 'Friends time': 38, 'Trips': 39, 'Chess': 40, 'Board games': 41, 'YouTube':42, 'Other': 44}],
                      'Talking': ['I', 'time'],
                      'Phone': ['L', 'time'],
                      'Operations': ['D', 'time'],
                      'My Tasks': ['J', 'time'],
                      'Family Tasks': ['K', 'time'],
                      }

daily_actions_start_end_sheet = ['B', 'M']
day_actions_order = ['Personal act','Work', 'Operations', 'Learning', 'Personal projects', 'Sport', 'Fun', 'Talking', 'My Tasks', 'Family Tasks', 'Phone', 'Sleep']
activities_with_sub = ['Personal act', 'Work', 'Learning', 'Personal projects', 'Fun', 'Sport']

data_for_check = ['Personal act','Work', 'Learning', 'Sport', 'Personal projects', 'Fun', 'Talking', 'Phone', 'Operations', 'Morning workout', 'Meditation&Affirmation&Visualization', 'Writing', 'My Tasks', 'Family Tasks','Read before sleep']
hour_format = ' '
yes_check_type = ['x', 'y', 'yes']
check_type = ['no', 'nope','n'] + yes_check_type

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
title3 = ' = = = = =  = = = = =  Weekly Data  = = = = =  = = = = =  '
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
