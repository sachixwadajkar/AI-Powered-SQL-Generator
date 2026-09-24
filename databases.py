import os
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT", 3306)

DATABASE_URL = (
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

engine = create_engine(DATABASE_URL, echo=False)

def list_databases():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW DATABASES"))
            databases = [row[0] for row in result]
        return databases
    except Exception as e:
        logging.error(f"Error listing databases: {e}")
        return []

def list_tables(database_name):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SHOW TABLES FROM {database_name}"))
            tables = [row[0] for row in result]
        return tables
    except Exception as e:
        logging.error(f"Error listing tables: {e}")
        return []

def list_columns(database_name, table_name):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SHOW COLUMNS FROM {database_name}.{table_name}"))
            columns = [row[0] for row in result]
        return columns
    except Exception as e:
        logging.error(f"Error listing columns: {e}")
        return []
