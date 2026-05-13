from http import HTTPStatus

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import StreamingResponse

from app.merge.dependencies import get_merge_service
from app.merge.service import MergeService

router = APIRouter(prefix="/merge")


# There are no schemas involved in this route.
# Multipart form data with file uploads can't be modelled as a Pydantic BaseModel for the request.
# FastAPI handles UploadFile fields directly in the route signature.
# Also, the success response is a StreamingResponse which also
# can't be modelled as a Pydantic schema — it's a raw binary stream, used for the attachment.
@router.post(
    "/",
    status_code=HTTPStatus.OK.value,
    responses={
        HTTPStatus.OK.value: {
            "content": {"application/pdf": {}},
            "description": "The merged PDF file",
        }
    },
)
async def merge(
    files: list[UploadFile],
    filename: str = "merged",
    service: MergeService = Depends(get_merge_service),
) -> StreamingResponse:
    output, output_filename = await service.merge_pdfs(files=files, filename=filename)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={output_filename}",
        },
    )
