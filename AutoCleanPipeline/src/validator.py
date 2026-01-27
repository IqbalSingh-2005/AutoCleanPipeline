import numpy as np
import pandas as pd

class stats:
    def stats(self, df: pd.DataFrame):
        df = df.copy()

        for col in df:
            if (pd.api.types.is_integer_dtype(df[col])
                or pd.api.types.is_float_dtype(df[col])):
                print(col)
                print(df[col].describe())