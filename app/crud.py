# app/crud.py
from sqlalchemy.orm import Session
from uuid import UUID

from .models import DBTask
from .schemas import TaskBase, TaskUpdate

# CREATE
def create_task(db: Session, task: TaskBase):
    db_task = DBTask(title=task.title, description=task.description, status=task.status.value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# READ (single task)
def get_task(db: Session, task_id: UUID):
    return db.query(DBTask).filter(DBTask.id == task_id).first()

# READ (multiple tasks)
def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DBTask).offset(skip).limit(limit).all()

# UPDATE (full update)
def update_task(db: Session, task_id: UUID, updated_task: TaskBase):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task:
        db_task.title = updated_task.title
        db_task.description = updated_task.description
        db_task.status = updated_task.status.value
        db.commit()
        db.refresh(db_task)
    return db_task

# UPDATE (partial update - PATCH)
def patch_task(db: Session, task_id: UUID, task_update: TaskUpdate):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task:
        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "status":
                setattr(db_task, key, value.value)
            else:
                setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

# DELETE
def delete_task(db: Session, task_id: UUID):
    db_task = db.query(DBTask).filter(DBTask.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True # Indicate successful deletion
    return False # Indicate task not found or deletion failed