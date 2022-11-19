from os import environ
from pathlib import Path

from dotenv import load_dotenv
import re

load_dotenv()

MYSQL_USER = environ.get('MYSQL_USER', 'sendhybrid')
MYSQL_DB = environ.get('MYSQL_DB', 'sendhybrid')
MYSQL_PASSWORD = environ.get('MYSQL_PASSWORD', 'sendhybrid')
MYSQL_HOST = environ.get('MYSQL_HOST', 'localhost:3306')

DOCUMENTS_DIR = Path(environ.get('DOCUMENTS_DIR', 'uploaded_documents'))
FIXED_DOCUMENTS_DIR = Path(environ.get('DOCUMENTS_DIR', 'uploaded_documents'))

print(environ["PYTHONPATH"])

FILENAME_REGEX = "^[\w\-.]+$"
MAX_FILENAME_LENGTH = 255