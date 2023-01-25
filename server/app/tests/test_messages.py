"""Tests for messages route"""


def auth(client, username="Alice", password="Alice", url="/users/register/"):
    """Helper function for auth"""
    userinfo = {"username": username, "password": password}
    response = client.post(url, json=userinfo)
    return response


def test_post_message(client):
    """Test posting a message"""
    response = auth(client)
    assert response.status_code == 200, response.text
    resp = response.json()
    assert "api_token" in resp
    msg = {"message": "BobVSAlice", "api_token": resp["api_token"]}
    response = client.post("/messages/post/", json=msg)
    assert response.status_code == 200, response.text
    resp = response.json()
    assert resp["status"] == "ok"


def test_get_messages(client):
    """Test getting messages from the server"""
    response = client.get("/messages/get/")
    assert response.status_code == 200, response.text
    resp = response.json()
    assert type(resp) is list
    assert resp[0]["message"] == "BobVSAlice"
