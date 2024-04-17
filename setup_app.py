from fastapi import FastAPI
from lib.db_init import create_tables
from lib.imports import ExcelReader



app = FastAPI()

# Call the create_tables() function to create the tables
create_tables()
file_paths = ['file1.xlsx', 'file2.xlsx', 'file3.xlsx']
reader = ExcelReader(file_paths)
data = reader.read_data()
