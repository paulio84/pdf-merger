from http import HTTPStatus

from fastapi.testclient import TestClient


class TestExceptionHandlers:
    # def test_generic_exception_handler_returns_500(self, client_no_raise: TestClient):
    #     """An unexpected exception returns a 500 with a safe error message."""
    #     with patch(
    #         "app.merge.service.MergeService.merge_pdfs",
    #         side_effect=Exception("Unexpected error"),
    #     ):
    #         response = client_no_raise.post(
    #             "/api/merge/",
    #             files=[
    #                 ("files", ("Doc1.pdf", b"%PDF-valid", "application/pdf")),
    #                 ("files", ("Doc2.pdf", b"%PDF-valid", "application/pdf")),
    #             ],
    #         )

    #     assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    #     assert response.json()["error_code"] == "INTERNAL_SERVER_ERROR"
    #     assert response.json()["message"] == "An unexpected error occurred"

    def test_validation_exception_handler_returns_422(self, client: TestClient):
        """Sending no files returns a 422 validation error."""
        response = client.post("/api/merge/")

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY.value
        assert response.json()["error_code"] == "VALIDATION_ERROR"
