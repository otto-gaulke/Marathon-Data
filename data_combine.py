import pandas as pd
import os
import data_parser as dp


def combine_all(export_name):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    df = pd.DataFrame()

    files = os.listdir(os.getcwd())
    files = [x for x in files if x[-4:] == '.tcx']

    for file in files:
        temp = dp.convert(dp.tcx_parse(os.getcwd() + '\\' + file))

        df = pd.concat([df, temp],
                       axis=0)

    df.to_csv(export_name,
              index=False)


def add_data(file_add, csv_name, export_name):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    df = pd.read_csv(csv_name)

    temp = dp.convert(dp.tcx_parse(file_add))

    df = pd.concat([df, temp],
                   axis=0)

    df.to_csv(export_name,
              index=False)


def single_file(file, export_name):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    df = dp.convert(dp.tcx_parse(os.getcwd() + '\\' + file))

    df.to_csv(export_name,
              index=False)
