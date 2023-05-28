from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Union
from core.exceptions import error_messages
from app.api.v1.models.user import User
from app.api.v1.repositories.common import CRUD
from app.api.v1.serializers.user import UserIn, Token, TokenData
from app.api.v1.dependancies.hash import Hasher

SECRET_KEY = "skeleton"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


def get_user(db: Session, email: str):
    user_data = db.query(User).filter_by(email=email).first()
    return user_data if user_data else False


def authenticate_user(email: str, password: str, db):
    email = email.lower()
    user = get_user(db=db, email=email)
    print(user)
    if not user:
        return False
    return user if Hasher().verify_password(password, user.password) else False


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=120)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db=Depends(CRUD().db_conn)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise error_messages.InvalidCredentials
        token_data = TokenData(email=email)
    except JWTError as e:
        raise error_messages.InvalidCredential from e
    user = get_user(db, email=token_data.email)
    if user is None:
        raise error_messages.InvalidCredentials
    return user


async def get_current_active_user(current_user: UserIn = Depends(get_current_user)):
    if not current_user.active:
        raise error_messages.UnactiveUser
    return current_user
