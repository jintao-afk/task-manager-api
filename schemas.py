from sqlmodel import SQLModel


class TaskCreate(SQLModel):
    title: str
    completed: bool = False

class TaskRead(SQLModel):
    id: int
    title: str
    completed: bool

