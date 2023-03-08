"""Testing for chatrooms"""
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import schemas

from db import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def auth(client, username="Alice", password="Alice", url="/users/register/"):
    """Helper function for auth"""
    userinfo = {"username": username, "password": password}
    response = client.post(url, json=userinfo)
    return response


def test_create_chatroom():
    resp = auth(client, username="jeff").json()
    chatroom = {"name": "Test Room", "api_token": resp["api_token"]}
    response = client.post("/chatroom/create/", json=chatroom)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Room"
    assert "uuid" in response.json()


def test_create_chatroom_again():
    resp = auth(client, username="dan").json()
    chatroom = {"name": "Test Room", "api_token": resp["api_token"]}
    response = client.post("/chatroom/create/", json=chatroom)
    assert response.json()["status_code"] == 409
    assert response.json()["detail"] == "Chatroom already exists with this name!"


def test_create_chatroom_failing_token():
    resp = auth(client, username="matt").json()
    chatroom = {"name": "Test Room", "api_token": "123"}
    response = client.post("/chatroom/create/", json=chatroom)
    assert response.status_code == 403
    assert response.json()["detail"] == "API token not valid!"


def test_different_chatroom_failures():
    resp = auth(client, username="bobbyB").json()
    chatroom = {"name": "Test Room for me", "api_token": resp["api_token"]}
    chatroom_fail = {"name": "Test Room for me2", "api_token": "kjhgch"}
    response_create = client.post("/chatroom/create/", json=chatroom)
    response_create_fail = client.post("/chatroom/create/", json=chatroom_fail)
    assert response_create_fail.status_code == 403
    message = {
        "user_id": "0",
        "recipient_id": "0",
        "room_uuid": response_create.json()["uuid"],
        "api_token": resp["api_token"],
        "message": "Hello World!",
    }
    response = client.post("/chatroom/post/", json=message)
    assert response.status_code == 200
    assert response.json() == {
        "detail": "You are not a member of this community",
        "headers": "Not a member",
        "status_code": 409,
    }
    leave_msg_too_soon = {
        "room_uuid": response_create.json()["uuid"],
        "api_token": resp["api_token"],
    }
    leave_response_too_soon = client.post("/chatroom/leave/", json=leave_msg_too_soon)
    assert leave_response_too_soon.status_code == 409
    join_msg = {
        "room_uuid": response_create.json()["uuid"],
        "api_token": resp["api_token"],
    }
    join_msg_fail = {
        "room_uuid": "asdf",
        "api_token": resp["api_token"],
    }
    join_msg_fail_api = {
        "room_uuid": response_create.json()["uuid"],
        "api_token": "asdf",
    }
    join_response = client.post("/chatroom/join/", json=join_msg)
    assert join_response.status_code == 200
    join_response = client.post("/chatroom/join/", json=join_msg)
    assert join_response.status_code == 409
    join_response = client.post("/chatroom/join/", json=join_msg_fail)
    assert join_response.status_code == 404
    join_response = client.post("/chatroom/join/", json=join_msg_fail_api)
    assert join_response.status_code == 403
    message = {
        "user_id": "0",
        "recipient_id": "0",
        "room_uuid": response_create.json()["uuid"],
        "api_token": resp["api_token"],
        "message": "Hello World!",
    }
    response2 = client.post("/chatroom/post/", json=message)
    assert response2.status_code == 200
    leave_msg_invalid = {"room_uuid": "sadda", "api_token": resp["api_token"]}
    leave_response_invalid = client.post("/chatroom/leave/", json=leave_msg_invalid)
    assert leave_response_invalid.status_code == 404
    leave_msg_invalid_api = {
        "room_uuid": response_create.json()["uuid"],
        "api_token": "asdf",
    }
    leave_response_invalid_api = client.post(
        "/chatroom/leave/", json=leave_msg_invalid_api
    )
    assert leave_response_invalid_api.status_code == 403
    leave_msg_valid = {
        "room_uuid": response_create.json()["uuid"],
        "api_token": resp["api_token"],
    }
    leave_response = client.post("/chatroom/leave/", json=leave_msg_valid)
    assert leave_response.json() == {
        "status": "ok",
        "info": "Succesfully left chatroom",
    }
