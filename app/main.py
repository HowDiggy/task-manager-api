# app/main.py
from fastapi import FastAPI
from sqlalchemy.orm import Session # Still needed for get_db dependency

# Imports needed for database initialization
from .database import engine, Base

# Import the tasks router
from .routers.tasks import router as tasks_router # Alias it as tasks_router for clarity

app = FastAPI()

# This line remains as it creates tables on app startup
Base.metadata.create_all(bind=engine)

# Include the tasks router
app.include_router(tasks_router)

# All API endpoint definitions have been moved to app/routers/tasks.py