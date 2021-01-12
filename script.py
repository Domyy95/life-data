from settings import *
import datetime
import gspread

today = datetime.datetime.today()

def main():
    sheet = google_api_auth()
    read_daily_data()
    read_daily_actions()
    read_sunday_data()

def read_daily_data():
    return 0

def read_daily_actions():
    return 0

def read_sunday_data():
    return 0

if __name__ == "__main__":
    main()
