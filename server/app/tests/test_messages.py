"""Tests for messages route"""


def auth(client, username="Alice", password="Alice", url="/users/register/"):
    """Helper function for auth"""
    userinfo = {"username": username, "password": password}
    response = client.post(url, json=userinfo)
    return response


def auth2(client, username="Malice", password="Alice", url="/users/register/"):
    """Helper function for auth"""
    userinfo = {"username": username, "password": password}
    response = client.post(url, json=userinfo)
    return response


def test_post_message_fail(client):
    """Test posting a message"""
    response = auth(client, username="Veeti")
    msg = {
        "message": "BobVSAlice",
        "api_token": "111",
        "user_id": 12,
        "recipient_id": 0,
        "room_uuid": 1,
    }
    response = client.post("/messages/post/", json=msg)
    assert response.status_code == 403, response.text


def test_get_messages(client):
    """Test getting messages from the server"""
    response = client.get("/messages/get/")
    assert response.status_code == 200, response.text
    resp = response.json()
    assert isinstance(resp, list)
    assert resp[0]["message"] == "Hello World!"
