from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.auth import Auth

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.auth import Auth

user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@user_router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user:User=Depends(Auth.require_roles("admin", "manager"))):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Create user
    new_user = User(
        name=user.name,
        email=user.email,
        password=Auth.hash_password(user.password),
        role=user.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@user_router.get("/all_user", response_model=List[UserResponse])
def user_list(
    current_user:User=Depends(Auth.get_current_user),
    db:Session=Depends(get_db)
    ) :
    user = db.query(User).all()
    return user


@user_router.get(f"/{id}", response_model = UserResponse)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()

    if not user :
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.patch(f"/{id}", response_model = UserResponse)
def update_user(id:int, user_data:UserUpdate, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if not user :
        raise HTTPException(status_code=404, detail="User not found")

    
    for key,value in user_data.model_dump(exclude_unset=True).items():
        if key == "password":
            setattr(user,key,Auth.hash_password(value))
        else:
            setattr(user,key,value)



    db.commit()
    db.refresh(user)
    return user

@user_router.delete(f"/{id}", response_model = dict)
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()

    if not user :
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()

    return {
        "Message":"User deleted Successfully"
    }


