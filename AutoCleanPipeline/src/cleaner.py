import pandas as pd
import numpy as np
from pandas.api.types import is_string_dtype

class column_cleaner:
 
    def stdn(self, df: pd.DataFrame) -> pd.DataFrame:
        
        df = df.copy()

        df.columns = (df.columns
                      .str.lower()
                      .str.strip()
                      .str.replace(" ","_")
                      .str.replace(r"[^a-z0-9_]", "", regex=True)
        )

        return df

    def missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
      
        df = df.copy()
        for col in df : 
            if (
                pd.api.types.is_integer_dtype(df[col]) 
                or pd.api.types.is_float_dtype(df[col])
                ):

                median = np.nanmedian(df[col])
                df[col] = df[col].fillna(median)
                
        return df
        
    def data_type_convt(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        for col in df:
            if(pd.api.types.is_string_dtype(df[col])):
                found = False
                for i in range(df.shape[0]):
                    str_data = df.loc[i,col]

                    if pd.isna(str_data):
                        continue

                    s = str_data.split()
                    for alpha in s:
                        if alpha.isalpha():
                            df[col] = df[col].astype(str)
                            found = True
                            break

                if found:
                    break
            else:
                print(col,"1")

        return df
    