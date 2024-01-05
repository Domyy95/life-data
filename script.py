from settings import *
import datetime

choosen_day = datetime.datetime.today()
day_of_the_year = choosen_day.timetuple().tm_yday
daily_data_y = day_of_the_year
week_day = choosen_day.isoweekday()
weekly_activities_x = choosen_day.isocalendar()[1]

sheet = google_api_auth()


def main():
    while True:
        print(margin)
        choose_day()
        print(margin2 + f" {choosen_day.date()} " + margin2)
        daily_data_r = read_daily_data()
        daily_action_r = read_daily_actions()
        weekly_data = read_weekly_data()
        all_data = {**daily_data_r, **daily_action_r, **weekly_data}
        data_review(all_data)
        upload_data(all_data)
        print(margin)

        if not repeat_question():
            break


def choose_day():
    global choosen_day
    global week_day
    global daily_data_y
    global day_of_the_year
    global weekly_activities_x
    choosen_day = datetime.datetime.today()

    while True:
        print("How many days ago do you want to go?")
        answer = int(input())
        answer, _ = verify_data("int", answer)

        tmp_day = choosen_day - datetime.timedelta(days=answer)
        print(f"Choosen day: {tmp_day.date()}. Ok? [y/n]")
        answer = input()
        if answer in yes_check_type:
            break

    choosen_day = tmp_day
    day_of_the_year = choosen_day.timetuple().tm_yday
    daily_data_y = day_of_the_year + year_offset
    week_day = choosen_day.isoweekday()
    weekly_activities_x = choosen_day.isocalendar()[1] + 1


def repeat_question():
    print("Do you want to insert another day?")
    answer = input()
    if answer in yes_check_type:
        return True
    else:
        return False


def worksheet_update(data, start, end=None, worksheet=None, worksheet_obj=None):
    """
    The function updates a worksheet with data starting from a specified cell.

    :param data: The data parameter is a list or a single data containing the data that you want to update in the worksheet

    :param start: The start parameter is used to specify the starting cell where the data should be
    updated in the worksheet. It can be specified as a string representing the cell address (e.g., "A1")
    or as a tuple of integers representing the row and column indices (e.g., (1, 1))

    :param end: The end parameter is used to specify the end cell of the range of data that needs to be
    updated in the worksheet. If the "end" parameter is not provided, the data will be updated starting
    from the "start" cell and continue until the last cell in the "data" list, or it will update a single cell.

    :param worksheet: The worksheet parameter is used to specify the name of the worksheet where the
    data will be updated. Only one between the "worksheet" and "worksheet_obj" parameters should be provided.

    :param worksheet_obj: The worksheet_obj parameter is an object that represents the worksheet where
    the data will be updated. It is used to access and modify the cells in the worksheet
    """
    try:
        worksheet = (
            sheet.worksheet(worksheet) if worksheet is not None else worksheet_obj
        )

        if end is None:
            worksheet.update(
                range_name=start,
                values=data,
                value_input_option="USER_ENTERED",
            )

        else:
            worksheet.update(
                range_name=f"{start}:{end}",
                values=[data],
                value_input_option="USER_ENTERED",
            )

    except Exception as e:
        print("Error updating worksheet {worksheet}:", e.to_string())


