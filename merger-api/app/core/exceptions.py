from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ApiException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers={"X-Error-Code": error_code},
        )


def add_exception_handlers(app: FastAPI) -> None:
    """
    Set all exception handlers to app object.
    """

    # Handle generic Exceptions
    @app.exception_handler(Exception)
    async def _generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
        return JSONResponse(
            status_code=status_code,
            content={
                "status_code": status_code,
                "type": "Exception",
                "message": "An unexpected error occurred",
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
                "errors": _format_errors(errors=exc.errors()),
                "path": request.url.path,
            },
        )

    # Handle domain / api exceptions
    @app.exception_handler(ApiException)
    async def _api_exception_handler(
        request: Request, exc: ApiException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status_code": exc.status_code,
                "type": type(exc).__name__,
                "message": exc.detail,
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
