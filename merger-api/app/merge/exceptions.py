from http import HTTPStatus

from app.core.exceptions import ApiException


class MergeTooFewDocuments(ApiException):
    """Exception raised if there are fewer than two documents uploaded."""

    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="You must upload at least 2 PDF documents to be merged.",
            error_code="TOO_FEW_DOCUMENTS",
        )


class MergeInvalidPDFDocument(ApiException):
    """Exception raised if the file is not a valid PDF file."""

    def __init__(self, filename: str):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail=f"The file '{filename}' is not a valid PDF file.",
            error_code="INVALID_PDF_DOCUMENT",
        )
