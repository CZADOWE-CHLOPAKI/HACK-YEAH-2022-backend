from os import environ

MYSQL_USER = environ.get('MYSQL_USER', 'sendhybrid')
MYSQL_DB = environ.get('MYSQL_DB', 'sendhybrid')
MYSQL_HOST = environ.get('MYSQL_DB', 'localhost:3306')