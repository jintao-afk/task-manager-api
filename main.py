from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Task


create_db_and_tables()

app = FastAPI()

@app.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    statement = select(Task)
    tasks = session.exec(statement).all()
    return tasks

@app.post("/tasks")
def create_task(
    task: Task,
    session: Session = Depends(get_session)
):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/tasks/{task_id}")
def get_task(
        task_id: int,
        session: Session = Depends(get_session)
):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.patch("/tasks/{task_id}/complete")
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