from http import HTTPStatus

from fastapi.testclient import TestClient


class TestExceptionHandlers:
    def test_validation_exception_handler_returns_422(self, client: TestClient):
        """Sending no files returns a 422 validation error."""
        response = client.post("/api/merge/")

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
        assert response.json()["error_code"] == "VALIDATION_ERROR"
