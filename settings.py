import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials

# To change every year
data_file_name = "2024_action_activity"
year_offset = 2

# Daily - Data sheet
daily_data_sheet = "Daily - Data"
daily_data_start_col = "B"
daily_data_end_col = "M"
# name: coloumn on sheet, type of data, when to ask (default daily)
daily_data = {
    "Sleep start": ["B", "hour"],
    "Awake": ["C", "hour"],
    "Read before sleep": ["D", "time"],
    "Brush teeth": ["E", "int"],
    "Out Home": ["F", "check"],
    "Eat meet": ["G", "check"],
    "Happiness": ["H", "int"],
    "Vote": ["I", "int"],
    "Notes": ["J", "str"],
    "Something new?": ["K", "str"],
    "First food": ["L", "time"],
    "Last food": ["M", "time"],
}

# Weekly - Actions sheet
# Asked only once a week
weekly_actions_sheet = "Weekly - Actions"
weekly_asked_day = 7  # Sunday
weekly_data_start_col = "Q"
weekly_data_end_col = "T"
weekly_data = {
    "Week Notes": ["Q", "str"],
    "Week Retrospective": ["R", "str"],
    "Week Vote": ["S", "int"],
    "Weight": ["T", "float"],
}

# Daily - Actions sheet + Daily activities sheet
daily_actions_sheet = "Daily - Actions"
daily_sub_activities_sheet = "Daily - subActions"

# name: coloumn on sheet, type of data, categories if presents
daily_actions_data = {
    "Sleep": ["L", "time"],
    "Personal act": [
        "B",
        "time",
        {"Planning": 59, "Writing": 60, "Meditation": 61, "Other": 64},
    ],
    "Work": [
        "C",
        "time",
        {
            "JobToMe": 49,
            "Freelance": 50,
            "Other": 54,
        },
    ],
    "Learning": [
        "E",
        "time",
        {
            "reading": 15,
            "Webinar / Courses": 16,
            "CTF": 17,
            "Coding": 18,
            "English": 19,
            "Other": 20,
        },
    ],
    "Sport": [
        "F",
        "time",
        {
            "Run": 3,
            "Hiking": 4,
            "Yoga": 5,
            "Bike": 7,
            "Workout": 8,
            "Other": 9,
        },
    ],
    "Personal projects": [
        "F",
        "time",
        {
            "3d Printing": 25,
            "Home projects": 26,
            "Website - Blog": 27,
            "GAE": 28,
            "House": 29,
            "Other": 30,
        },
    ],
    "Fun": [
        "H",
        "time",
        {
            "Martina": 35,
            "YouTube": 36,
            "Friends time": 37,
            "Board games": 38,
            "Movies": 39,
            "Trips": 40,
            "Other": 44,
        },
    ],
    "Talking": ["I", "time"],
    "Phone": ["L", "time"],
    "Operations": ["D", "time"],
    "My Tasks": ["J", "time"],
    "Family Tasks": ["K", "time"],
}

daily_actions_start_end_sheet = ["B", "M"]
day_actions_order = [
    "Personal act",
    "Work",
    "Operations",
    "Learning",
    "Personal projects",
    "Sport",
    "Fun",
    "Talking",
    "My Tasks",
    "Family Tasks",
    "Phone",
    "Sleep",
]
activities_with_sub = [
    "Personal act",
    "Work",
    "Learning",
    "Personal projects",
    "Fun",
    "Sport",
]

data_for_check = [
    "Personal act",
    "Work",
    "Learning",
    "Sport",
    "Personal projects",
    "Fun",
    "Talking",
    "Phone",
    "Operations",
    "My Tasks",
    "Family Tasks",
    "Read before sleep",
]
hour_format = " "
yes_check_type = ["x", "y", "yes"]
check_type = ["no", "nope", "n"] + yes_check_type

from_n_to_letter = {
    "2": "B",
    "3": "C",
    "4": "D",
    "5": "E",
    "6": "F",
    "7": "G",
    "8": "H",
    "9": "I",
    "10": "J",
    "11": "K",
    "12": "L",
    "13": "M",
    "14": "N",
    "15": "O",
    "16": "P",
    "17": "Q",
    "18": "R",
    "19": "S",
    "20": "T",
    "21": "U",
    "22": "V",
    "23": "W",
    "24": "X",
    "25": "Y",
    "26": "Z",
    "27": "AA",
    "28": "AB",
    "29": "AC",
    "30": "AD",
    "31": "AE",
    "32": "AF",
    "33": "AG",
    "34": "AH",
    "35": "AI",
    "36": "AJ",
    "37": "AK",
    "38": "AL",
    "39": "AM",
    "40": "AN",
    "41": "AO",
    "42": "AP",
    "43": "AQ",
    "44": "AR",
    "45": "AS",
    "46": "AT",
    "47": "AU",
    "48": "AV",
    "49": "AW",
    "50": "AX",
    "51": "AY",
    "52": "AZ",
}

confirm_data = 99
margin = " = = = = =  = = = = =  = = = = =  = = = = =  = = = = =  = = = = = = = =  "
title1 = " = = = = =  = = = = =  Daily Data     = = = = =  = = = = =  "
title2 = " = = = = =  = = = = =  Daily Actions  = = = = =  = = = = =  "
title3 = " = = = = =  = = = = =  Weekly Data  = = = = =  = = = = =  "
margin2 = " = = = = =  = = = = = "
ask_sub_data = "In which category is this action?"


# Authorize the Google API and get gspead client
def google_api_auth():
    scope = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
    ]
    file_name = "client_key.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
    client = gspread.authorize(creds)
    sheet = client.open(data_file_name)
    return sheet


def read_test(sheet):
    python_sheet = sheet.get_all_values()
    pp = pprint.PrettyPrinter()
    pp.pprint(python_sheet)


# generate the strings for the formula
# string = "='Daily - Data'!$D{n}"

# for i in range(3, 372):
#     print(string.format(n=i))
