from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi import HTTPException

from app.models.user import User
from app.database import Base, engine
from app.routers.user import user_router
from app.routers.task import task_router
from app.schemas.user import LogingSchema
from app.auth import Auth

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(task_router)

@app.get("/")
def home():
    return {"message": "Hello, World!"}


@app.post("/login")
def login_user(userdata:LogingSchema, db:Session=Depends(get_db)):

    email = userdata.email
    password = userdata.password
    
    user = db.query(User).filter(User.email==email).first()
    if not user :
        raise HTTPException(status_code=404, detail="User not found")

    user_password = user.password

    is_autherised = Auth.verify_password(password, user_password)

    if is_autherised:
        token = Auth.create_access_token({"email":email})
    else:
        raise HTTPException(status_code=404, detail="Unautherised User")

    return {
            "access_token": token,
            "token_type": "bearer"
        }