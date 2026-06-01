from http import HTTPStatus

from fastapi import APIRouter

from app.health_check.schemas import HealthCheckResponse

router = APIRouter(prefix="/health")


@router.get("/", response_model=HealthCheckResponse, status_code=HTTPStatus.OK.value)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(
        status="Ok!",
        description="A PDF Merger project, to merge multiple PDF documents into a single document.",
        version=1.0,
    )
