from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

# PostgreSQL connection string
# Format: "postgresql://USER:PASSWORD@HOST:PORT/DATABASE_NAME"
# These match the environment variables in your docker-compose.yml
SQLALCHEMY_DATABASE_URL = "postgresql://user:mysecretpassword@localhost:5432/taskmanagerdb"

# Create the SQLAlchemy engine
# connect_args={"check_same_thread": False} is only needed for SQLite, not PostgreSQL
# For PostgreSQL, we don't need connect_args
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
# Each instance of SessionLocal will be a database session.
# The 'autocommit=False' will prevent the session from committing changes automatically.
# The 'autoflush=False' will prevent the session from flushing objects to the database automatically.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class
# We will inherit from this class to create each of the database models or classes (the ORM models).
Base = declarative_base()

class DBTask(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="pending start", nullable=False)

# Dependency for getting a DB session in FastAPI endpoints
# This function will be used by FastAPI's Depends()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()