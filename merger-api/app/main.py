from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import add_exception_handlers
from app.core.logging import setup_logging
from app.core.rate_limiting import setup_rate_limiting
from app.router import api_router


def create_application() -> FastAPI:
    """Create and configure a FastAPI application."""
    app = FastAPI(
        debug=settings.DEBUG,
        docs_url="/api/docs" if settings.DEBUG else None,
        redoc_url="/api/redoc" if settings.DEBUG else None,
        title=settings.APP_NAME,
    )

    setup_logging()
    setup_rate_limiting(app)
    # setup CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS.split(","),
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    add_exception_handlers(app)

    app.include_router(api_router)

    return app


app = create_application()
