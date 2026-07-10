
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from app.models.task import Task, TaskStatus
from app.schemas.user import UserResponse



class TaskCreate(BaseModel):

    title:str
    desc:Optional[str]=None
    status : Optional[TaskStatus] = None
    assigned_to : int

    model_config = ConfigDict(from_attributes=True)

class TaskResponse(BaseModel):
    title:str
    desc:Optional[str]=None
    status : Optional[TaskStatus] = None
    user : UserResponse

    model_config = ConfigDict(from_attributes=True)
