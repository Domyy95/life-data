import gspread
import pprint
from oauth2client.service_account import ServiceAccountCredentials

last_entry_file_path = ".last_entry.txt"

# To change every year
data_file_name = "2026"
year_offset = -2

# Daily - Data sheet
daily_data_sheet = "Daily - Data"
daily_data_start_col = "B"
daily_data_end_col = "M"
# name: coloumn on sheet, type of data, when to ask (default daily)
daily_data = {
    "Sleep start": ["B", "hour"],
    "Awake": ["C", "hour"],
    "Read before sleep": ["D", "time"],
    "Out Home": ["E", "check"],
    "Energy": ["F", "float"],
    "Stress": ["G", "float"],
    "Happiness": ["H", "float"],
    "Achievement": ["I", "float"],
    "Notes": ["J", "str"],
    "Something new?": ["K", "str"],
    "First food": ["L", "time"],
    "Last food": ["M", "time"],
}

# Weekly - Actions sheet
# Asked only once a week
weekly_actions_sheet = "Weekly - Actions"
weekly_asked_day = 7  # Sunday
weekly_data_start_col = "N"
weekly_data_end_col = "P"
weekly_data = {
    "Week Notes": ["N", "str"],
    "Week Vote": ["O", "int"],
    "Weight": ["P", "float"],
}

# Daily - Actions sheet + Daily activities sheet
daily_actions_sheet = "Daily - Actions"
daily_sub_activities_sheet = "Daily - subActions"

# name: coloumn on sheet, type of data, categories if presents
daily_actions_data = {
    # Recupero
    "Sleep": ["time"],
    # Baseline della vita (mangiare, lavarsi, spostamenti, ecc.)
    "Operations": ["time"],
    # Crescita personale
    "Personal Growth": [
        "time",
        {
            "Reading": 15,
            "Planning": 16,
            "Writing": 17,
            "Meditation": 18,
            "Courses / Webinar": 19,
            "Other": 21,
        },
    ],
    # Lavoro retribuito
    "Work": [
        "time",
        {
            "JobToMe": 48,
            "Freelance": 49,
            "Other": 53,
        },
    ],
    # Corpo e movimento
    "Sport": [
        "time",
        {
            "Run": 3,
            "Workout": 4,
            "Hiking": 5,
            "Yoga": 6,
            "Bike": 7,
            "Other": 9,
        },
    ],
    # Costruzione e responsabilità personali
    "Side Projects": [
        "time",
        {
            "Blog": 26,
            "Home": 27,
            "Family Support": 28,
            "GAE": 29,
            "Coding / CTF": 30,
            "3D printing": 31,
            "Other": 32,
        },
    ],
    # Relazioni (intenzionali e casual)
    "Relationships": [
        "time",
        {
            "Martina": 58,
            "Friends": 59,
            "Family": 60,
            "Other": 63,
        },
    ],
    # Svago / consumo
    "Fun": [
        "time",
        {
            "YouTube": 37,
            "Board Games": 38,
            "Movies": 39,
            "Gaming": 40,
            "Trips": 41,
            "Other": 43,
        },
    ],
    "Phone": ["time"],
}

daily_actions_start_end_sheet = ["B", "J"]
day_actions_order = [
    "Personal Growth",
    "Work",
    "Side Projects",
    "Sport",
    "Fun",
    "Relationships",
    "Operations",
    "Phone",
    "Sleep",
]
activities_with_sub = ["Personal Growth", "Work", "Side Projects", "Fun", "Sport", "Relationships"]

data_for_check = [
    "Personal Growth",
    "Work",
    "Relationships",
    "Sport",
    "Side Projects",
    "Fun",
    "Phone",
    "Operations",
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
    file_name = "../secret/client_key.json"
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
