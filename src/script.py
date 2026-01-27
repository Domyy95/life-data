import os
from datetime import date, datetime, time, timedelta

import settings as st
from random_quotes import random_quote_and_book_notes
from random_tag import random_tag_note

yesterday = datetime.today() - timedelta(days=1)
chosen_day = datetime.today()
day_of_the_year = chosen_day.timetuple().tm_yday
daily_data_y = day_of_the_year
week_day = chosen_day.isoweekday()
weekly_activities_x = chosen_day.isocalendar()[1] - 2

sheet = st.google_api_auth()


def main():
    random_quote_and_book_notes()
    print(st.margin)
    choose_day()
    while True:
        print(st.margin2 + f" {chosen_day.date()} " + st.margin2)
        daily_data_r = read_daily_data()
        daily_action_r = read_daily_actions()
        weekly_data = read_weekly_data()
        all_data = {**daily_data_r, **daily_action_r, **weekly_data}
        data_review(all_data)
        upload_data(all_data)
        update_last_day_entry_file()
        print(st.margin)

        next_day = compute_next_day()
        if not next_day:
            print("All the days inserted! Bye!")
            print(st.margin)
            random_tag_note()
            break


def choose_day():
    global chosen_day, week_day, daily_data_y, day_of_the_year, weekly_activities_x

    if os.path.exists(st.last_entry_file_path):
        with open(st.last_entry_file_path, "r") as f:
            last_date_str = f.read().strip()
            try:
                last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                chosen_day = last_date + timedelta(days=1)
                print(f"Auto-selected day: {chosen_day.date()}")
                update_day_metadata()
            except ValueError:
                print(f"Invalid date format in {st.last_entry_file_path}, fallback to manual input")
                manual_choose_day()
                return
    else:
        manual_choose_day()
        return


def manual_choose_day():
    """
    Allows the user to manually select a day when automatic selection fails.

    This function is called by `choose_day()` as a fallback mechanism. It prompts
    the user to specify how many days ago they want to go, validates the input,
    and updates the global variables related to the chosen day.
    """
    global chosen_day, week_day, daily_data_y, day_of_the_year, weekly_activities_x
    chosen_day = datetime.today()

    while True:
        print("How many days ago do you want to go?")
        answer = input()
        answer, wrong = verify_data("int", answer)

        if not wrong:
            tmp_day = chosen_day - timedelta(days=answer)
            print(f"Chosen day: {tmp_day.date()}. Ok? [y/n]")
            answer = input()
            if answer in st.yes_check_type:
                chosen_day = tmp_day
                update_day_metadata()
                break


def update_day_metadata():
    """
    Updates global variables related to the currently chosen day.

    This function recalculates and updates the following global variables:
    - day_of_the_year: The day of the year for the chosen day.
    - daily_data_y: Adjusted day of the year with an offset.
    - week_day: The weekday number (1 for Monday, 7 for Sunday).
    - weekly_activities_x: The ISO calendar week number, incremented by 1.

    Call this function whenever the `chosen_day` variable is modified
    to ensure all related metadata is consistent.
    """
    global chosen_day, week_day, daily_data_y, day_of_the_year, weekly_activities_x
    day_of_the_year = chosen_day.timetuple().tm_yday
    daily_data_y = day_of_the_year + st.year_offset
    week_day = chosen_day.isoweekday()
    weekly_activities_x = chosen_day.isocalendar()[1] + 1


def update_last_day_entry_file():
    """
    Updates the last entry file with the last inserted date.

    This function writes the last inserted date in 'YYYY-MM-DD' format to the specified
    last entry file path. It is called after each successful data upload.
    """
    try:
        with open(st.last_entry_file_path, "w") as f:
            f.write(chosen_day.strftime("%Y-%m-%d"))
    except OSError as e:
        print(f"Error: Unable to write to file {st.last_entry_file_path}. {e}")
        # Optionally, you could log the error or take further action here.


