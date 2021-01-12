import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials

data_file_name = '2021_action_activity'
# Daily - Data sheet
daily_data_sheet = 'Daily - Data'
daily_data = ['sleep start', 'awake', 'morning workout', 'meditation', 'affirmation visualization', 'read night before', 'brush teeth', 'happiness', 'vote']
daily_data_positions = ['B', 'C', 'D', 'E', 'F', 'H', 'happiness', 'vote']
once_a_week_data = {'sunday': 'weight'}
once_a_week_positions = ['I']

# Daily - Actions sheet
daily_actions_sheet = 'Daily - Actions'
daily_actions_data = ['sleep', 'work', 'learning', 'side projects', 'sport', 'fun', 'phone', 'notes']
daily_actions_positions = []

# Weekly activities sheet
weekly_activities_sheet = 'Weekly Activities'
weekly_activities_data = {'learning': ['reading', 'english', 'gcp certifications', 'other'],
                     'side projects': ['website', '3d Printing', 'other'],
                     'sport': ['run', 'football', 'hiking', 'tennis', 'yoga', 'other'],
                     'fun': ['movies', 'martina', 'football', 'go out', 'chess', 'Trips']}
weekly_activities_positions = []



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
