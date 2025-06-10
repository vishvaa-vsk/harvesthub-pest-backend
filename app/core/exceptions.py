"""
Custom exceptions for HarvestHub application
"""
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse


class HarvestHubException(Exception):
    """Base exception class for HarvestHub"""
    pass


class ModelException(HarvestHubException):
    """Raised when model operations fail"""
    pass


class ValidationException(HarvestHubException):
    """Raised when validation fails"""
    pass


class ExternalAPIException(HarvestHubException):
    """Raised when external API calls fail"""
    pass


class CacheException(HarvestHubException):
    """Raised when cache operations fail"""
    pass


# HTTP Exception shortcuts
def http_400_bad_request(detail: str = "Bad Request") -> HTTPException:
    return HTTPException(status_code=400, detail=detail)


def http_404_not_found(detail: str = "Not Found") -> HTTPException:
    return HTTPException(status_code=404, detail=detail)


def http_422_unprocessable_entity(detail: str = "Unprocessable Entity") -> HTTPException:
    return HTTPException(status_code=422, detail=detail)


def http_500_internal_server_error(detail: str = "Internal Server Error") -> HTTPException:
    return HTTPException(status_code=500, detail=detail)


# Exception handlers
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "path": str(request.url.path)
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc),
            "path": str(request.url.path)
        }
    )


def add_exception_handlers(app: FastAPI) -> None:
    """Add custom exception handlers to FastAPI app"""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
