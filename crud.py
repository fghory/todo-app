# crud.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import UserCreate, TodoCreate, TodoUpdate
from models import User as DBUser, Todo as DBTodo
from security import get_password_hash, verify_password
from typing import Annotated


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user_create.password)
    db_user = DBUser(username=user_create.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session = Depends(get_db), username: str | None = None):
    return db.query(DBUser).filter(DBUser.username == username).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(DBUser).filter(DBUser.id == user_id).first()


def create_todo(db: Session, todo_create: TodoCreate, user_id: int):
    todo = DBTodo(**todo_create.model_dump(), user_id=user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todos(db: Session, user_id: int):
    return db.query(DBTodo).filter(DBTodo.user_id == user_id).all()


def todo_erase(db: Session, todo_id: int, user_id: int):
    todo = (
        db.query(DBTodo).filter(DBTodo.id == todo_id, DBTodo.user_id == user_id).first()
    )
    if todo:
        db.delete(todo)
        db.commit()
        return True
    return False


def change_todo(db: Session, todo_id: int, todo_change: TodoUpdate, user_id: int):
    todo = (
        db.query(DBTodo).filter(DBTodo.id == todo_id, DBTodo.user_id == user_id).first()
    )
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo_change.title is not None:
        todo.title = todo_change.title
    if todo_change.title is not None:
        todo.description = todo_change.description

    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo
