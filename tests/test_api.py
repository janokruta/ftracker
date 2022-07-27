from fastapi.testclient import TestClient

from ftracker.api.main import api

client = TestClient(api)


def test_home_response():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
