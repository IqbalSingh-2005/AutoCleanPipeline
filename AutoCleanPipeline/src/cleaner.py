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
        #duplicate removal
        df = df.loc[:, ~df.columns.duplicated()]

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

    def detect_outliers_iqr(self, df, col):
        """
        Returns a DataFrame with an additional column:
        - <col>_outlier = True if outlier else False
        """
        df = df.copy()

        # Calculate Q1 and Q3
        Q1 = np.percentile(df[col].dropna(), 25)
        Q3 = np.percentile(df[col].dropna(), 75)

        IQR = Q3 - Q1

        # Outlier bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Flag outliers
        df[f"{col}_outlier"] = ~df[col].between(lower_bound, upper_bound)

        print(f"{col}: Q1={Q1}, Q3={Q3}, IQR={IQR}")
        print(f"Lower={lower_bound}, Upper={upper_bound}")
        print("Outliers count:", df[f"{col}_outlier"].sum())

        return df
