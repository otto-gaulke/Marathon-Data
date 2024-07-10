import pandas as pd
import os
import time
import datetime
import data_combine as dc
import visualize as v

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main(first=True):
    if first is True:
        print('Hello!')

    while True:
        print('''\nWhat would you like to do?
a) Parse .tcx data to .csv's
b) Edit existing .csv's
c) Visualize/analyze data''')
        create_edit_analyze = input('\nEnter a, b, or c: ')

        accept = ['a', 'b', 'c']

        if create_edit_analyze not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if create_edit_analyze == 'a':
        print('\nCreate...')
        create()
    elif create_edit_analyze == 'b':
        print('\nEdit...')
        edit()
    elif create_edit_analyze == 'c':
        print('\nAnalyze...')
        analyze()

    while True:
        print('\nWould you like to do anything else?')
        again = input('\nEnter yes or no: ')

        accept = ['yes', 'no']

        if again not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if again == 'yes':
        main(first=False)
    else:
        print('\nGoodbye...')

        time.sleep(2)


def extention_check(name, extention):
    if extention == '.csv':
        if name[-4:] != '.csv':
            return False
        else:
            return True
    elif extention == '.tcx':
        if name[-4:] != '.tcx':
            return False
        else:
            return True
    elif extention == '.html':
        if name[-5:] != '.html':
            return False
        else:
            return True


def create():
    while True:
        print('''\nHow would you like to parse the .tcx data?
a) Parse all .tcx data into a single main file
b) Parse .tcx data into separate files''')
        main_separate = input('\nEnter a or b: ')

        accept = ['a', 'b']

        if main_separate not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if main_separate == 'a':
        print('\nCreate main file...')
        create_main()
    elif main_separate == 'b':
        print('\nCreate separate files...')
        create_separate()

    while True:
        print('\nWould you like to create anything else?')
        again = input('\nEnter yes or no: ')

        accept = ['yes', 'no']

        if again not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if again == 'yes':
        create()


def create_main():
    while True:
        exp = input('\nEnter desired export filename (ending in .csv): ')

        if exp[-4:] != '.csv':
            print('\nIncorrect extention...')
            continue
        else:
            break

    print('\nProcessing data...')

    dc.combine_all(exp_name=exp)


def create_separate():
    while True:
        print('''\nHow would you like to parse the .tcx files?
a) Parse all .tcx's into separate files
b) Parse specific .tcx's into separate files''')
        all_specific = input('\nEnter a or b: ')

        accept = ['a', 'b']

        if all_specific not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    os.chdir('..')
    os.chdir(os.getcwd() + '\\tcx')
    files = os.listdir(os.getcwd())
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if all_specific == 'a':
        exp = [x.rstrip('tcx') + 'csv' for x in files]

        dc.single_file(exp_name=exp,
                       tcx=files)
    elif all_specific == 'b':
        while True:
            tcx = input('''\nEnter the .tcx filenames to be parsed (ending in 
.tcx, comma separated without spaces): ''')

            tcx = tcx.split(',')
            tcx = [x.strip(' ') for x in tcx]

            check_extention = True
            check_exist = True

            for file in tcx:
                if file[-4:] != '.tcx':
                    check_extention = False
                elif file not in files:
                    check_exist = False

            if check_extention is False:
                print('\nInvalid extention...')
                continue
            elif check_exist is False:
                print('\nFile does not exist...')
                continue
            else:
                break

        while True:
            exp = input('''\nEnter the desired export filenames (ending in 
.csv, comma separated without spaces): ''')

            exp = exp.split(',')
            exp = [x.strip(' ') for x in exp]

            check = True

            for file in exp:
                if file[-4:] != '.csv':
                    check = False
                    continue

            if check is False:
                print('\nInvalid extention...')
                continue
            elif len(tcx) != len(exp):
                print('\nInvalid entry...')
                continue
            else:
                break

        dc.single_file(exp_name=exp,
                       tcx=tcx)


def edit():
    while True:
        print('''\nHow would you like to edit?
a) Add .tcx data to an existing file
b) Add a custom entry to an existing file''')
        add_custom = input('\nEnter a or b: ')

        accept = ['a', 'b']

        if add_custom not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if add_custom == 'a':
        edit_add()
    elif add_custom == 'b':
        edit_custom()

    while True:
        print('\nWould you like to edit anything else?')
        again = input('\nEnter yes or no: ')

        accept = ['yes', 'no']

        if again not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if again == 'yes':
        edit()


