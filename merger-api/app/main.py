from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.exceptions import add_exception_handlers
from app.core.logging import setup_logging
from app.core.rate_limiting import setup_rate_limiting
from app.router import api_router


def create_application() -> FastAPI:
    """Create and configure a FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        debug=settings.debug,
        docs_url="/api/docs" if settings.debug else None,
        redoc_url="/api/redoc" if settings.debug else None,
        title=settings.app_name,
    )

    setup_logging()
    setup_rate_limiting(app)
    # setup CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )
    add_exception_handlers(app)

    app.include_router(api_router)

    return app


app = create_application()
