from numpy._core import numeric
import pandas as pd
import numpy as np
from pandas.api.types import is_float, is_integer, is_string_dtype

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

        for col in df.columns:
            if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):

                is_all_numeric = True

                for val in df[col]:
                    if pd.isna(val):
                        continue
                    try:
                        float(val)
                    except (ValueError, TypeError):
                        is_all_numeric = False
                        break

                # 🔑 ONE decision per column
                if is_all_numeric:
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype(float)

                
                else:
                    df[col] = df[col].astype("string")

            else:
                print(col, "1")

        print(df.dtypes)
        return df