def upload_data(all_data):
    # Daily data
    to_upload = []
    for d in daily_data:
        if isinstance(all_data[d], datetime.datetime):
            to_upload.append(all_data[d].strftime("%H:%M"))
        else:
            to_upload.append(all_data[d])

    worksheet_update(
        data=to_upload,
        start=f"{daily_data_start_col}{daily_data_y}",
        end=f"{daily_data_end_col}{daily_data_y}",
        worksheet=daily_data_sheet,
    )

    # Daily actions
    to_upload = []

    for d in day_actions_order:
        if isinstance(all_data[d], datetime.datetime):
            to_upload.append(all_data[d].strftime("%H:%M"))
        elif isinstance(all_data[d], list):
            to_upload.append(all_data[d][0].strftime("%H:%M"))
        else:
            to_upload.append(all_data[d])

    worksheet_update(
        data=to_upload,
        start=f"{daily_actions_start_end_sheet[0]}{daily_data_y}",
        end=f"{daily_actions_start_end_sheet[1]}{daily_data_y}",
        worksheet=daily_actions_sheet,
    )

    # Weekly Data
    if any([x in all_data for x in weekly_data]):
        to_upload = [all_data[d] for d in weekly_data]

        worksheet_update(
            data=to_upload,
            start=f"{weekly_data_start_col}{str(weekly_activities_x)}",
            end=f"{weekly_data_end_col}{str(weekly_activities_x)}",
            worksheet=weekly_actions_sheet,
        )

    # Daily sub activities
    worksheet = sheet.worksheet(daily_sub_activities_sheet)
    for d in activities_with_sub:
        if isinstance(all_data[d], list):
            to_upload_rows = all_data[d][1]
            for to_upload_name in to_upload_rows:
                to_upload = all_data[d][1][to_upload_name]
                h = int(to_upload.hour)
                m = int(to_upload.minute)
                if m >= 60:
                    h += 1
                    m -= 60
                m = "00" if m == 0 else m
                to_upload = f"{h}:{m}"

                worksheet_update(
                    data=to_upload,
                    start=f"{base_10_to_alphabet(day_of_the_year - 1 + year_offset)}{daily_actions_data[d][2][to_upload_name]}",
                    worksheet_obj=worksheet,
                )


def data_review(data):
    number_to_ref = {n: d for n, d in enumerate(data)}
    while True:
        print_all_data(data)
        check_total_time(data)
        print(f"Do you want to change something? [Confirm Data {confirm_data}]")
        answer = input()
        if 0 < int(answer) < len(list(data)):
            modify_data(data, number_to_ref[int(answer)])
        elif int(answer) == confirm_data:
            break


def check_total_time(data):
    inserted = datetime.datetime.combine(
        datetime.date(1, 1, 1), datetime.time(data["Awake"].hour, data["Awake"].minute)
    )
    for d in data:
        if d in data_for_check:
            if not isinstance(data[d], datetime.datetime):
                h = data[d][0].hour
                m = data[d][0].minute
                inserted = (
                    inserted
                    + datetime.timedelta(hours=h)
                    + datetime.timedelta(minutes=m)
                )
            else:
                h = data[d].hour
                m = data[d].minute
                inserted = (
                    inserted
                    + datetime.timedelta(hours=h)
                    + datetime.timedelta(minutes=m)
                )

    print(f"Computed h {inserted.hour}:{inserted.minute}")


def modify_data(data, ref):
    next = True
    if isinstance(data[ref], datetime.datetime) or not isinstance(data[ref], list):
        while next:
            print("New Data: ")
            new_d = input()
            new_d, next = verify_data(
                daily_actions_data[ref][1]
                if ref in daily_actions_data
                else daily_data[ref][1],
                new_d,
            )

        data[ref] = new_d

    else:
        while next:
            print("New Data: ")
            new_d = input()
            new_d, next = verify_data(
                daily_actions_data[ref][1]
                if ref in daily_actions_data
                else daily_data[ref][1],
                new_d,
            )

        readed_sub_data = read_sub_data(ref, new_d)
        data[ref] = [new_d, readed_sub_data]


def print_all_data(data):
    print("These are the data inserted:")
    for n, d in enumerate(data):
        if isinstance(data[d], datetime.datetime):
            print(f"({n}) {d} - {data[d].hour}:{data[d].minute}")

        elif isinstance(data[d], list):
            print(f"({n}) {d} - {data[d][0].hour}:{data[d][0].minute}")
            for sub in data[d][1]:
                print(f"   - {sub}: {data[d][1][sub].hour}:{data[d][1][sub].minute}")

        else:
            print(f"({n}) {d} - {data[d]}")


def read_weekly_data():
    result = {}
    if week_day == weekly_asked_day:
        print(title3)
        for data in weekly_data:
            next = True
            while next:
                print(f"{data}: ")
                readed_data = input()
                readed_data, next = verify_data(weekly_data[data][1], readed_data)

            result[data] = readed_data

        print(margin)

    return result


