import os
import time
import datetime
import data_combine as dc

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main(first=1):
    if first == 1:
        print('\nHello!')

    while True:
        print('\nWould you like to create a new file, '
              'edit an existing file, or analyze data?')

        new_exist_analyze = input('Enter Create, Edit, or Analyze: ')

        accept = ['Create', 'Edit', 'Analyze', 'create', 'edit', 'analyze']
        mapping = {'create': 'Create', 'edit': 'Edit', 'analyze': 'Analyze'}

        if new_exist_analyze in accept:
            if new_exist_analyze in mapping.keys():
                new_exist_analyze = mapping[new_exist_analyze]

            break
        else:
            print('\nInvalid entry...')

    if new_exist_analyze == 'Create':
        create()
    elif new_exist_analyze == 'Edit':
        edit()
    elif new_exist_analyze == 'Analyze':
        analyze()

    while True:
        print('\nWould you like to do anything else?')

        end_ans = input('Enter Yes or No: ')

        accept = ['Yes', 'No', 'yes', 'no']
        mapping = {'yes': 'Yes', 'no': 'No'}

        if end_ans in accept:
            if end_ans in mapping.keys():
                end_ans = mapping[end_ans]

            break
        else:
            print('\nInvalid entry...')

    if end_ans == 'Yes':
        main(first=2)
    elif end_ans == 'No':
        print('\nGoodbye...')

        time.sleep(2)


def file_check(filename, extension):
    files = [x for x in os.listdir(os.getcwd()) if x[-4:] == extension]

    if filename in files:
        return True
    else:
        return False


def warning():
    while True:
        print('\nWarning: a file by this name already exists. '
              'Would you like to overwite this file?')

        ovwr_ans = input('\nEnter Yes or No: ')

        accept = ['Yes', 'No', 'yes', 'no']
        mapping = {'yes': 'Yes', 'no': 'No'}

        if ovwr_ans in accept:
            if ovwr_ans in mapping.keys():
                ovwr_ans = mapping[ovwr_ans]

            if ovwr_ans == 'Yes':
                return True
            elif ovwr_ans == 'No':
                return False


def int_check(value, check):
    try:
        value = int(value)
    except ValueError:
        check = False

    return value, check


def create():
    print('\nCreate')

    while True:
        print("\nWould you like to parse all .tcx data into a main .csv, "
              "parse all .tcx data into separate .csv's, "
              "or create a single file?")

        all_sep_single = input('Enter Main, Separate, or Single: ')

        accept = ['Main', 'Separate', 'Single', 'main', 'separate', 'single']
        mapping = {'main': 'Main', 'separate': 'Separate', 'single': 'Single'}

        if all_sep_single in accept:
            if all_sep_single in mapping.keys():
                all_sep_single = mapping[all_sep_single]

            break
        else:
            print('\nInvalid entry...')

    if all_sep_single == 'Main':
        print('\nCreate a main file')

        while True:
            main_name = input('\nEnter the desired '
                              'name of the main file (ending in .csv): ')

            if main_name[-4:] == '.csv':
                check = file_check(filename=main_name,
                                   extension='.csv')

                if check is True:
                    cont = warning()

                    if cont is True:
                        break
                else:
                    break
            else:
                print('\nInvalid entry...')

        print('\nParsing data...\n')

        dc.combine_all(exp_name=main_name)
    elif all_sep_single == 'Separate':
        print('\nCreate separate files')

        files = [x for x in os.listdir(os.getcwd()) if x[-4:] == '.tcx']

        print('\nParsing data...\n')

        for file in files:
            print(file)

            dc.single_file(exp_name=file[:-4] + '.csv',
                           tcx=file)
    elif all_sep_single == 'Single':
        print('\nCreate a single file')

        while True:
            single_name = input('\nEnter the desired '
                                'name of the single file (ending in .csv): ')

            if single_name[-4:] == '.csv':
                check = file_check(filename=single_name,
                                   extension='.csv')

                if check is True:
                    cont = warning()

                    if cont is True:
                        break
            else:
                print('\nInvalid entry...')

        while True:
            tcx = input('\nEnter the name of the '
                        'source .tcx file (ending in .tcx): ')

            if tcx[-4:] == '.tcx':
                check = file_check(filename=tcx,
                                   extension='.tcx')

                if check is True:
                    break
                else:
                    print('\nInvalid entry...')
            else:
                print('\nInvalid entry...')

        print('\nParsing data...')

        dc.single_file(exp_name=single_name,
                       tcx=tcx)

    print('\nDone!')


