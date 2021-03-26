from settings import *
import datetime
import gspread

today = datetime.datetime.today()
today = datetime.datetime.today() - datetime.timedelta(days=1) if today.hour < 6 else today
day_of_the_year = datetime.datetime.now().timetuple().tm_yday
day_of_the_year = day_of_the_year - 1 if today.hour < 8 else day_of_the_year
week_day = today.isoweekday()
daily_data_y = day_of_the_year - 8
weekly_activities_x = today.isocalendar()[1]

def main():
    print(margin)
    print(margin2 + f' {today.date()} ' + margin2)
    clean_daily_data()
    daily_data_r = read_daily_data()
    daily_action_r = read_daily_actions()
    all_data = {**daily_data_r, **daily_action_r}
    data_review(all_data)
    upload_data(all_data)
    print(margin)

def upload_data(all_data):
    sheet = google_api_auth()

    # Daily data
    to_upload = []
    end_l = daily_data_start_l
    for d in daily_data:
        if isinstance(all_data[d], datetime.datetime):
            to_upload.append(all_data[d].strftime('%H:%M'))
        else:
            to_upload.append(all_data[d])

        end_l = daily_data[d][0]

    to_upload = [to_upload]

    worksheet = sheet.worksheet(daily_data_sheet)
    worksheet.update(f'{daily_data_start_l}{daily_data_y}:{end_l}{daily_data_y}', to_upload, value_input_option="USER_ENTERED")

    # Weekly actions
    to_upload = []

    for d in weekly_activities_order:
        if isinstance(all_data[d], datetime.datetime):
            to_upload.append(all_data[d].strftime('%H:%M'))
        elif isinstance(all_data[d], list):
            to_upload.append(all_data[d][0].strftime('%H:%M'))
        else:
            to_upload.append(all_data[d])

    to_upload = [to_upload]

    worksheet = sheet.worksheet(daily_actions_sheet)
    worksheet.update(f'{weekly_activities_start_end_sheet[0]}{daily_data_y}:{weekly_activities_start_end_sheet[1]}{daily_data_y}', to_upload, value_input_option="USER_ENTERED")

    for d in weekly_activities_not_in_row:
        to_upload = all_data[d]
        worksheet.update(f'{daily_actions_data[d][0]}{daily_data_y}', to_upload, value_input_option="USER_ENTERED")

    # Weekly activities
    worksheet = sheet.worksheet(weekly_activities_sheet)
    for d in weekly_activities_with_sub:
        if isinstance(all_data[d], list):
            to_upload_rows = all_data[d][1]
            for to_upload_name in to_upload_rows:
                old_data = worksheet.cell(int(daily_actions_data[d][2][to_upload_name]), int(weekly_activities_x)).value.split(':')
                h = int(old_data[0])
                m = int(old_data[1]) if len(old_data) >= 2 else 0
                to_upload = all_data[d][1][to_upload_name]
                h += int(to_upload.hour)
                m += int(to_upload.minute)
                if m >= 60:
                    h += 1
                    m -= 60
                to_upload = f'{h}:{m}'
                worksheet.update(f'{from_n_to_letter[str(weekly_activities_x)]}{daily_actions_data[d][2][to_upload_name]}', to_upload, value_input_option="USER_ENTERED")

def data_review(data):
    number_to_ref = {n:d for n,d in enumerate(data)}
    final_version = True
    while final_version:
        print_all_data(data)
        check_total_time(data)
        print(f'Do you want to change something? [Confirm Data {confirm_data}]')
        answer = input()
        if 0 < int(answer) < len(list(data)):
            modify_data(data, number_to_ref[int(answer)])
        elif int(answer) == confirm_data:
            final_version = False

def check_total_time(data):
    should_be = datetime.datetime.combine(datetime.date(1, 1, 2), datetime.time(today.hour, today.minute))
    inserted = datetime.datetime.combine(datetime.date(1, 1, 1), datetime.time(data['Awake'].hour, data['Awake'].minute))
    for d in data:
        if d in data_for_check:
            if not isinstance(data[d], datetime.datetime):
                h = data[d][0].hour
                m = data[d][0].minute
                inserted = inserted + datetime.timedelta(hours=h) + datetime.timedelta(minutes=m)
            else:
                h = data[d].hour
                m = data[d].minute
                inserted = inserted + datetime.timedelta(hours=h) + datetime.timedelta(minutes=m)

    print(f'Computed h {inserted.hour}:{inserted.minute}, it should be {should_be.hour}:{should_be.minute}')

