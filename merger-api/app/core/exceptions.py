import logging
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger(__name__)


class ApiException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


def add_exception_handlers(app: FastAPI) -> None:
    """
    Set all exception handlers to app object.
    """

    # Handle generic Exceptions
    @app.exception_handler(Exception)
    async def _generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error(
            "An unexpected error occurred",
            extra={"path": request.url.path},
            exc_info=True,
        )
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
        return JSONResponse(
            status_code=status_code,
            content={
                "status_code": status_code,
                "type": "Exception",
                "message": "An unexpected error occurred",
                "error_code": "INTERNAL_SERVER_ERROR",
                "errors": None,
                "path": request.url.path,
            },
        )

    # Handle Pydantic validation exceptions
    @app.exception_handler(RequestValidationError)
    async def _validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        status_code = HTTPStatus.UNPROCESSABLE_ENTITY.value
        return JSONResponse(
            status_code=status_code,
            content={
                "status_code": status_code,
                "type": "RequestValidationError",
                "message": "Schema validation error",
                "error_code": "VALIDATION_ERROR",
                "errors": _format_errors(errors=list(exc.errors())),
                "path": request.url.path,
            },
        )

    # Handle domain / api exceptions
    @app.exception_handler(ApiException)
    async def _api_exception_handler(
        request: Request, exc: ApiException
    ) -> JSONResponse:
        logger.warning(
            "API exception raised",
            extra={
                "path": request.url.path,
                "status_code": exc.status_code,
                "error_code": exc.error_code,
                "detail": exc.detail,
            },
        )
        return JSONResponse(
            status_code=exc.status_code,
            headers={"X-Error-Code": exc.error_code},
            content={
                "status_code": exc.status_code,
                "type": type(exc).__name__,
                "message": exc.detail,
                "error_code": exc.error_code,
                "errors": None,
                "path": request.url.path,
            },
        )

    # Handle rate limit exceptions
    @app.exception_handler(RateLimitExceeded)
    async def _rate_limit_handler(
        request: Request, exc: RateLimitExceeded
    ) -> JSONResponse:
        logger.warning(
            "Rate limit exceeded",
            extra={
                "path": request.url.path,
                "status_code": exc.status_code,
                "error_code": "RATE_LIMIT_EXCEEDED",
                "detail": exc.detail,
                "source": "rate_limiter",
            },
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status_code": exc.status_code,
                "type": type(exc).__name__,
                "message": "Too many requests made. Please try again later.",
                "error_code": "RATE_LIMIT_EXCEEDED",
                "errors": None,
                "path": request.url.path,
            },
        )


def _format_errors(errors: list) -> dict[str, list[str]]:
    """
    Format errors from Pydantic validation errors.
    """
    result: dict[str, list[str]] = {}
    for error in errors:
        field: str = error["loc"][-1]
        message: str = error.get("ctx", {}).get("reason") or error["msg"]
        result[field] = []
        result[field].append(message.lower())
    return result
