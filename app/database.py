# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection string
# Format: "postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"
# These match the environment variables in your docker-compose.yml
SQLALCHEMY_DATABASE_URL = "postgresql://user:mysecretpassword@db:5432/taskmanagerdb"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class
Base = declarative_base()

# Dependency for getting a DB session in FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()