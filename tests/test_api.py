import pytest


from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from main import app
from database import get_session


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

SQLModel.metadata.create_all(test_engine)

def get_test_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_database():
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    yield

def test_get_missing_task():
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_create_and_get_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "学习pytest",
            "completed": False
        }
    )

    assert create_response.status_code == 201

    created_task = create_response.json()

    assert created_task["title"] == "学习pytest"
    assert created_task["completed"] is False
    assert created_task["id"] is not None

    task_id = created_task["id"]

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == task_id
    assert get_response.json()["title"] == "学习pytest"
    assert get_response.json()["completed"] is False


def test_complete_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "完成 pytest 测试",
            "completed": False
        }
    )

    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}/complete")

    assert response.status_code == 200
    assert response.json()["completed"] is True

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.json()["completed"] is True

def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "准备删除的任务",
            "completed": False
        }
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Task deleted"}

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Task not found"}
