from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models.task import Task
from dependencies.auth import get_current_user
from dependencies.db import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


class TaskCreate(BaseModel):
    title: str


# GET tasks (DB)
@router.get("/")
def get_tasks(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return db.query(Task).filter(Task.owner == user).all()


# POST task (DB)
@router.post("/")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        completed=False,
        owner=user
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# DELETE task (DB)
@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner == user
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}


# PATCH task (DB)
@router.patch("/{task_id}")
def toggle_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner == user
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed
    db.commit()
    db.refresh(task)

    return task
