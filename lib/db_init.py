from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.model import *
import os

# Load environment variables from .env file
load_dotenv()

# Get database connection information from environment variables
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')



# Create database engine and session
# engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}", sslmode='disable')
engine = create_engine(f"mysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
Session = sessionmaker(bind=engine)
DBSession = Session()
# Base = declarative_base()



def create_tables():
    print("Running create tables")
    Base.metadata.create_all(bind=engine)

    