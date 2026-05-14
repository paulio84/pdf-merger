import io
import logging

from fastapi import UploadFile
from pypdf import PdfWriter
from pypdf.errors import PdfReadError

from app.merge.exceptions import (
    MergeInvalidPDFDocument,
    MergeTooFewDocuments,
)

logger = logging.getLogger(__name__)


class MergeService:
    async def merge_pdfs(
        self, files: list[UploadFile], filename: str
    ) -> tuple[io.BytesIO, str]:
        """
        Merge multiple PDF files into a single PDF.

        Files are merged in the order they are received. The merged PDF is
        returned as an in-memory byte stream alongside the constructed filename.

        Params:
            files: A list of uploaded PDF files to merge.
            filename: The desired name for the merged PDF, without extension.

        Returns:
            A tuple containing:
                - An in-memory byte stream of the merged PDF.
                - The constructed filename with the .pdf extension appended.

        Raises:
            MergeTooFewDocuments: There are fewer than two documents uploaded.
            MergeInvalidPDFDocument: The PDF document is invalid, e.g. the document cannot be read correctly.
        """
        # Validate there are 2 or more documents to merge.
        if len(files) < 2:
            raise MergeTooFewDocuments()

        logger.info(
            "PDF merge started",
            extra={"file_count": len(files), "output_filename": filename},
        )

        writer = PdfWriter()
        for file in files:
            # Read the uploaded file contents into memory and append to the writer.
            content = await file.read()
            # Validate that the first 4 bytes start with '%PDF'
            # this should identify the document as a PDF.
            if not content.startswith(b"%PDF"):
                logger.warning(
                    "Invalid PDF file rejected",
                    extra={
                        "input_filename": file.filename or "unknown",
                        "source": "MergeService.merge_pdfs",
                    },
                )
                raise MergeInvalidPDFDocument(file.filename or "unknown")

            try:
                writer.append(io.BytesIO(content))
            except PdfReadError:
                logger.warning(
                    "Malformed PDF file rejected",
                    extra={
                        "input_filename": file.filename or "unknown",
                        "source": "MergeService.merge_pdfs",
                    },
                )
                raise MergeInvalidPDFDocument(file.filename or "unknown")

        # Write the merged PDF to an in-memory byte stream.
        output = io.BytesIO()
        writer.write(output)

        # Reset the stream position to the beginning so it can be read by the caller.
        output.seek(0)

        logger.info(
            "PDF merge completed successfully",
            extra={"file_count": len(files), "output_filename": f"{filename}.pdf"},
        )

        return output, f"{filename}.pdf"
