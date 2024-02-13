# models.py

from database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship("Todo", back_populates="user")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    # title = Column(String)
    title: Mapped[str] = mapped_column(index=True)
    # description = Column(String)
    description: Mapped[str] = mapped_column(index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # priority  = Column(Integer)
    # complete  = Column(Boolean, default=False)

    user = relationship("User", back_populates="todos")


Base.metadata.create_all(bind=engine)
