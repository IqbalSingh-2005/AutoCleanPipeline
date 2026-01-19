import pandas as pd



class FileLoader:
   
    def read_csv(self, path):
        return pd.read_csv(path)

    def read_excel(self, path):
        return pd.read_excel(path)

    def read_json(self, path):
        return pd.read_json(path)
                

    def load_data(file_path: str) -> pd.DataFrame:
        try:
            df  = pd.read_csv(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
         except Exception as e:
            raise RuntimeError(f"Failed to Load CSV: {e}")