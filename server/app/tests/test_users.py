"""Tests for users route"""


def test_user_registration(test_app):
    """Test registrating an user"""
    userinfo = {"username": "Bob", "password": "Alice"}
    response = test_app.post("/users/register/", json=userinfo)
    assert response.status_code == 200
    resp = response.json()
    assert resp["username"] == "Bob"
    assert "api_token" in resp.keys()
