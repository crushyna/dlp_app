import pandas as pd
import numpy as np
import os
import xlrd


def read_excel_file(filename: str):
    dataframe = pd.read_excel(os.path.join('app/acquisition/', filename),
                              header=None,
                              names=None,
                              index_col=None,
                              usecols="A,C",
                              convert_float=False,
                              skiprows=1)

    # name columns properly
    dataframe.columns = ['part_no', 'price']

    # change comma separators
    dataframe = dataframe.apply(lambda x: x.str.replace(',', '.'))

    # change price objects to floats
    dataframe['price'] = pd.to_numeric(dataframe['price'])

    # change type "object" to string
    dataframe['part_no'] = dataframe['part_no'].astype('str')

    return dataframe
