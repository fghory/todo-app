from fastapi import FastAPI, Depends, HTTPException, status
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from schemas import Token, UserCreate, TodoCreate, User, TodoUpdate
from security import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user,
)
from sqlalchemy.orm import Session
from sqlalchemy import Integer
from datetime import timedelta
from crud import (
    get_user_by_username,
    create_user as create_user_db,
    create_todo as create_todo_db,
    get_todos,
    todo_erase,
    change_todo,
)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/")
def create_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    db_user = get_user_by_username(db, username=form_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_create = UserCreate(username=form_data.username, password=form_data.password)
    return create_user_db(user_create, db)


@app.post("/login/")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/todos/")
def create_todo(
    todo_make: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_todo_db(db=db, todo_create=todo_make, user_id=current_user.id)


@app.get("/todos/")
def read_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_todos(db=db, user_id=current_user.id)


@app.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = todo_erase(db=db, todo_id=todo_id, user_id=current_user.id)
    if deleted:
        return {"message": "Todo deleted"}
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@app.put("/todos/{todo_id}")
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return change_todo(
        db=db, todo_id=todo_id, todo_change=todo_update, user_id=current_user.id
    )
