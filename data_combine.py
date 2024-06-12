import pandas as pd
import os
import datetime as dt
import data_parser as dp


def combine_all(exp_name):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    df = pd.DataFrame()

    files = os.listdir(os.getcwd())
    files = [x for x in files if x[-4:] == '.tcx']

    for file in files:
        print(f'Processing {file}...')
        temp = dp.convert(dp.tcx_parse(os.getcwd() + '\\' + file))

        df = pd.concat([df, temp],
                       axis=0)

    df.sort_values(by=['Date', 'Time (Seconds)'],
                   ascending=True,
                   inplace=True)

    if exp_name in files:
        os.remove(os.getcwd() + '\\' + exp_name)

    df.to_csv(exp_name,
              index=False)


def add_data(filename, exp_name, tcx):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    df = pd.read_csv(filename)

    temp = dp.convert(dp.tcx_parse(tcx))

    df = pd.concat([df, temp],
                   axis=0)

    files = os.listdir(os.getcwd())

    if exp_name in files:
        os.remove(os.getcwd() + '\\' + exp_name)

    df.to_csv(exp_name,
              index=False)


def single_file(exp_name, tcx):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    df = dp.convert(dp.tcx_parse(os.getcwd() + '\\' + tcx))

    files = os.listdir(os.getcwd())

    if exp_name in files:
        os.remove(os.getcwd() + '\\' + exp_name)

    df.to_csv(exp_name,
              index=False)


def data_entry(filename, exp_name, month, day, year,
               hours, minutes, seconds, pace_hours,
               pace_minutes, pace_seconds, distance_miles, avg_hr):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    files = os.listdir(os.getcwd())

    df = pd.read_csv(filename)

    date = dt.date(year=year,
                   month=month,
                   day=day)

    time = dt.time(hour=hours,
                   minute=minutes,
                   second=seconds)

    pace = dt.time(hour=pace_hours,
                   minute=pace_minutes,
                   second=pace_seconds)

    seconds += (minutes + hours * 60) * 60

    distance_m = distance_miles * 1609.344

    distance_km = distance_m / 1000

    new = {'Date': [date], 'Time (Seconds)': [seconds],
           'Time (Hour-Minute-Second)': [time],
           'Distance (Meters)': [distance_m],
           'Distance (Kilometers)': [distance_km],
           'Distance (Miles)': [distance_miles], 'Pace (Minutes / Mile)': [pace],
           'Heart Rate': [avg_hr]}

    df = pd.concat([df, pd.DataFrame(new)],
                   ignore_index=True)

    df['Date'] = pd.to_datetime(df['Date'])

    df.sort_values(by=['Date', 'Time (Seconds)'],
                   ascending=True,
                   inplace=True)

    if exp_name in files:
        os.remove(os.getcwd() + '\\' + exp_name)

    df.to_csv(exp_name,
              index=False)
