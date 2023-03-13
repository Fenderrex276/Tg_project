import datetime
import secrets

import pytz
from tzwhere import tzwhere
from aiogram import Dispatcher


def get_timezone(location):
    tz = tzwhere.tzwhere()
    # 65.60632, -168.08659
    timezone_str = tz.tzNameAt(location["latitude"], location["longitude"])  # Seville coordinates
    timezone = pytz.timezone(timezone_str)
    dt = datetime.datetime.now()
    relative_to_utc = str(timezone.utcoffset(dt))
    tmp = relative_to_utc.split(', ')

    if len(tmp) == 1:
        hour = tmp[0].split(':')
        result = f"+{hour[0]} UTC"
    else:
        hour = tmp[1].split(':')
        s = 24 - int(hour[0])
        result = f"-{s} UTC"

    return result


def get_date_to_start_dispute(current_date: datetime.datetime, start_date: str, timezone: str):
    # print("ARGUMENTS : ", current_date.utcnow(), start_date, timezone)
    if ":" not in timezone:
        timezone += ":00"
    arr = get_current_timezone(timezone)
    hours, minutes = arr[0], arr[1]

    future_date = current_date.utcnow()
    if timezone[0] == "—":
        future_date -= datetime.timedelta(hours=hours, minutes=minutes)
    else:
        future_date += datetime.timedelta(hours=hours, minutes=minutes)

    weekdate = datetime.datetime.weekday(future_date)

    if start_date == 'select_monday':

        if weekdate == 0:
            future_date += datetime.timedelta(days=7)
        elif weekdate == 6:
            future_date += datetime.timedelta(days=8)
        else:
            future_date += datetime.timedelta(days=7 - weekdate)

    elif start_date == 'select_after_tomorrow':
        future_date += datetime.timedelta(days=2)
    # print(future_date)
    return future_date


def get_current_timezone(timezone: str):
    if timezone[0] == "—":
        tmp = timezone[2:].split(":")
        # print(f'-----> {tmp}')
        # if len(tmp) == 1:
        #     return [int(tmp[0]), 0]
        return [int(tmp[0]), int(tmp[1])]
    else:
        tmp = timezone[1:].split(":")
        # print(tmp)
        # if len(tmp) == 1:
        #     return [int(tmp[0]), 0]

        return [-1 * int(tmp[0]), -1 * int(tmp[1])]


def buttons_timezone(dp: Dispatcher, func, current_state):
    dp.register_callback_query_handler(func, text='— 10', state=current_state)
    dp.register_callback_query_handler(func, text='— 9:30', state=current_state)
    dp.register_callback_query_handler(func, text='— 9', state=current_state)
    dp.register_callback_query_handler(func, text='— 8', state=current_state)
    dp.register_callback_query_handler(func, text='— 7', state=current_state)
    dp.register_callback_query_handler(func, text='— 6', state=current_state)
    dp.register_callback_query_handler(func, text='— 5', state=current_state)
    dp.register_callback_query_handler(func, text='— 4', state=current_state)
    dp.register_callback_query_handler(func, text='— 3:30', state=current_state)
    dp.register_callback_query_handler(func, text='— 3', state=current_state)
    dp.register_callback_query_handler(func, text='— 2', state=current_state)
    dp.register_callback_query_handler(func, text='— 1', state=current_state)
    dp.register_callback_query_handler(func, text='+0', state=current_state)
    dp.register_callback_query_handler(func, text='+1', state=current_state)
    dp.register_callback_query_handler(func, text='+2', state=current_state)
    dp.register_callback_query_handler(func, text='+3', state=current_state)
    dp.register_callback_query_handler(func, text='+3:30', state=current_state)
    dp.register_callback_query_handler(func, text='+4', state=current_state)
    dp.register_callback_query_handler(func, text='+4:30', state=current_state)
    dp.register_callback_query_handler(func, text='+5', state=current_state)
    dp.register_callback_query_handler(func, text='+5:30', state=current_state)
    dp.register_callback_query_handler(func, text='+5:45', state=current_state)
    dp.register_callback_query_handler(func, text='+6', state=current_state)
    dp.register_callback_query_handler(func, text='+6:30', state=current_state)
    dp.register_callback_query_handler(func, text='+7', state=current_state)
    dp.register_callback_query_handler(func, text='+8', state=current_state)
    dp.register_callback_query_handler(func, text='+8:45', state=current_state)
    dp.register_callback_query_handler(func, text='+9', state=current_state)
    dp.register_callback_query_handler(func, text='+9:30', state=current_state)
    dp.register_callback_query_handler(func, text='+10', state=current_state)
    dp.register_callback_query_handler(func, text='+10:30', state=current_state)
    dp.register_callback_query_handler(func, text='+11', state=current_state)


"""myDate = datetime.datetime.today()
myMonth = myDate.strftime('%B')
now = datetime.datetime.now()
future_date = datetime.datetime.today() + datetime.timedelta(days=2)
print(future_date.date().day, myMonth, "через два дня будет делать!")
print(datetime.datetime.weekday(now))
print(myMonth)"""
# print(datetime.datetime.today())
# print(get_date_to_start_dispute(datetime.datetime.today(), "select_after_tomorrow"))
# print(get_current_timezone('+4:00'))
# print(len(str(get_date_to_start_dispute(datetime.datetime.now(), "select_monday", "+7"))))


