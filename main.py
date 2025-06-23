from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum
from database import Base, engine, SessionLocal, DBTask, get_db
from sqlalchemy.orm import Session


app = FastAPI()
Base.metadata.create_all(bind=engine) # creates all tables defined by Base (like DBTask) in the database

# to ensure our status field has specific, valid values
class TaskStatus(str, Enum):
    pending_start = "pending start"
    in_progress = "in progress"
    completed = "completed"
    cancelled = "cancelled"

# Todo: define two pydantic models for tasks: TaskBase and Task
# for creating or updating a task
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending_start

# Model for partial updates (PATCH)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

# for returning a task (includes the ID)
class Task(TaskBase):
    id: UUID

@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskBase, db: Session = Depends(get_db)):
    db_task = DBTask(title=task.title, description=task.description, status=task.status.value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@app.get("/tasks/", response_model=list[TaskBase])
async def read_tasks(db: Session = Depends(get_db)):
    tasks = db.query(DBTask).all()
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: UUID, updated_task: TaskBase, db: Session = Depends(get_db)):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db_task.title = updated_task.title
    db_task.description = updated_task.description
    db_task.status = updated_task.status.value

    db.commit()
    db.refresh(db_task)

    return db_task


@app.patch("/tasks/{task_id}", response_model=Task)
async def patch_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "status":
            setattr(db_task, key, value.value)
        else:
            setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(db_task)
    db.commit()

    return



