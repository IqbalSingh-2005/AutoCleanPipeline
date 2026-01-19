from src.loader import load_csv

raw_data = r"D:\project\AutoCleanPipeline\AutoCleanPipeline\test\Salary.csv"

df = load_csv(raw_data)
print(df.head())
