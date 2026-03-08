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

    def data(self, df: pd.DataFrame):
        df = df.copy()
        
        rows, cols = df.shape

        size_bytes = df.memory_usage(deep=True).sum()
        size_mb = size_bytes / (1024 * 1024)

        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

        duplicated_mask = df.duplicated(keep="first")
        duplicate_rows_count = int(duplicated_mask.sum())

        if duplicate_rows_count > 0:
            dup_mask_all = df.duplicated(keep=False)
            dup_df = df.loc[duplicated_mask]
            duplicated_column_names = [
                str(col) for col in dup_df.columns
                if dup_df[col].nunique(dropna=False) > 1
            ]

        else:
            duplicated_column_names = []

        nulls_by_col = df.isna().sum()
        nulls_by_col = nulls_by_col[nulls_by_col > 0].astype(int)  # only columns with nulls
        null_columns = [str(c) for c in nulls_by_col.index.tolist()] 
        total_nulls = int(nulls_by_col.sum())

        summary = {
        "rows": int(rows),
        "columns": int(cols),
        "memory": {"bytes": size_bytes, "mb": size_mb},
        "nulls": {
            "total": total_nulls,
            "columns_with_nulls": null_columns,          # <-- column names with nulls
            "by_column": nulls_by_col.to_dict(),         # <-- {"colA": 2, "colB": 5}
        },
        "dtypes": dtypes,
        "duplicates": {
            "duplicate_rows_count": duplicate_rows_count,
            "duplicated_column_names": duplicated_column_names,
        },
        "column_names": [str(c) for c in df.columns],
            }

        return summary


               