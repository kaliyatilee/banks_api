from typing import List
import pandas as pd

class ExcelReader:
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths

    def read_data(self):
        dataframes = []
        for file_path in self.file_paths:
            try:
                df = pd.read_excel(file_path)
                dataframes.append(df)
            except Exception as e:
                print(f"Failed to read {file_path}: {str(e)}")
                # You can choose to handle the error differently, like logging it or returning an error message
        return dataframes

# Example usage:
