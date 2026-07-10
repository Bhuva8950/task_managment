
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.auth import Auth

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.auth import Auth
from app.schemas.task import TaskCreate, TaskResponse
from app.models.task import Task, TaskStatus

task_router = APIRouter(
    prefix="/task",
    tags=["Tasks"]
)


@task_router.get("/", response_model=List[TaskResponse])
def get_task(db:Session=Depends(get_db)):
    task = db.query(Task).all()
    return task


@task_router.post("/create_task")
def create_task(data:TaskCreate, db:Session=Depends(get_db)):

    task = Task(
        title = data.title,
        desc = data.desc,
        status = data.status,
        assigned_to = data.assigned_to
    )

    db.add(task)
    db.commit()
    db.refresh(task)
    
    return {}