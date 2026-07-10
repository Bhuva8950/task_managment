
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from app.database import Base
from enum import Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship



class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

    
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    desc = Column(String)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    assigned_to = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")


