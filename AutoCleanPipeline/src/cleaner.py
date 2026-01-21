from pandas._libs.lib import is_integer

from src.loader import FileLoader

import pandas as pd
import numpy as np
import re

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

            if pd.api.types.is_integer_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
                median = np.nanmedian(df[col])
                df[col] = df[col].fillna(median)
                
        return df
        

    