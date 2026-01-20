import pandas as pd

class FileLoader:

    def read_csv(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_csv(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")

    def read_excel(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_excel(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")

    def read_json(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_json(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")

    def read_fwf(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_fwf(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")

    def read_html(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_html(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")

    def read_hdf(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_hdf(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")

    def read_feather(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_hdf(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")

    def read_parquet(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_parquet(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")

    def read_orc(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_orc(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")

    def read_pickle(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_pickle(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")

    def read_parquet(self, file_path: str) -> pd.DataFrame:
        
        try:
            df = pd.read_sql(file_path)
            print(f"Loaded data with Shape: {df.shape}")
            return df
        except Exception as e:
             raise RuntimeError(f"Failed to Load CSV: {e}")
                

    