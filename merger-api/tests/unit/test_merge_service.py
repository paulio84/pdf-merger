import io

import pytest
from fastapi import UploadFile

from app.merge.exceptions import MergeInvalidPDFDocument, MergeTooFewDocuments
from app.merge.service import MergeService


def make_upload_file(content: bytes, filename: str) -> UploadFile:
    """Helper to create an UploadFile from bytes for testing."""
    return UploadFile(
        filename=filename,
        file=io.BytesIO(content),
    )


@pytest.fixture
def service() -> MergeService:
    """Return a MergeService instance."""
    return MergeService()


class TestMergePDFs:
    async def test_merge_two_valid_pdfs_return_bytes(
        self, service: MergeService, valid_pdf_one: bytes, valid_pdf_two: bytes
    ):
        """A successful merge of two valid PDFs returns a byte stream."""
        files = [
            make_upload_file(valid_pdf_one, "Doc1.pdf"),
            make_upload_file(valid_pdf_two, "Doc2.pdf"),
        ]
        output, filename = await service.merge_pdfs(files=files, filename="merged")

        assert isinstance(output, io.BytesIO)
        assert output.read(4) == b"%PDF"

    async def test_merge_returns_correct_filename(
        self, service: MergeService, valid_pdf_one: bytes, valid_pdf_two: bytes
    ):
        """The returned filename has .pdf appended correctly."""
        files = [
            make_upload_file(valid_pdf_one, "Doc1.pdf"),
            make_upload_file(valid_pdf_two, "Doc2.pdf"),
        ]
        _, filename = await service.merge_pdfs(files=files, filename="my-document")

        assert filename == "my-document.pdf"

    async def test_merge_default_filename(
        self, service: MergeService, valid_pdf_one: bytes, valid_pdf_two: bytes
    ):
        """When no filename is provided the default is merged.pdf."""
        files = [
            make_upload_file(valid_pdf_one, "Doc1.pdf"),
            make_upload_file(valid_pdf_two, "Doc2.pdf"),
        ]
        _, filename = await service.merge_pdfs(files=files, filename="merged")

        assert filename == "merged.pdf"

    async def test_merge_three_valid_pdfs(
        self,
        service: MergeService,
        valid_pdf_one: bytes,
        valid_pdf_two: bytes,
        valid_pdf_three: bytes,
    ):
        """A successful merge of three valid PDFs returns a byte stream."""
        files = [
            make_upload_file(valid_pdf_one, "Doc1.pdf"),
            make_upload_file(valid_pdf_two, "Doc2.pdf"),
            make_upload_file(valid_pdf_three, "Doc3.pdf"),
        ]
        output, filename = await service.merge_pdfs(files=files, filename="merged")

        assert isinstance(output, io.BytesIO)
        assert output.read(4) == b"%PDF"

    async def test_too_few_files_raises_exception(
        self, service: MergeService, valid_pdf_one: bytes
    ):
        """Fewer than two files raises MergeTooFewDocuments."""
        files = [make_upload_file(valid_pdf_one, "Doc1.pdf")]

        with pytest.raises(MergeTooFewDocuments):
            await service.merge_pdfs(files=files, filename="merged")

    async def test_invalid_pdf_raises_exception(
        self, service: MergeService, valid_pdf_one: bytes, invalid_pdf: bytes
    ):
        """An invalid PDF file raises MergeInvalidPDFDocument."""
        files = [
            make_upload_file(valid_pdf_one, "Doc1.pdf"),
            make_upload_file(invalid_pdf, "Doc4-invalid.pdf"),
        ]

        with pytest.raises(MergeInvalidPDFDocument):
            await service.merge_pdfs(files=files, filename="merged")

    async def test_empty_pdf_raises_exception(
        self, service: MergeService, valid_pdf_one: bytes, empty_pdf: bytes
    ):
        """An empty PDF file raises MergeInvalidPDFDocument."""
        files = [
            make_upload_file(valid_pdf_one, "Doc1.pdf"),
            make_upload_file(empty_pdf, "Doc5-empty.pdf"),
        ]

        with pytest.raises(MergeInvalidPDFDocument):
            await service.merge_pdfs(files=files, filename="merged")
