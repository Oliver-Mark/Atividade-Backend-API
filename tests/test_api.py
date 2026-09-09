import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.infrastructure.database import Base, get_db
from main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_create_user_success(client):
    payload = {"name": "Carlos Silva", "email": "carlos@example.com"}
    response = client.post("/users", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["message"] == "User created successfully"
    assert body["data"]["name"] == "Carlos Silva"
    assert body["data"]["email"] == "carlos@example.com"
    assert "id" in body["data"]


def test_create_user_duplicate_email(client):
    payload = {"name": "Carlos Silva", "email": "carlos@example.com"}
    client.post("/users", json=payload)

    response = client.post("/users", json=payload)
    assert response.status_code == 409
    body = response.json()
    assert body["success"] is False
    assert "already registered" in body["message"]
    assert body["data"] is None


def test_create_user_invalid_email(client):
    payload = {"name": "Carlos", "email": "email_invalido_sem_arroba"}
    response = client.post("/users", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert "Validation error" in body["message"]


def test_get_users_list(client):
    client.post("/users", json={"name": "User 1", "email": "user1@example.com"})
    client.post("/users", json={"name": "User 2", "email": "user2@example.com"})

    response = client.get("/users")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert len(body["data"]) == 2


def test_get_user_by_id_success(client):
    create_res = client.post("/users", json={"name": "User 1", "email": "user1@example.com"})
    user_id = create_res.json()["data"]["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["id"] == user_id


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["message"] == "User not found"


def test_update_user(client):
    create_res = client.post("/users", json={"name": "User Old", "email": "old@example.com"})
    user_id = create_res.json()["data"]["id"]

    response = client.put(f"/users/{user_id}", json={"name": "User New"})
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "User New"
    assert body["data"]["email"] == "old@example.com"


def test_delete_user(client):
    create_res = client.post("/users", json={"name": "User To Delete", "email": "delete@example.com"})
    user_id = create_res.json()["data"]["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True

    get_res = client.get(f"/users/{user_id}")
    assert get_res.status_code == 404


def test_create_course_success(client):
    payload = {
        "title": "FastAPI Masterclass",
        "description": "Curso completo de FastAPI com Clean Architecture",
        "workload": 40,
    }
    response = client.post("/courses", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["title"] == "FastAPI Masterclass"
    assert body["data"]["workload"] == 40


def test_create_course_invalid_workload(client):
    payload = {"title": "Curso Teste", "workload": 0}
    response = client.post("/courses", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False


def test_get_courses_list_and_by_id(client):
    create_res = client.post("/courses", json={"title": "Python Básico", "workload": 20})
    course_id = create_res.json()["data"]["id"]

    list_res = client.get("/courses")
    assert list_res.status_code == 200
    assert len(list_res.json()["data"]) == 1

    get_res = client.get(f"/courses/{course_id}")
    assert get_res.status_code == 200
    assert get_res.json()["data"]["title"] == "Python Básico"


def test_update_and_delete_course(client):
    create_res = client.post("/courses", json={"title": "Banco de Dados", "workload": 30})
    course_id = create_res.json()["data"]["id"]

    put_res = client.put(f"/courses/{course_id}", json={"workload": 50})
    assert put_res.status_code == 200
    assert put_res.json()["data"]["workload"] == 50

    del_res = client.delete(f"/courses/{course_id}")
    assert del_res.status_code == 200

    get_res = client.get(f"/courses/{course_id}")
    assert get_res.status_code == 404


def test_enrollment_success(client):
    u_res = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    c_res = client.post("/courses", json={"title": "Arquitetura de Software", "workload": 60})
    user_id = u_res.json()["data"]["id"]
    course_id = c_res.json()["data"]["id"]

    enroll_res = client.post("/enrollments", json={"user_id": user_id, "course_id": course_id})
    assert enroll_res.status_code == 201
    body = enroll_res.json()
    assert body["success"] is True
    assert body["message"] == "User enrolled in course successfully"
    assert body["data"]["user_id"] == user_id
    assert body["data"]["course_id"] == course_id


def test_duplicate_enrollment_fails(client):
    u_res = client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
    c_res = client.post("/courses", json={"title": "Clean Code", "workload": 25})
    user_id = u_res.json()["data"]["id"]
    course_id = c_res.json()["data"]["id"]

    client.post("/enrollments", json={"user_id": user_id, "course_id": course_id})

    dup_res = client.post("/enrollments", json={"user_id": user_id, "course_id": course_id})
    assert dup_res.status_code == 409
    body = dup_res.json()
    assert body["success"] is False
    assert "already enrolled" in body["message"]


def test_enrollment_user_or_course_not_found(client):
    res1 = client.post("/enrollments", json={"user_id": 999, "course_id": 1})
    assert res1.status_code == 404
    assert res1.json()["message"] == "User not found"

    u_res = client.post("/users", json={"name": "Carlos", "email": "carlos@example.com"})
    user_id = u_res.json()["data"]["id"]
    res2 = client.post("/enrollments", json={"user_id": user_id, "course_id": 999})
    assert res2.status_code == 404
    assert res2.json()["message"] == "Course not found"


def test_get_user_courses_relational(client):
    u_res = client.post("/users", json={"name": "Daniel", "email": "daniel@example.com"})
    user_id = u_res.json()["data"]["id"]

    c1_res = client.post("/courses", json={"title": "Python", "workload": 30})
    c2_res = client.post("/courses", json={"title": "PostgreSQL", "workload": 20})
    c1_id = c1_res.json()["data"]["id"]
    c2_id = c2_res.json()["data"]["id"]

    client.post("/enrollments", json={"user_id": user_id, "course_id": c1_id})
    client.post("/enrollments", json={"user_id": user_id, "course_id": c2_id})

    rel_res = client.get(f"/users/{user_id}/courses")
    assert rel_res.status_code == 200
    body = rel_res.json()
    assert body["success"] is True
    assert body["data"]["id"] == user_id
    assert body["data"]["name"] == "Daniel"
    assert len(body["data"]["courses"]) == 2
    course_titles = [c["title"] for c in body["data"]["courses"]]
    assert "Python" in course_titles
    assert "PostgreSQL" in course_titles
