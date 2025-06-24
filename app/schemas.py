# app/schemas.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from enum import Enum

# to ensure our status field has specific, valid values
class TaskStatus(str, Enum):
    pending_start = "pending start"
    in_progress = "in progress"
    completed = "completed"
    cancelled = "cancelled"

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

    class Config:
        from_attributes = True # Changed from orm_mode = True in Pydantic v2