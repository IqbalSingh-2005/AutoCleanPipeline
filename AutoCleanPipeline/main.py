from src.loader import FileLoader
from src.cleaner import column_cleaner



loader = FileLoader()
c_clean = column_cleaner()

raw_data = loader.upload_file()
df = loader.load(str(raw_data))
df = c_clean.stdn(df)
df = c_clean.data_type_convt(df)
df = c_clean.missing_data(df)

print(df.head())
