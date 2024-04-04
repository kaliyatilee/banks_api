from fastapi import FastAPI
from lib.db_init import create_tables



app = FastAPI()

# Call the create_tables() function to create the tables
create_tables()
