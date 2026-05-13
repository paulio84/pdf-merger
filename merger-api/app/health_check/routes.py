from http import HTTPStatus

from fastapi import APIRouter

from app.health_check.schemas import HealthCheckResponse

router = APIRouter(prefix="/health")

@router.get("/", response_model=HealthCheckResponse, status_code=HTTPStatus.OK.value)
async def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(healthy="Yes!")