def edit():
    print('\nEdit')

    while True:
        inp = input('\nEnter the name of the file you would like to edit '
                    '(ending in .csv),\nthe desired name of the edited file '
                    '(ending in .csv),\nthe date of the entry '
                    '(MM/DD/YYYY),\nthe duration of the entry '
                    '(HH:MM:SS),\nthe pace of the entry '
                    '(HH:MM:SS),\nthe distance (miles) '
                    'of the entry,\nthe average heart rate of the entry,\n'
                    'all comma separated without spaces\n'
                    '(ex. example_orig.csv,example_save.csv,02/22/2024,'
                    '00:28:00,00:09:30,3,160): ')

        inp = inp.split(',')
        csv, exp, date_raw, time_raw = inp[0], inp[1], inp[2], inp[3]
        pace_raw, distance, hr = inp[4], inp[5], inp[6]

        check = True

        if csv[-4:] == '.csv':
            check = file_check(filename=csv,
                               extension='.csv')
        else:
            print('\nInvalid file entry... file name must end in .csv')
            continue

        if check is False:
            print('\nInvalid file entry... file does not exist')
            continue

        if exp[-4:] == '.csv':
            check = file_check(filename=exp,
                               extension='.csv')
        else:
            print('\nInvalid save entry... save name must end in .csv')
            continue

        if check is True:
            cont = warning()

            if cont is False:
                continue

        if not (date_raw[2] == '/' and date_raw[5] == '/'):
            print('\nInvalid date entry... enter date in MM/DD/YYYY format')
            continue

        check = True

        month = date_raw[0:2]
        day = date_raw[3:5]
        year = date_raw[6:10]

        month, check = int_check(value=month,
                                 check=check)
        day, check = int_check(value=day,
                               check=check)
        year, check = int_check(value=year,
                                check=check)

        if (not (0 <= month <= 12 and 0 <= day <= 31 and 0 < year)
                or check is False):
            print('\nInvalid date entry... enter date in MM/DD/YYYY format')
            continue

        try:
            datetime.date(year=year,
                          month=month,
                          day=day)
        except ValueError:
            print('\nInvalid date entry... enter date in MM/DD/YYYY format')
            continue

        if not (time_raw[2] == ':' and time_raw[5] == ':'):
            print('\nInvalid date entry... enter time in HH:MM:SS format')
            continue

        hours = time_raw[:-6]
        minutes = time_raw[-5:-3]
        seconds = time_raw[-2:]

        hours, check = int_check(value=hours,
                                 check=check)
        minutes, check = int_check(value=minutes,
                                   check=check)
        seconds, check = int_check(value=seconds,
                                   check=check)

        if (not (0 <= hours and 0 <= minutes <= 59 and 0 <= seconds <= 59)
                or check is False):
            print('\nInvalid time entry... enter time in HH:MM:SS format')
            continue

        try:
            datetime.time(hour=hours,
                          minute=minutes,
                          second=seconds)
        except ValueError:
            print('\nInvalid time entry... enter time in HH:MM:SS format')
            continue

        if not (pace_raw[2] == ':' and pace_raw[5] == ':'):
            print('\nInvalid pace entry... enter pace in HH:MM:SS format')
            continue

        p_hours = pace_raw[:-6]
        p_minutes = pace_raw[-5:-3]
        p_seconds = pace_raw[-2:]

        p_hours, check = int_check(value=p_hours,
                                   check=check)
        p_minutes, check = int_check(value=p_minutes,
                                     check=check)
        p_seconds, check = int_check(value=p_seconds,
                                     check=check)

        if not (0 <= p_hours and 0 <= p_minutes <= 59
                and 0 <= p_seconds <= 59) or check is False:
            print('\nInvalid pace entry... enter pace in HH:MM:SS format')
            continue

        try:
            datetime.time(hour=p_hours,
                          minute=p_minutes,
                          second=p_seconds)
        except ValueError:
            print('\nInvalid pace entry... enter pace in HH:MM:SS format')
            continue

        distance, check = int_check(value=distance,
                                    check=check)

        if distance < 0 or check is False:
            print('\nInvalid distance entry...')
            continue

        hr, check = int_check(value=hr,
                              check=check)

        if hr < 0 or check is False:
            print('\nInvalid heart rate entry...')
            continue

        if check is True:
            break

    dc.data_entry(filename=csv, exp_name=exp, month=month, day=day, year=year,
                  hours=hours, minutes=minutes, seconds=seconds,
                  pace_hours=p_hours, pace_seconds=p_seconds,
                  pace_minutes=p_minutes, distance_miles=distance, avg_hr=hr)


def analyze():
    print('\nIn dev...')


main()
