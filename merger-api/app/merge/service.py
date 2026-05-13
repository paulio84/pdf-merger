import io

from fastapi import UploadFile
from pypdf import PdfWriter


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
        """
        writer = PdfWriter()

        for file in files:
            # Read the uploaded file contents into memory and append to the writer.
            content = await file.read()
            writer.append(io.BytesIO(content))

        # Write the merged PDF to an in-memory byte stream.
        output = io.BytesIO()
        writer.write(output)

        # Reset the stream position to the beginning so it can be read by the caller.
        output.seek(0)

        return output, f"{filename}.pdf"
