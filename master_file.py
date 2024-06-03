import sys

import data_combine as dc
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

maps = {'parse all': 'Parse All', 'add data': 'Add Data',
        'single file': 'Single File', 'report': 'Report'}

print('\nWould you like to: Parse All, Add Data, create a Single File, '
      'or create a Report')

x = 0

answers = ['Parse All', 'Add Data', 'Single File', 'Report',
           'parse all', 'add data', 'single file', 'report']

while x == 0:
    ans1 = input('\nParse All/Add Data/Single File/Report: ')

    if ans1 not in answers:
        print('\nIncorrect Entry...')
        print('Please enter: Parse All, Add Data, Single File, or Report')
    else:
        x = 1

x = 0

if ans1 in maps.keys():
    ans1 = maps[ans1]

if ans1 == 'Parse All':
    while x == 0:
        exp_name = input('\nProvide a export file name ending in .csv: ')

        if exp_name[-4:] != '.csv':
            print('\nIncorrect Entry...')
        else:
            x = 1
            dc.combine_all(exp_name)
elif ans1 == 'Add Data':
    files = os.listdir(os.getcwd())

    while x == 0:
        tcx_name = input('\nProvide the name of the source data file: ')

        if tcx_name[-4:] != '.tcx':
            tcx_name += '.tcx'

        if tcx_name not in files:
            print('\nIncorrect Entry...')
        else:
            x = 1

    x = 0

    while x == 0:
        csv_name = input('\nProvide the name of the .csv: ')

        if csv_name[-4:] != '.csv':
            csv_name += '.csv'

        if csv_name not in files:
            print('\nIncorrect Entry...')
        else:
            x = 1

    x = 0

    while x == 0:
        exp_name = input('\nProvide an export file name: ')

        if exp_name[-4:] != '.csv':
            exp_name += '.csv'

        x = 1

    x = 0

    dc.add_data(tcx_name,
                csv_name,
                exp_name)
elif ans1 == 'Single File':
    files = os.listdir(os.getcwd())

    while x == 0:
        tcx_name = input('\nProvide the name of the source data file: ')

        if tcx_name[-4:] != '.tcx':
            tcx_name += '.tcx'

        if tcx_name not in files:
            print('\nIncorrect Entry...')
        else:
            x = 1

    x = 0

    while x == 0:
        exp_name = input('\nProvide an export file name: ')

        if exp_name[-4:] != '.csv':
            exp_name += '.csv'

        x = 1

    x = 0

    dc.single_file(tcx_name,
                   exp_name)

x = 0

answers = ['Y', 'N', 'y', 'n']

while x == 0:
    print('\nWould you like to do anything else?')

    complete = input('Y/N: ')

    if complete not in answers:
        print('\nIncorrect Entry...')
    elif complete == 'Y' or complete == 'y':
        x = 1
        os.system('python master_file.py')
    elif complete == 'N' or complete == 'n':
        x = 1
