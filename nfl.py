from datetime import datetime as dt
import time
import pandas as pd


def current_week():
    dt_now = dt.now()
    start_date = pd.Timestamp('2023-09-07')
    end_date = pd.Timestamp('2024-03-01')
    week_range = pd.interval_range(start=start_date,end=end_date,freq='7D',closed='left')
    weeks = week_range.contains(dt_now)
    current_week = 0
    for i in range(len(weeks)):
        if weeks[i] == True:
            current_week = i + 1
        else:
            continue
    if current_week == 0:
        current_week = 1
    return current_week

def week_period():
    week = current_week()
    weekday = dt.now().strftime("%A")
    if weekday == 'Thursday':
        return 1
    elif weekday == 'Sunday':
        if dt.now().time() <= dt(2023,1,1,13,0,0,0).time():
            return 2
        elif dt.now().time() <= dt(2023,1,1,16,1,0,0).time():
            return 3
        elif dt.now().time() <= dt(2023,1,1,20,0,0,0).time():
            return 4
    elif weekday == 'Monday':
        if dt.now().time() <= dt(2023,1,1,8,0,0,0).time():
            return 5
        else:
            return 6
    elif weekday == 'Tuesday':
        return 7
    elif weekday == 'Wednesday':
        return 8
    elif weekday == 'Friday':
        return 9