from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import settings

# SQLALCHEMY_DATABASE_URL = "mysql://localhost:3306/test"
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}/{settings.MYSQL_DB}"

engine = create_engine(
        SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()