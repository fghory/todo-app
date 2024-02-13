# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv, find_dotenv
from os import getenv


_: bool = load_dotenv(find_dotenv())

neon_db_url = getenv("POSTGRES_DB_URL")
if neon_db_url is None:
    raise ValueError("No 'DB URL' found in .env file")

engine = create_engine(neon_db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
