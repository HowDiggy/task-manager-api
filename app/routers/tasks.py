# app/routers/tasks.py
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session # Keep Session import for dependency injection

from ..database import get_db # Relative import for get_db
from .. import crud # Relative import for crud functions
from ..schemas import Task, TaskBase, TaskUpdate, TaskStatus # Relative import for Pydantic schemas

# Create an APIRouter instance
router = APIRouter(
    prefix="/tasks",    # All paths in this router will be prefixed with "/tasks"
    tags=["tasks"],     # Adds this tag to the API documentation (Swagger UI)
    responses={404: {"description": "Not found"}}, # Common response for this router
)

@router.post("/", response_model=Task)
async def create_task_endpoint(task: TaskBase, db: Session = Depends(get_db)):
    db_task = crud.create_task(db=db, task=task)
    return db_task

@router.get("/", response_model=list[Task])
async def read_tasks_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=Task)
async def read_task_endpoint(task_id: UUID, db: Session = Depends(get_db)):
    task = crud.get_task(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task_endpoint(task_id: UUID, updated_task: TaskBase, db: Session = Depends(get_db)):
    db_task = crud.update_task(db=db, task_id=task_id, updated_task=updated_task)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

@router.patch("/{task_id}", response_model=Task)
async def patch_task_endpoint(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.patch_task(db=db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(task_id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return