def edit_add():
    while True:
        filename = input('\nEnter the filename to edit (ending in .csv): ')

        os.chdir('..')
        os.chdir(os.getcwd() + '\\csv')
        files = os.listdir(os.getcwd())
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        if filename[-4:] != '.csv':
            print('\nInvalid entry...')
            continue
        elif filename not in files:
            print('\nFile does not exist...')
            continue
        else:
            break

    while True:
        exp = input('\nEnter the desired export filename (ending in .csv): ')

        if exp[-4:] != '.csv':
            print('\nInvalid entry...')
            continue
        else:
            break

    while True:
        tcx = input('''\nEnter the .tcx filenames to add (ending in 
.tcx, comma separated without spaces): ''')

        tcx = tcx.split(',')
        tcx = [x.strip(' ') for x in tcx]

        os.chdir('..')
        os.chdir(os.getcwd() + '\\tcx')
        files = os.listdir(os.getcwd())
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        check_extention = True
        check_exist = True

        for file in tcx:
            if file[-4:] != '.tcx':
                check_extention = False
            elif file not in files:
                check_exist = False

        if check_extention is False:
            print('\nInvalid extention...')
            continue
        elif check_exist is False:
            print('\nFile does not exist...')
            continue
        else:
            break

    dc.add_data(filename=filename,
                exp_name=exp,
                tcx=tcx)


def edit_custom():
    while True:
        filename = input('\nEnter the filename to edit (ending in .csv): ')

        os.chdir('..')
        os.chdir(os.getcwd() + '\\csv')
        files = os.listdir(os.getcwd())
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        if filename[-4:] != '.csv':
            print('\nInvalid extention...')
            continue
        elif filename not in files:
            print('\nFile does not exist...')
            continue
        else:
            break

    while True:
        exp = input('\nEnter the desired export filename (ending in .csv): ')

        if exp[-4:] != '.csv':
            print('\nInvalid extention...')
            continue
        else:
            break

    while True:
        print('''\nEnter the following:
1. Date of the entry in MM/DD/YYYY format
2. Duration in HH:MM:SS format
3. Mile pace in HH:MM:SS format
4. Distance (miles)
5. Average heart rate''')
        entry_raw = input('''\nEnter these comma separated without spaces
(MM/DD/YYYY,HH:MM:SS,HH:MM:SS,42,42): ''')

        entry_raw = entry_raw.split(',')
        entry_raw = [x.strip(' ') for x in entry_raw]
        date_raw, time_raw = entry_raw[0], entry_raw[1]
        pace_raw, distance, hr = entry_raw[2], entry_raw[3], entry_raw[4]

        if date_raw[2] != '/' or date_raw[5] != '/':
            print('\nInvalid date format...')
            continue
        elif time_raw[2] != ':' or time_raw[5] != ':':
            print('\nInvalid duration format...')
            continue
        elif pace_raw[2] == ':' and pace_raw[5] == ':':
            print('\nInvalid mile pace format...')
            continue

        month, day, year = date_raw[0:2], date_raw[3:5], date_raw[6:10]
        hour, minute, second = time_raw[0:2], time_raw[3:5], time_raw[6:8]
        p_hour, p_minute, p_second = (pace_raw[0:2], pace_raw[3:5],
                                      pace_raw[6:8])

        int_check = [month, day, year, hour, minute, second,
                     p_hour, p_minute, p_second, distance, hr]

        check = True
        int_false = []

        for index, val in enumerate(int_check):
            try:
                int_check[index] = int(val)
            except:
                int_false.append(index)
                check = False
                continue

        if check is False:
            print(f'\n{int_false[0]} not integer...')
            continue

        if not (0 < int_check[0] < 13):
            print('\nDate: invalid month entry...')
            continue
        elif not (0 < int_check[1] < 31):
            print('\nDate: invalid day entry...')
            continue
        elif not (0 < int_check[2] < 10000):
            print('\nDate: invalid year entry...')
            continue
        elif not (int_check[3] < 24):
            print('\nDuration: invalid hour entry...')
            continue
        elif not (int_check[4] < 60):
            print('\nDuration: invalid minute entry...')
            continue
        elif not (int_check[5] < 60):
            print('\nDuration: invalid second entry...')
            continue
        elif not (int_check[6] < 24):
            print('\nPace: invalid hour entry...')
            continue
        elif not (int_check[7] < 60):
            print('\nPace: invalid minute entry...')
            continue
        elif not (int_check[8] < 60):
            print('\nPace: invalid second entry...')
            continue

        try:
            datetime.date(month=int_check[0],
                          day=int_check[1],
                          year=int_check[2])
        except:
            print('\nInvalid date entry...')
            continue

        try:
            datetime.time(hour=int_check[3],
                          minute=int_check[4],
                          second=int_check[5])
        except:
            print('\nInvalid duration entry...')
            continue

        try:
            datetime.time(hour=int_check[6],
                          minute=int_check[7],
                          second=int_check[8])
        except:
            print('\nInvalid pace entry...')
            continue

        break

    dc.data_entry(filename=filename, exp_name=exp, month=int_check[0],
                  day=int_check[1], year=int_check[2],
                  hours=int_check[3], minutes=int_check[4],
                  seconds=int_check[5], pace_hours=int_check[6],
                  pace_minutes=int_check[7], pace_seconds=int_check[8],
                  distance_miles=int_check[9], avg_hr=int_check[10])

    while True:
        print('\nWould you like to make another entry?')
        again = input('\nEnter yes or no: ')

        accept = ['yes', 'no']

        if again not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if again == 'yes':
        edit_custom()


