from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Task
from schemas import TaskCreate, TaskRead

create_db_and_tables()

app = FastAPI()

@app.get("/tasks", response_model=list[TaskRead])
def get_tasks(session: Session = Depends(get_session)):
    statement = select(Task)
    tasks = session.exec(statement).all()
    return tasks

@app.post("/tasks", response_model=TaskRead)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    task = Task(
        title=task_data.title,
        completed=task_data.completed
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
        task_id: int,
        session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def complete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True

    session.add(task)
    session.commit()
    session.refresh(task)

    return task




@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()

    return {"message": "Task deleted"}