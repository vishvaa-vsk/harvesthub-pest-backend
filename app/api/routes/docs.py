"""
Documentation and utility endpoints
"""
from fastapi import APIRouter

router = APIRouter(prefix="/docs-info", tags=["Documentation"])


@router.get("")
async def docs_info():
    """Information about API documentation"""
    return {
        "message": "Visit /docs for interactive API documentation",
        "swagger_ui": "/docs",
        "redoc": "/redoc",
        "openapi_json": "/openapi.json",
        "postman_collection": "/docs#/",
        "api_version": "3.0.0"
    }
