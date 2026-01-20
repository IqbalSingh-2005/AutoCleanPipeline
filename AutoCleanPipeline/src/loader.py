import pandas as pd
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

class FileLoader:

    #Dictionary for getting function for related CSV
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
    #Function to convert data in Dataframe
    

    def upload_file(self):
        root = tk.Tk()
        file_path = filedialog.askopenfilename(title="Select Data source", filetypes=[("All files", "*.*")])
        root.destroy()
        return file_path

    def load(self, file_path: str) -> pd.DataFrame: 
        ext = Path(file_path).suffix.lower()
        if ext not in self._READERS:
            raise ValueError(f"Unsupported file type: {ext}")

        try:
            df = self._READERS[ext](file_path)
            if isinstance(df, list):    # read_html returns a list
                df = df[0]

            print(f"Loaded {file_path} with shape {df.shape}")
            return df

        except Exception as e:
            raise RuntimeError(f"Failed to load {file_path}: {e}")

