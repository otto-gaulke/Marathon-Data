import pandas as pd
import os
import data_parser as dp


def combine_all():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    df = pd.DataFrame()

    files = os.listdir(os.getcwd())
    files = [x for x in files if x[-4:] == '.tcx']

    for file in files:
        temp = dp.convert(dp.tcx_parse())

        df = pd.concat([df, temp],
                       axis=0)



combine_all()
