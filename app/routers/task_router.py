from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskResponse
from app.dependencies import get_current_user

router = APIRouter(tags=["Tasks"])


# Create task
@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    new_task = Task(
        title=task.title,
        description=task.description,
        owner_id=user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# Get all tasks (pagination + filtering)
@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    skip: int = 0,
    limit: int = 10,
    completed: Optional[bool] = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    query = db.query(Task).filter(Task.owner_id == user.id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    tasks = query.offset(skip).limit(limit).all()

    return tasks


# Get single task
@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# Mark task completed
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def mark_completed(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True

    db.commit()
    db.refresh(task)

    return task


# Delete task
@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}