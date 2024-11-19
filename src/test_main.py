from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# This file contains unit tests for the main.py file.


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running"}


def test_do_credentials_check_no_credentials():
    response = client.get("/v1/credentials-check")
    assert response.json() == {"detail": "Not authenticated"}
    assert response.status_code == 401, response.text