def modify_data(data, ref):
    next = True
    if isinstance(data[ref], datetime.datetime) or not isinstance(data[ref], list):
        while next:
            print('New Data: ')
            new_d = input()
            new_d, next = verify_data(daily_actions_data[ref][1] if ref in daily_actions_data else daily_data[ref][1], new_d)

        data[ref] = new_d

    else:
        while next:
            print('New Data: ')
            new_d = input()
            new_d, next = verify_data(daily_actions_data[ref][1] if ref in daily_actions_data else daily_data[ref][1], new_d)

        readed_sub_data = read_sub_data(ref, new_d)
        data[ref] = [new_d, readed_sub_data]

def print_all_data(data):
    print('These are the data inserted:')
    for n, d in enumerate(data):
        if isinstance(data[d], datetime.datetime):
            print(f'({n}) {d} - {data[d].hour}:{data[d].minute}')

        elif isinstance(data[d], list):
            print(f'({n}) {d} - {data[d][0].hour}:{data[d][0].minute}')
            for sub in data[d][1]:
                print(f'   - {sub}: {data[d][1][sub].hour}:{data[d][1][sub].minute}')

        else:
            print(f'({n}) {d} - {data[d]}')


def read_daily_data():
    print(title1)
    result = {}
    for data in daily_data:
        next = True
        while next:
            print(f'{data}: ')
            readed_data = input()
            readed_data, next = verify_data(daily_data[data][1], readed_data)

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
                readed_data, next = verify_data(daily_actions_data[data][1], readed_data)

            result[data] = readed_data

            if len(daily_actions_data[data]) == 3 and (readed_data.hour != 0 or readed_data.minute != 0):
                readed_sub_data = read_sub_data(data, readed_data)
                result[data] = [readed_data, readed_sub_data]

    return result

def read_sub_data(data, time):
    next = True
    result = {}
    while next:
        option = choose_option(data, result)
        print('Time: ')
        sub_data = input()
        sub_data, maybe_next = verify_data(daily_actions_data[data][1], sub_data)
        maybe_next = maybe_next or sub_data == '0'
        if not maybe_next:
            ver_sub_hours = verify_sub_hours(time, list(result.values()), sub_data)
            if ver_sub_hours == 0:
                result[option] = sub_data
                next = False
            elif ver_sub_hours == 1:
                print('Too much, are you sure about the data inserted?')
            else:
                result[option] = sub_data
                print('Time Missing, other actions?')

    return result

def choose_option(data, choosen):
    print(ask_sub_data)
    tmp_sub = []
    ok = True
    while ok:
        for n, option in enumerate(daily_actions_data[data][2]):
            print(f'- {option} ({n})')
            tmp_sub.append(option)

        sub_cat = int(input())
        if sub_cat <= n:
            if tmp_sub[sub_cat] not in choosen:
                ok = False

    return tmp_sub[sub_cat]


def verify_sub_hours(total, hours, new_hour):
    tot_datetime = datetime.datetime.combine(datetime.date(1, 1, 1), datetime.time(total.hour, total.minute))
    tot_hours = datetime.datetime.combine(datetime.date(1, 1, 1), datetime.time(0, 0))
    for h in hours:
        tot_hours += datetime.timedelta(hours=int(h.hour)) + datetime.timedelta(minutes=int(h.minute))

    tot_hours = tot_hours + datetime.timedelta(hours=int(new_hour.hour)) + datetime.timedelta(minutes=int(new_hour.minute))

    if tot_datetime == tot_hours:
        return 0
    elif tot_datetime < tot_hours:
        return 1
    else:
        return -1

def verify_data(type, data):
    result = False
    data_new = data
    if type == 'hour':
        tmp = data.split(hour_format)
        if (len(tmp) < 2):
            result = True
        if len(tmp) == 2:
            if int(tmp[1]) > 59:
                result = True

        if not result:
            data_new = datetime.datetime.strptime(data, '%H %M')

    if type == 'time':
        tmp = data.split(hour_format)
        if len(tmp) < 2:
            data = data + ' 0'
        if len(tmp) == 2:
            if int(tmp[1]) > 59:
                result = True

        if not result:
            data_new = datetime.datetime.strptime(data, '%H %M')

    elif type == 'int':
        try:
            int(data)
        except ValueError:
            result = True

    elif type == 'check':
        if data.lower() not in check_type:
            result = True
        elif data.lower() in yes_check_type:
            data_new = 'X'
        else:
            data_new = ' '

    elif type == 'str':
      pass

    if result == True:
        print('Data not correct, reinsert pls')

    return data_new, result

def clean_daily_data():
    to_delete = []
    for d in daily_data:
        if len(daily_data[d]) == 3:
            if week_day not in daily_data[d][2]:
                to_delete.append(d)

    for d in to_delete:
        del daily_data[d]

if __name__ == "__main__":
    main()
