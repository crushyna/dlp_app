import pandas as pd
from tabulate import tabulate


class SaveTxtHelper:

    @staticmethod
    def to_fwf(df, fname):
        content = tabulate(df.values.tolist(), list(df.columns), tablefmt="plain")
        open(fname, "w").write(content)

    pd.DataFrame.to_fwf = to_fwf