def compute_next_day():
    global chosen_day, week_day, daily_data_y, day_of_the_year, weekly_activities_x

    if chosen_day.date() == yesterday.date():
        return False

    chosen_day = chosen_day + timedelta(days=1)
    update_day_metadata()
    return True


def worksheet_update(data: list, start: str, worksheet: str, end=None):
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
    data will be updated.
    """
    data = [data]
    try:
        worksheet = sheet.worksheet(worksheet)
        if end is None:
            worksheet.update(
                values=[data],
                range_name=start,
                value_input_option="USER_ENTERED",
            )

        else:
            worksheet.update(
                values=data,
                range_name=f"{start}:{end}",
                value_input_option="USER_ENTERED",
            )

    except Exception as e:
        print(f"Error updating worksheet {worksheet}: {e}")


def upload_data(all_data):
    # Daily data
    to_upload = []
    for d in st.daily_data:
        if isinstance(all_data[d], datetime):
            to_upload.append(all_data[d].strftime("%H:%M"))
        else:
            to_upload.append(all_data[d])

    worksheet_update(
        data=to_upload,
        start=f"{st.daily_data_start_col}{daily_data_y}",
        end=f"{st.daily_data_end_col}{daily_data_y}",
        worksheet=st.daily_data_sheet,
    )
    print("Daily data uploaded")

    # Daily actions
    to_upload = []

    for d in st.day_actions_order:
        if isinstance(all_data[d], datetime):
            to_upload.append(all_data[d].strftime("%H:%M"))
        elif isinstance(all_data[d], list):
            to_upload.append(all_data[d][0].strftime("%H:%M"))
        else:
            to_upload.append(all_data[d])

    worksheet_update(
        data=to_upload,
        start=f"{st.daily_actions_start_end_sheet[0]}{daily_data_y}",
        end=f"{st.daily_actions_start_end_sheet[1]}{daily_data_y}",
        worksheet=st.daily_actions_sheet,
    )
    print("Daily actions uploaded")

    # Weekly Data
    if any([x in all_data for x in st.weekly_data]):
        to_upload = [all_data[d] for d in st.weekly_data]

        worksheet_update(
            data=to_upload,
            start=f"{st.weekly_data_start_col}{str(weekly_activities_x)}",
            end=f"{st.weekly_data_end_col}{str(weekly_activities_x)}",
            worksheet=st.weekly_actions_sheet,
        )
        print("Weekly data uploaded")

    # Daily sub activities
    for d in st.activities_with_sub:
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
                    start=f"{base_10_to_alphabet(day_of_the_year - 1 + st.year_offset)}{st.daily_actions_data[d][1][to_upload_name]}",
                    worksheet=st.daily_sub_activities_sheet,
                )

    print("Daily sub activities uploaded")


def data_review(data):
    number_to_ref = {n: d for n, d in enumerate(data)}
    while True:
        print_all_data(data)
        check_total_time(data)
        print(f"Do you want to change something? [Confirm Data {st.confirm_data}]")
        answer = input()
        if 0 < int(answer) < len(list(data)):
            modify_data(data, number_to_ref[int(answer)])
        elif int(answer) == st.confirm_data:
            break


def check_total_time(data):
    inserted = datetime.combine(date(1, 1, 1), time(data["Awake"].hour, data["Awake"].minute))
    for d in data:
        if d in st.data_for_check:
            if not isinstance(data[d], datetime):
                h = data[d][0].hour
                m = data[d][0].minute
                inserted = inserted + timedelta(hours=h) + timedelta(minutes=m)
            else:
                h = data[d].hour
                m = data[d].minute
                inserted = inserted + timedelta(hours=h) + timedelta(minutes=m)

    print(f"Computed h {inserted.hour}:{inserted.minute}")


def modify_data(data, ref):
    next = True
    if isinstance(data[ref], datetime) or not isinstance(data[ref], list):
        while next:
            print("New Data: ")
            new_d = input().strip()
            new_d, next = verify_data(
                st.daily_actions_data[ref][0]
                if ref in st.daily_actions_data
                else st.daily_data[ref][1],
                new_d,
            )

        data[ref] = new_d

    else:
        while next:
            print("New Data: ")
            new_d = input().strip()
            new_d, next = verify_data(
                st.daily_actions_data[ref][0]
                if ref in st.daily_actions_data
                else st.daily_data[ref][1],
                new_d,
            )

        readed_sub_data = read_sub_data(ref, new_d)
        data[ref] = [new_d, readed_sub_data]


def print_all_data(data):
    print("These are the data inserted:")
    print(f"Day: {chosen_day.date()}")
    for n, d in enumerate(data):
        if isinstance(data[d], datetime):
            print(f"({n}) {d} - {data[d].hour}:{data[d].minute}")

        elif isinstance(data[d], list):
            print(f"({n}) {d} - {data[d][0].hour}:{data[d][0].minute}")
            for sub in data[d][1]:
                print(f"   - {sub}: {data[d][1][sub].hour}:{data[d][1][sub].minute}")

        else:
            print(f"({n}) {d} - {data[d]}")


def read_weekly_data():
    result = {}
    if week_day == st.weekly_asked_day:
        print(st.title3)
        for data in st.weekly_data:
            next = True
            while next:
                print(f"{data}: ")
                readed_data = input().strip()
                readed_data, next = verify_data(st.weekly_data[data][1], readed_data)

            result[data] = readed_data

        print(st.margin)

    return result


def read_daily_data():
    print(st.title1)
    result = {}
    for data in st.daily_data:
        next = True
        while next:
            print(f"{data}: ")
            readed_data = input().strip()
            readed_data, next = verify_data(st.daily_data[data][1], readed_data)

        result[data] = readed_data

    print(st.margin)

    return result


def read_daily_actions():
    print(st.title2)
    result = {}
    for data in st.daily_actions_data:
        next = True
        while next:
            print(f"{data}: ")
            readed_data = input().strip()
            readed_data, next = verify_data(st.daily_actions_data[data][0], readed_data)

        result[data] = readed_data

        if len(st.daily_actions_data[data]) == 2 and (
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
        sub_data = input().strip()
        sub_data, maybe_next = verify_data(st.daily_actions_data[data][0], sub_data)
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


def choose_option(data, chosen):
    print(st.ask_sub_data)
    tmp_sub = []
    ok = True
    while ok:
        for n, option in enumerate(st.daily_actions_data[data][1]):
            print(f"- {option} ({n})")
            tmp_sub.append(option)

        sub_cat = int(input())
        if sub_cat <= n:
            if tmp_sub[sub_cat] not in chosen:
                ok = False

    return tmp_sub[sub_cat]


def verify_sub_hours(total, hours, new_hour):
    tot_datetime = datetime.combine(date(1, 1, 1), time(total.hour, total.minute))
    tot_hours = datetime.combine(date(1, 1, 1), time(0, 0))
    for h in hours:
        tot_hours += timedelta(hours=int(h.hour)) + timedelta(minutes=int(h.minute))

    tot_hours = (
        tot_hours + timedelta(hours=int(new_hour.hour)) + timedelta(minutes=int(new_hour.minute))
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
        tmp = data.split(st.hour_format)
        if len(tmp) < 2:
            result = True
        if len(tmp) == 2:
            if int(tmp[1]) > 59:
                result = True

        if not result:
            data_new = datetime.strptime(data, "%H %M")

    if type == "time":
        tmp = data.split(st.hour_format)
        if len(tmp) < 2:
            data = data + " 0"
        if len(tmp) == 2:
            if int(tmp[1]) > 59:
                result = True

        if not result:
            data_new = datetime.strptime(data, "%H %M")

    elif type == "int":
        try:
            int(data)
            if int(data) < 0:
                result = True
        except ValueError:
            result = True

    elif type == "float":
        try:
            float(data)
        except ValueError:
            result = True

    elif type == "check":
        if data.lower() not in st.check_type:
            result = True
        elif data.lower() in st.yes_check_type:
            data_new = "X"
        else:
            data_new = " "

    elif type == "str":
        pass

    if result:
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
