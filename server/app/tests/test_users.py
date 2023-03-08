"""Tests for users route"""


def auth(client, username="Bob", password="Alice", url="/users/register/"):
    """Helper function for auth"""
    userinfo = {"username": username, "password": password}
    response = client.post(url, json=userinfo)
    return response


def auth_fail(client, username="Bob2", password="Malice", url="/users/register/"):
    """Helper function for auth"""
    userinfo = {"username": username, "password": password}
    response = client.post(url, json=userinfo)
    return response


def test_user_registration(client):
    """Test registrating an user"""
    response = auth(client)
    assert response.status_code == 200
    resp = response.json()
    assert resp["username"] == "Bob"
    assert "api_token" in resp


def test_user_already_registered(client):
    """Test registrating an duplicate user"""
    response = auth(client)
    assert response.status_code == 400


def test_apitoken_check(client):
    """Test fetching api token for user"""
    response = auth(client, url="/users/check-api-token/")
    assert response.status_code == 200, response.text
    resp = response.json()
    assert "api_token" in resp


def test_apitoken_check_fail(client):
    """Test fetching api token for user"""
    response = auth_fail(client, url="/users/check-api-token/")
    assert response.status_code == 403
