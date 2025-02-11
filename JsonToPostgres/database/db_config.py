import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DBConfig:
    HOST = os.getenv('DB_HOST')
    PORT = os.getenv('DB_PORT')
    NAME = os.getenv('DB_NAME')
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
