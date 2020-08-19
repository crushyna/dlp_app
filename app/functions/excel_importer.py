import pandas as pd
import os
import xlrd


def read_excel_file(filename: str):
    dataframe = pd.read_excel(os.path.join('app/acquisition/', filename))
    return dataframe
