import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from db_orm import Base, get_db

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API is working!"}


def test_user_not_found(client):
    response = client.get("/users/999999")

    assert response.status_code == 404


def test_invalid_user_data(client):
    response = client.post(
        "/users",
        json={"name": "Y", "email": "invalid-email"},
    )

    assert response.status_code == 422


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "pytest.unique@example.com",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test User"
    assert response.json()["email"] == "pytest.unique@example.com"

def test_update_user(client):
    created = client.post(
        "/users",
        json={
            "name": "Old Name",
            "email": "old@example.com",
        },
    )
    user_id = created.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={
            "name": "New Name",
            "email": "new@example.com",
        },
    )

    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    assert response.json()["email"] == "new@example.com"


def test_delete_user(client):
    created = client.post(
        "/users",
        json={
            "name": "Delete Me",
            "email": "delete@example.com",
        },
    )
    user_id = created.json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404

def test_duplicate_email(client):
    payload = {
        "name": "First User",
        "email": "duplicate@example.com",
    }

    first = client.post("/users", json=payload)
    second = client.post("/users", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["detail"] == "Email already exists"
