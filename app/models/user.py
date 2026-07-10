
from sqlalchemy import Column, Integer, String, Enum as SQLEnum
from app.database import Base
from enum import Enum
from sqlalchemy.orm import relationship


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    role = Column(SQLEnum(UserRole),default=UserRole.EMPLOYEE)

    tasks = relationship("Task", back_populates="user")
    

    