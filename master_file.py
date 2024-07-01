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
        create_edit_analyze = input('\nEnter create, edit, analyze: ')

        accept = ['create', 'edit', 'analyze']

        if create_edit_analyze not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if create_edit_analyze == 'create':
        create()
    elif create_edit_analyze == 'edit':
        edit()
    elif create_edit_analyze == 'analyze':
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


def create():
    print('\nCreate...')

    while True:
        print('Would you like to parse all .tcx data into a main file, '
              '\nor parse .tcx data into separate files?')
        main_separate = input('\nEnter main or separate: ')

        accept = ['main', 'separate']

        if main_separate not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if main_separate == 'main':
        while True:
            exp = input('\nEnter desired file name (ending in .csv): ')

            if exp[-4:] != '.csv':
                print('\nInvalid entry...')
                continue
            else:
                break

        print('\nProcessing data...')

        dc.combine_all(exp_name=exp)
    else:
        while True:
            print("\nWould you like to parse all .tcx's?")
            parse_all = input('\nEnter yes or no: ')

            accept = ['yes', 'no']

            if parse_all not in accept:
                print('\nInvalid entry...')
                continue
            else:
                break

        if parse_all == 'yes':
            os.chdir('..')
            os.chdir(os.getcwd() + '\\tcx')

            files = os.listdir(os.getcwd())
            exp = [x.rstrip('tcx') + 'csv' for x in files]

            os.chdir(os.path.dirname(os.path.abspath(__file__)))

            dc.single_file(exp_name=exp,
                           tcx=files)
        else:
            while True:
                tcx = input('\nEnter the .tcx files to be parsed '
                            '\n(ending in .tcx, comma separated '
                            'without spaces): ')

                tcx = tcx.split(',')
                tcx = [x.strip(' ') for x in tcx]

                os.chdir('..')
                os.chdir(os.getcwd() + '\\tcx')

                file_check = os.listdir(os.getcwd())

                os.chdir(os.path.dirname(os.path.abspath(__file__)))

                check = True

                for file in tcx:
                    if file[-4:] != '.tcx' or file not in file_check:
                        check = False

                if check is False:
                    print('\nInvalid entry...')
                    continue

                exp = input('\nEnter the desired names of the files '
                            '\n(ending in .csv, comma separated '
                            'without spaces): ')

                exp = exp.split(',')
                exp = [x.strip(' ') for x in exp]

                for file in exp:
                    if file[-4:] != '.csv':
                        print('\nInvalid entry...')
                        continue

                if len(tcx) != len(exp):
                    print('\nInvalid entry...')
                    continue
                else:
                    break

            dc.single_file(exp_name=exp,
                           tcx=tcx)