def analyze():
    while True:
        print('''\nHow would you like to analyze the data?
a) Map data
b) Query data
c) Plot data''')
        map_query_plot = input('\nEnter a, b, or c: ')

        accept = ['a', 'b', 'c']

        if map_query_plot not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if map_query_plot == 'a':
        analyze_map()

    while True:
        print('\nWould you like to analyze anything else?')
        again = input('\nEnter yes or no: ')

        accept = ['yes', 'no']

        if again not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if again == 'yes':
        analyze()


def analyze_map():
    while True:
        print('''\nHow would you like to map the data?
a) Map data from a main file
b) Map data from separate files''')
        map_main_separate = input('\nEnter a or b: ')

        accept = ['a', 'b']

        if map_main_separate not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if map_main_separate == 'a':
        analyze_map_main()
    elif map_main_separate == 'b':
        analyze_map_separate()


def analyze_map_main():
    os.chdir('..')
    os.chdir(os.getcwd() + '\\csv')
    files = os.listdir(os.getcwd())

    while True:
        filename = input('\nEnter the filename to edit (ending in .csv): ')

        if filename[-4:] != '.csv':
            print('\nInvalid extention...')
            continue
        elif filename not in files:
            print('\nFile does not exist...')
            continue

        df = pd.read_csv(filename)

        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        dates_check = df['Date'].unique().tolist()

        if len(dates_check) < 2:
            print('\nFile not a main file...')
            continue
        else:
            break

    while True:
        print('''\nHow would you like to map data from the main file?
a) Map all dates in the main file
b) Map specific dates in the main file''')
        main_all_specific = input('\nEnter a or b: ')

        accept = ['a', 'b']

        if main_all_specific not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if main_all_specific == 'a':
        v.plot_route(filename=[filename])
    elif main_all_specific == 'b':
        while True:
            dates = input('''\nEnter the dates to map in MM/DD/YYYY format
(comma separated without spaces): ''')

            dates = dates.split(',')
            dates = [x.strip(' ') for x in dates]

            check = True

            for date in dates:
                if date[2] != '/' or date[5] != '/':
                    error = '\nInvalid date format...'
                    check = False
                    break

                month, day, year = date[0:2], date[3:5], date[6:10]

                int_check = [month, day, year]
                int_false = []

                for index, val in enumerate(int_check):
                    try:
                        int_check[index] = int(val)
                    except:
                        int_false.append(index)
                        check = False
                        continue

                if check is False:
                    error = f'\n{int_false[0]} not integer...'
                    break

                if not (0 < int_check[0] < 13):
                    error = '\nDate: invalid month entry...'
                    check = False
                    break
                elif not (0 < int_check[1] < 31):
                    error = '\nDate: invalid day entry...'
                    check = False
                    break
                elif not (0 < int_check[2] < 10000):
                    error = '\nDate: invalid year entry...'
                    check = False
                    break

                if date not in dates_check:
                    error = '\nDate does not exist...'
                    check = False
                    break

            if check is False:
                print(error)
                continue
            else:
                break

        v.plot_route(filename=[filename], dates=dates)

def analyze_map_separate():
    x = 1