from src.loader import FileLoader
from src.cleaner import column_cleaner



loader = FileLoader()
c_clean = column_cleaner()

raw_data = loader.upload_file()
df = loader.load(str(raw_data))
f = c_clean.stdn(df)
print(f.head())
