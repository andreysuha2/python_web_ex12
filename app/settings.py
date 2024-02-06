from dotenv import load_dotenv
import os

load_dotenv()

# APP
APP_HOST = os.getenv('APP_HOST')
APP_PORT = int(os.getenv('APP_PORT'))

# DATABASE SETTINGS

DB_ENGINE = os.getenv('DB_ENGINE')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT', ''))

DB_CONNECTION_STRING = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# URL

BASE_URL_PREFIX = '/api'
