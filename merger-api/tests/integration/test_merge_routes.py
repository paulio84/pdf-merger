from http import HTTPStatus

from fastapi.testclient import TestClient


class TestMergeEndpoint:
    def test_merge_two_valid_pdfs_returns_pdf(
        self, client: TestClient, valid_pdf_one: bytes, valid_pdf_two: bytes
    ):
        """A successful merge of two valid PDFs returns a 200 with a PDF content type."""
        response = client.post(
            "/api/merge/",
            files=[
                ("files", ("Doc1.pdf", valid_pdf_one, "application/pdf")),
                ("files", ("Doc2.pdf", valid_pdf_two, "application/pdf")),
            ],
        )

        assert response.status_code == HTTPStatus.OK.value
        assert response.headers["content-type"] == "application/pdf"

    def test_merge_three_valid_pdfs_returns_pdf(
        self,
        client: TestClient,
        valid_pdf_one: bytes,
        valid_pdf_two: bytes,
        valid_pdf_three: bytes,
    ):
        """A successful merge of three valid PDFs returns a 200 with a PDF content type."""
        response = client.post(
            "/api/merge/",
            files=[
                ("files", ("Doc1.pdf", valid_pdf_one, "application/pdf")),
                ("files", ("Doc2.pdf", valid_pdf_two, "application/pdf")),
                ("files", ("Doc3.pdf", valid_pdf_three, "application/pdf")),
            ],
        )

        assert response.status_code == HTTPStatus.OK.value
        assert response.headers["content-type"] == "application/pdf"

    def test_merge_returns_default_filename(
        self, client: TestClient, valid_pdf_one: bytes, valid_pdf_two: bytes
    ):
        """When no filename is provided the content disposition defaults to merged.pdf."""
        response = client.post(
            "/api/merge/",
            files=[
                ("files", ("Doc1.pdf", valid_pdf_one, "application/pdf")),
                ("files", ("Doc2.pdf", valid_pdf_two, "application/pdf")),
            ],
        )

        assert response.status_code == HTTPStatus.OK.value
        assert "merged.pdf" in response.headers["content-disposition"]

    def test_merge_returns_custom_filename(
        self, client: TestClient, valid_pdf_one: bytes, valid_pdf_two: bytes
    ):
        """A custom filename is appended with .pdf and returned in content disposition."""
        response = client.post(
            "/api/merge/?filename=my-document",
            files=[
                ("files", ("Doc1.pdf", valid_pdf_one, "application/pdf")),
                ("files", ("Doc2.pdf", valid_pdf_two, "application/pdf")),
            ],
        )

        assert response.status_code == HTTPStatus.OK.value
        assert "my-document.pdf" in response.headers["content-disposition"]

    def test_merge_too_few_files_returns_400(
        self, client: TestClient, valid_pdf_one: bytes
    ):
        """Fewer than two files returns a 400 with a descriptive error message."""
        response = client.post(
            "/api/merge/",
            files=[
                ("files", ("Doc1.pdf", valid_pdf_one, "application/pdf")),
            ],
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        assert response.json()["error_code"] == "TOO_FEW_DOCUMENTS"

    def test_merge_invalid_pdf_returns_400(
        self, client: TestClient, valid_pdf_one: bytes, invalid_pdf: bytes
    ):
        """An invalid PDF returns a 400 with a descriptive error message."""
        response = client.post(
            "/api/merge/",
            files=[
                ("files", ("Doc1.pdf", valid_pdf_one, "application/pdf")),
                ("files", ("Doc4-invalid.pdf", invalid_pdf, "application/pdf")),
            ],
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        assert response.json()["error_code"] == "INVALID_PDF_DOCUMENT"

    def test_merge_empty_pdf_returns_400(
        self, client: TestClient, valid_pdf_one: bytes, empty_pdf: bytes
    ):
        """An empty PDF returns a 400 with a descriptive error message."""
        response = client.post(
            "/api/merge/",
            files=[
                ("files", ("Doc1.pdf", valid_pdf_one, "application/pdf")),
                ("files", ("Doc5-empty.pdf", empty_pdf, "application/pdf")),
            ],
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST.value
        assert response.json()["error_code"] == "INVALID_PDF_DOCUMENT"
