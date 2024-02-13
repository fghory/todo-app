# schemas.py

from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    description: str
    # is_completed: bool


class TodoCreate(TodoBase):
    title: str
    description: str | None = None


class TodoUpdate(TodoBase):
    title: str | None = None
    description: str | None


class Todo(TodoBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    password: str


class UserCreate(UserBase):
    pass


class UserLogin(UserBase):
    pass


class User(UserBase):
    id: int
    todos: list[Todo] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
