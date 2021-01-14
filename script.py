from settings import *
import datetime
import gspread

today = datetime.datetime.today()
day_of_the_year = datetime.datetime.now().timetuple().tm_yday
week_day = today.isoweekday()
daily_data_x = day_of_the_year - 8
daily_actions_x = day_of_the_year - 8
weekly_activities_y = today.isocalendar()[1]

def main():
    # sheet = google_api_auth()
    print(margin)
    #daily_data_r = read_daily_data()
    daily_action_r = read_daily_actions()

def read_daily_data():
    print(title1)
    result = {}
    for data in daily_data:
        if len(daily_data[data]) == 2 or week_day in daily_data[data][2]:
            next = True
            while next:
                print(f'{data}: ')
                readed_data = input()
                next = verify_data(daily_data[data][1], readed_data)

            result[data] = readed_data

    print(margin)

    return result

def read_daily_actions():
    print(title2)
    result = {}
    for data in daily_actions_data:
            next = True
            while next:
                print(f'{data}: ')
                readed_data = input()
                next = verify_data(daily_actions_data[data][1], readed_data)

            result[data] = readed_data

            if len(daily_actions_data[data]) == 3:
                readed_sub_data = read_sub_data(data)
                result[data] = [readed_data, readed_sub_data]

    return result

def read_sub_data(data):
    next = True
    while next:
        print(ask_sub_data)
        tmp_sub = []
        for n, option in enumerate(daily_actions_data[data][2]):
            print(f'- {option} ({n})')
            tmp_sub.append(option)

        sub_cat = input()
        if int(sub_cat) < n:
            option = tmp_sub[int(sub_cat)]
            print('Time: ')
            sub_data = input()
            maybe_next = verify_data(daily_actions_data[data][1], sub_data)
            if not maybe_next:
                readed_sub_data[option] = sub_data
                hours = readed_sub_data.values()
                next = maybe_next and verify_sub_hours(result[data], hours)



print(margin)

def verify_sub_hours(total, hours):
    print(total, hours)
    tot_datetime = datetime.time(total.split(hour_format)[0], total.split(hour_format)[1])
    tot_hours = datetime.time(0 , 0)
    for h in hours:
        tot_hours += datetime.timedelta(hours=h.split(hour_format)[0]) + datetime.timedelta(minutes=h.split(hour_format)[1])

    if tot_datetime == tot_hours:
        return True
    else:
        return False


def verify_data(type, data):
    result = False
    if type == 'hour':
        tmp = data.split(hour_format)
        if len(tmp) < 2 or int(tmp[1]) > 59:
            result = True

    if type == 'time':
        tmp = data.split(hour_format)
        if (len(tmp) < 2 and data != '0') or int(tmp[1]) > 59:
            result = True

    elif type == 'int':
        try:
            int(data)
        except ValueError:
            result = True

    elif type == 'check':
        if data.lower() not in check_type:
            result = True

    elif type == 'str':
      pass

    return result

if __name__ == "__main__":
    main()
