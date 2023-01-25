# Testing of database with temp
# https://fastapi.tiangolo.com/advanced/testing-database/

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from main import app, get_db
from db import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    """Getting testclient of app"""
    with TestClient(app) as client:
        yield client


# client = TestClient(app)


# def test_create_user(client):
#     response = client.post(
#         "/users/register/",
#         json={"username": "Bob", "password": "chimichangas4life"},
#     )
#     assert response.status_code == 200, response.text