def edit():
    print('\nEdit...')

    while True:
        print('\nWould you like to add .tcx data to an existing file '
              '\nor add a custom entry to an existing file?')
        add_custom = input('\nEnter add or custom: ')

        accept = ['add', 'custom']

        if add_custom not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if add_custom == 'add':
        while True:
            filename = input('\nEnter the name of the file to '
                             'edit (ending in .csv): ')

            os.chdir('..')
            os.chdir(os.getcwd() + '\\csv')

            files = os.listdir(os.getcwd())

            os.chdir(os.path.dirname(os.path.abspath(__file__)))

            if filename[-4:] != '.csv' or filename not in files:
                print('\nInvalid entry...')
                continue

            exp = input('\nEnter the desired name for the '
                        'file (ending in .csv): ')

            if exp[-4:] != '.csv':
                print('\nInvalid entry...')
                continue

            tcx = input('\nEnter the .tcx files to add '
                        '\n(ending in .tcx, comma separated without spaces): ')

            tcx = tcx.split(',')
            tcx = [x.strip(' ') for x in tcx]

            os.chdir('..')
            os.chdir(os.getcwd() + '\\tcx')

            file_check = os.listdir(os.getcwd())

            os.chdir(os.path.dirname(os.path.abspath(__file__)))

            check = True

            for file in tcx:
                if file[-4:] != '.tcx'or file not in file_check:
                    check = False

            if check is False:
                print('\nInvalid entry...')
                continue

            break

        dc.add_data(filename=filename,
                    exp_name=exp,
                    tcx=tcx)
    else:
        while True:
            filename = input('\nEnter the name of the file to '
                             'edit (ending in .csv): ')

            os.chdir('..')
            os.chdir(os.getcwd() + '\\csv')

            files = os.listdir(os.getcwd())

            os.chdir(os.path.dirname(os.path.abspath(__file__)))

            if filename[-4:] != '.csv' or filename not in files:
                print('\nInvalid entry...')
                continue

            exp = input('\nEnter the desired name for the '
                        'file (ending in .csv): ')

            if exp[-4:] != '.csv':
                print('\nInvalid entry...')
                continue

            entry_raw = input('\nEnter the date of '
                              'the entry (in MM/DD/YYYY format), '
                              '\nthe duration (in HH:MM:SS format), the mile '
                              'pace (in HH:MM:SS format), the distance (miles),'
                              ' \nand the average heart rate, all comma '
                              'separated without spaces: ')

            entry_raw = entry_raw.split(',')
            entry_raw = [x.strip(' ') for x in entry_raw]
            date_raw, time_raw = entry_raw[0], entry_raw[1]
            pace_raw, distance, hr = entry_raw[2], entry_raw[3], entry_raw[4]

            if not(date_raw[2] == '/' and date_raw[5] == '/'
                   and time_raw[2] == ':' and time_raw[5] == ':'
                   and pace_raw[2] == ':' and pace_raw[5] == ':'):
                print('\nInvalid entry...')
                continue

            month, day, year = date_raw[0:2], date_raw[3:5], date_raw[6:10]
            hour, minute, second = time_raw[0:2], time_raw[3:5], time_raw[6:8]
            p_hour, p_minute, p_second = (pace_raw[0:2], pace_raw[3:5],
                                          pace_raw[6:8])

            int_check = [month, day, year, hour, minute, second,
                         p_hour, p_minute, p_second, distance, hr]

            check = True

            for index, val in enumerate(int_check):
                try:
                    int_check[index] = int(val)
                except:
                    check = False
                    continue

            if check is False:
                print('\nInvalid entry...')
                continue

            if not(0 < int_check[0] < 13 and 0 < int_check[1] < 31
                   and 0 < int_check[2] < 10000 and int_check[3] < 24
                   and int_check[4] < 60 and int_check[5] < 60
                   and int_check[6] < 24 and int_check[7] < 60
                   and int_check[8] < 60):
                print('\nInvalid entry...')
                continue

            try:
                datetime.date(month=int_check[0],
                              day=int_check[1],
                              year=int_check[2])
                datetime.time(hour=int_check[3],
                              minute=int_check[4],
                              second=int_check[5])
                datetime.time(hour=int_check[6],
                              minute=int_check[7],
                              second=int_check[8])
            except:
                print('\nInvalid entry...')
                continue

            dc.data_entry(filename=filename, exp_name=exp, month=int_check[0],
                          day=int_check[1], year=int_check[2],
                          hours=int_check[3], minutes=int_check[4],
                          seconds=int_check[5], pace_hours=int_check[6],
                          pace_minutes=int_check[7], pace_seconds=int_check[8],
                          distance_miles=int_check[9], avg_hr=int_check[10])

            print('\nWould you like to make another entry?')
            again = input('\nEnter yes or no: ')

            accept = ['yes', 'no']

            if again not in accept:
                print('\nInvalid entry...')
                continue

            if again == 'yes':
                continue
            else:
                break


def analyze():
    print('\nAnalyze...')

    os.chdir('..')
    os.chdir(os.getcwd() + '\\csv')

    files = os.listdir()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    while True:
        print('\nWould you like to map data, plot data, or create a '
              'new dataframe?')
        ans_ana = input('Enter map, plot, or dataframe: ')

        accept = ['map', 'plot', 'dataframe']

        if ans_ana not in accept:
            print('\nInvalid entry...')
            continue
        else:
            break

    if ans_ana == 'map':
        while True:
            filename = input('\nEnter the name of the '
                             'main data file (ending in .csv): ')

            if filename[-4:] != '.csv':
                print('\nInvalid entry...')
                continue

            if filename not in files:
                print('\nInvalid entry...')
                continue
            else:
                break

        os.chdir('..')
        os.chdir(os.getcwd() + '\\csv')

        dates_full = pd.read_csv(filename)['Date'].unique()

        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        while True:
            dates = input('\nEnter the dates of runs to map '
                          '(in MM/DD/YYYY format, '
                          '\ncomma separated without spaces): ')

            dates = dates.split(',').strip(' ')

            check = True

            for date in dates:
                if not(date[2] == '/' and date[5] == '/'):
                    check = False
                    continue

                month, day, year = date[0:2], date[3:5], date[6:10]

                int_check = [month, day, year]

                for index, val in enumerate(int_check):
                    try:
                        int_check[index] = int(val)
                    except:
                        check = False
                        continue

                if check is False:
                    continue

                if not(0 < int_check[0] < 13 and 0 < int_check[1] < 31
                   and 0 < int_check[2] < 10000):
                    check = False
                    continue

                try:
                    test_date = dt.datetime(year=year, month=month, day=day) \
                        .date().strftime('%Y-%m-%d')
                except:
                    check = False
                    continue

                if test_date not in dates_full:
                    check = False
                    continue

            if check is False:
                print('\nInvalid entry...')
                continue
            else:
                break

        while True:
            exp = input('\nEnter the desired names for the files in an '
                        'order corresponding to the date entry '
                        '\n(ending in .html, comma '
                        'separated without spaces): ')

            exp = exp.split(',').strip(' ')

            if len(exp) != len(dates):
                print('\nInvalid entry...')
                continue

            check = True

            for file in exp:
                if file[-5:] != '.html':
                    check = False
                    continue

            if check is False:
                print('\nInvalid entry...')
                continue
            else:
                break


main()
