from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from decouple import config

# Load environment variables

DB_USER = config('DB_USER')
DB_NAME = config('DB_NAME')
DB_PASSWORD = config('DB_PASSWORD')
DB_HOST = config('DB_HOST', default='localhost')

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"


# SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal for dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for models
Base = declarative_base()

# Dependecy (for using FastAPI with Depends)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


