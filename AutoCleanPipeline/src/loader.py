import pandas as pd
from pathlib import Path

class FileLoader:

    _READERS = {
        ".csv": pd.read_csv,
        ".xlsx": pd.read_excel,
        ".xls": pd.read_excel,
        ".json": pd.read_json,
        ".fwf": pd.read_fwf,
        ".html": pd.read_html,
        ".hdf": pd.read_hdf,
        ".feather": pd.read_feather,
        ".parquet": pd.read_parquet,
        ".orc": pd.read_orc,
        ".pkl": pd.read_pickle,
    }

    def load(self, file_path: str) -> pd.DataFrame: 
        ext = Path(file_path).suffix.lower()

        if ext not in self._READERS:
            raise ValueError(f"Unsupported file type: {ext}")

        try:
     
            df = self._READERS[ext](file_path)

            # pd.read_html returns a list → normalize
            if isinstance(df, list):
                df = df[0]

            print(f"Loaded {file_path} with shape {df.shape}")
            return df

        except Exception as e:
            raise RuntimeError(f"Failed to load {file_path}: {e}")
