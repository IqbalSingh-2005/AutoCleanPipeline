from src.loader import FileLoader

raw_data = r"D:\project\AutoCleanPipeline\AutoCleanPipeline\test\Salary.csv"


loader = FileLoader()

df = loader.load(raw_data)
print(df.head())
