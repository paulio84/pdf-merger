from fastapi import FastAPI

from app.core.config import settings
from app.router import api_router


def create_application() -> FastAPI:
    """Create and configure a FastAPI application."""
    app = FastAPI(
        debug=settings.DEBUG,
        docs_url="/api/docs" if settings.DEBUG else None,
        redoc_url="/api/redoc" if settings.DEBUG else None,
        title=settings.APP_NAME,
    )

    app.include_router(api_router)
    # add_exception_handlers(app)

    return app

app = create_application()