def read_daily_data():
    print(title1)
    result = {}
    for data in daily_data:
        next = True
        while next:
            print(f"{data}: ")
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
            print(f"{data}: ")
            readed_data = input()
            readed_data, next = verify_data(daily_actions_data[data][1], readed_data)

        result[data] = readed_data

        if len(daily_actions_data[data]) == 3 and (
            readed_data.hour != 0 or readed_data.minute != 0
        ):
            readed_sub_data = read_sub_data(data, readed_data)
            result[data] = [readed_data, readed_sub_data]

    return result


def read_sub_data(data, time):
    next = True
    result = {}
    while next:
        option = choose_option(data, result)
        print("Time: ")
        sub_data = input()
        sub_data, maybe_next = verify_data(daily_actions_data[data][1], sub_data)
        maybe_next = maybe_next or sub_data == "0"
        if not maybe_next:
            ver_sub_hours = verify_sub_hours(time, list(result.values()), sub_data)
            if ver_sub_hours == 0:
                result[option] = sub_data
                next = False
            elif ver_sub_hours == 1:
                print("Too much, are you sure about the data inserted?")
            else:
                result[option] = sub_data
                print("Time Missing, other actions?")

    return result


def choose_option(data, choosen):
    print(ask_sub_data)
    tmp_sub = []
    ok = True
    while ok:
        for n, option in enumerate(daily_actions_data[data][2]):
            print(f"- {option} ({n})")
            tmp_sub.append(option)

        sub_cat = int(input())
        if sub_cat <= n:
            if tmp_sub[sub_cat] not in choosen:
                ok = False

    return tmp_sub[sub_cat]


def verify_sub_hours(total, hours, new_hour):
    tot_datetime = datetime.datetime.combine(
        datetime.date(1, 1, 1), datetime.time(total.hour, total.minute)
    )
    tot_hours = datetime.datetime.combine(datetime.date(1, 1, 1), datetime.time(0, 0))
    for h in hours:
        tot_hours += datetime.timedelta(hours=int(h.hour)) + datetime.timedelta(
            minutes=int(h.minute)
        )

    tot_hours = (
        tot_hours
        + datetime.timedelta(hours=int(new_hour.hour))
        + datetime.timedelta(minutes=int(new_hour.minute))
    )

    if tot_datetime == tot_hours:
        return 0
    elif tot_datetime < tot_hours:
        return 1
    else:
        return -1


def verify_data(type, data):
    result = False
    data_new = data
    if type == "hour":
        tmp = data.split(hour_format)
        if len(tmp) < 2:
            result = True
        if len(tmp) == 2:
            if int(tmp[1]) > 59:
                result = True

        if not result:
            data_new = datetime.datetime.strptime(data, "%H %M")

    if type == "time":
        tmp = data.split(hour_format)
        if len(tmp) < 2:
            data = data + " 0"
        if len(tmp) == 2:
            if int(tmp[1]) > 59:
                result = True

        if not result:
            data_new = datetime.datetime.strptime(data, "%H %M")

    elif type == "int":
        try:
            int(data)
        except ValueError:
            result = True

    elif type == "float":
        try:
            float(data)
        except ValueError:
            result = True

    elif type == "check":
        if data.lower() not in check_type:
            result = True
        elif data.lower() in yes_check_type:
            data_new = "X"
        else:
            data_new = " "

    elif type == "str":
        pass

    if result == True:
        print("Data not correct, reinsert pls")

    return data_new, result


A_UPPERCASE = ord("A")
ALPHABET_SIZE = 26


def _decompose(number):
    """Generate digits from `number` in base alphabet, least significants
    bits first.

    Since A is 1 rather than 0 in base alphabet, we are dealing with
    `number - 1` at each iteration to be able to extract the proper digits.
    """

    while number:
        number, remainder = divmod(number - 1, ALPHABET_SIZE)
        yield remainder


def base_10_to_alphabet(number):
    """Convert a decimal number to its base alphabet representation"""

    return "".join(chr(A_UPPERCASE + part) for part in _decompose(number))[::-1]


if __name__ == "__main__":
    main()
