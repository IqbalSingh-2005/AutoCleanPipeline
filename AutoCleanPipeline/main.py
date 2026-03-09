from src.loader import FileLoader
from src.cleaner import column_cleaner
from src.visualizer import visual
from src.validator import stats


class AutoCleanPipeline:
    def __init__(self):
        self.loader = FileLoader()
        self.cleaner = column_cleaner()
        self.validator = stats()
        self.raw_data_path = None
        self.df = None
        self.summary = None

    def upload_file(self):
        """Prompt user to upload a file and store the path"""
        self.raw_data_path = self.loader.upload_file()
        return self.raw_data_path

    def load_data(self, file_path=None):
        """Load data from file path and return dataframe"""
        if file_path is None:
            if self.raw_data_path is None:
                raise ValueError("No file path provided. Call upload_file() first or pass file_path.")
            file_path = self.raw_data_path

        self.df = self.loader.load(str(file_path))
        return self.df

    def get_summary(self):
        """Generate and return summary of raw data"""
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        self.summary = self.validator.data(self.df)
        return self.summary

    def standardize_columns(self):
        """Standardize column names"""
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        self.df = self.cleaner.stdn(self.df)
        return self.df

    def convert_data_types(self):
        """Convert data types"""
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        self.df = self.cleaner.data_type_convt(self.df)
        return self.df

    def handle_missing_data(self):
        """Handle missing data"""
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        self.df = self.cleaner.missing_data(self.df)
        return self.df

    def detect_outliers(self, column):
        """Detect and handle outliers in specified column"""
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        self.df = self.cleaner.detect_outliers_iqr(self.df, column)
        return self.df

    def clean_all(self, outlier_column=None):
        """Apply all cleaning steps"""
        self.standardize_columns()
        self.convert_data_types()
        self.handle_missing_data()

        if outlier_column:
            self.detect_outliers(outlier_column)

        return self.df

    def generate_stats(self):
        """Generate and display statistics"""
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        self.validator.stats(self.df)

    def visualize(self):
        """Generate visualizations"""
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        visual(self.df)

    def run_full_pipeline(self, file_path=None, outlier_column="salary"):
        """Run the complete pipeline from upload to visualization"""
        if file_path is None:
            self.upload_file()
            file_path = self.raw_data_path

        self.load_data(file_path)
        self.get_summary()
        self.clean_all(outlier_column)
        self.generate_stats()
        self.visualize()

        return self.df


if __name__ == "__main__":
    pipeline = AutoCleanPipeline()
    df = pipeline.run_full_pipeline()
    print(df.head())
