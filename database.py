import os
from sqlmodel import SQLModel, create_engine, Session
from models import Task

sqlite_url = os.getenv("DATABASE_URL", "sqlite:///tasks.db")
engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

