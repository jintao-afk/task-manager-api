from sqlmodel import SQLModel, create_engine
from models import Task

sqlite_url = "sqlite:///tasks.db"
engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
