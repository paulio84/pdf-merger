from fastapi import APIRouter

from app.health_check.routes import router as health_check_router
from app.merge.routes import router as merge_router

api_router = APIRouter(prefix="/api")
api_router.include_router(router=health_check_router, tags=["health check"])
api_router.include_router(router=merge_router, tags=["merge"])
