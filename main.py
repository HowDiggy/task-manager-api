from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum
from database import Base, engine, SessionLocal, DBTask

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

# in-memory storage for tasks
tasks_db: dict[UUID, Task] = {}

@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskBase):
    task_id = uuid4()
    new_task = Task(id=task_id, **task.model_dump())
    tasks_db[task_id] = new_task
    return new_task

@app.get("/tasks/", response_model=list[TaskBase])
async def read_tasks():
    return list(tasks_db.values())


@app.get("/tasks/{task_id}", response_model=TaskBase)
async def read_task(task_id: UUID):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return tasks_db[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: UUID, updated_task: TaskBase):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # retrieve existing task
    existing_task = tasks_db[task_id]

    # update attributes from updated_task (which is TaskBase)
    existing_task.title = updated_task.title
    existing_task.description = updated_task.description
    existing_task.status = updated_task.status

    return existing_task


@app.patch("/tasks/{task_id}", response_model=Task)
async def patch_task(task_id: UUID, task_update: TaskUpdate):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    existing_task = tasks_db[task_id]

    # Update only the fields that were provided in the request
    # Pydantic's .model_dump(exclude_unset=True) is perfect for this
    update_data = task_update.model_dump(exclude_unset=True)
    updated_item = existing_task.model_copy(update=update_data)

    tasks_db[task_id] = updated_item
    return updated_item

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID):
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    del tasks_db[task_id] # Remove the task from the dictionary
    return # No content is typically returned for 204 No Content



