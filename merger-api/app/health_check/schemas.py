from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str
    description: str
    version: float
