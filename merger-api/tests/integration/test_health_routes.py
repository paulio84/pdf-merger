from http import HTTPStatus

from fastapi.testclient import TestClient


class TestHealthEndpoint:
    def test_health_returns_200(self, client: TestClient):
        """Health endpoint returns a 200 response."""
        response = client.get("/api/health/")

        assert response.status_code == HTTPStatus.OK.value

    def test_health_returns_correct_body(self, client: TestClient):
        """Health endpoint returns the expected JSON body."""
        response = client.get("/api/health/")

        assert response.json()["status"] == "Ok!"
        assert response.json()["description"] != ""
