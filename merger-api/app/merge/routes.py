from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import StreamingResponse

from app.core.config import get_settings
from app.core.rate_limiting import limiter
from app.merge.dependencies import get_merge_service
from app.merge.service import MergeService

router = APIRouter(prefix="/merge")
settings = get_settings()


# There are no schemas involved in this route.
# Multipart form data with file uploads can't be modelled as a Pydantic BaseModel for the request.
# FastAPI handles UploadFile fields directly in the route signature.
# The success response is a StreamingResponse which can't be modelled as a Pydantic schema.
# It's a raw binary stream, used for the attachment.
@router.post("", include_in_schema=False)
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
@limiter.limit(settings.rate_limit)
async def merge(
    request: Request,
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
