# security.py


from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from typing import Annotated, Optional
from models import User as DBUser
from schemas import TokenData
from jose import jwt, JWTError
from datetime import timedelta, datetime
from dotenv import load_dotenv, find_dotenv
from os import getenv


_: bool = load_dotenv(find_dotenv())


SECRET_KEY = getenv("SECRET")
if SECRET_KEY is None:
    raise ValueError("No 'SECRET' found in .env file")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db: Session = Depends(get_db), username: str | None = None):
    return db.query(DBUser).filter(DBUser.username == username).first()


def authenticate_user(
    username: str, password: str, db: Annotated[Session, Depends(get_db)]
):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        print(username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
