from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

from app.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

class Auth():
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)


    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(
            plain_password,
            hashed_password
        )

    @staticmethod
    def create_access_token(data: dict) -> str:
        payload = data.copy()
        print(payload)

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        payload.update({"exp": expire})
        print(payload)
        access_token = jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM,
        )

        return access_token

    @staticmethod
    def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
            )

            email = payload.get("email")

            if email is None:
                raise credentials_exception

        except JWTError:
            raise credentials_exception

        user = db.query(User).filter(User.email == email).first()

        if user is None:
            raise credentials_exception

        return user

    @staticmethod
    def require_roles(*roles):
        def role_checker(
            current_user: User = Depends(Auth.get_current_user),
        ):
            if current_user.role.value not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permission denied",
                )

            return current_user

        return role_checker