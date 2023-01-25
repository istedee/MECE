"""Tests for the FastAPI backend server to ensure functionality"""

# Based on official documentation of FastAPI:
# https://fastapi.tiangolo.com/tutorial/testing/


def test_health_check(client):
    """Test that the health check of the server works"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}
