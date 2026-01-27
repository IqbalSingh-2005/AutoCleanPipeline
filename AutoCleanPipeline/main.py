from src.loader import FileLoader
from src.cleaner import column_cleaner
from src.visualizer import visual
from src.validator import stats



loader = FileLoader()
c_clean = column_cleaner()
stats = stats()

raw_data = loader.upload_file()
df = loader.load(str(raw_data))
df = c_clean.stdn(df)
df = c_clean.data_type_convt(df)
df = c_clean.missing_data(df)
df = c_clean.detect_outliers_iqr(df,"salary")
stats.stats(df)
visual(df)

print(df.head())
