"""
Health check endpoints
"""
from fastapi import APIRouter, Depends, Request
from datetime import datetime

from app.api.dependencies import get_model_service
from app.core.config import settings
from app.schemas.responses import HealthResponse, DetailedHealthResponse, StatusResponse
from app.services.model_service import ModelService

router = APIRouter(prefix="", tags=["Health"])


@router.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Main health check endpoint"""
    return HealthResponse(
        status="success",
        message="HarvestHub Pest Detection API is running",
        version=settings.API_VERSION,
        features=[
            "Multi-language pest detection",
            "AI-powered recommendations", 
            "Firebase caching",
            f"{len(settings.SUPPORTED_LANGUAGES)} Indian languages supported",
            "Async FastAPI architecture"
        ]
    )


@router.get("/health", response_model=DetailedHealthResponse)
async def detailed_health(
    model_service: ModelService = Depends(get_model_service)
) -> DetailedHealthResponse:
    """Detailed health check endpoint"""
    model_loaded = model_service.is_model_loaded()
    
    return DetailedHealthResponse(
        status="success",
        health={
            "model_loaded": model_loaded,
            "labels_loaded": model_service.get_total_classes() > 0,
            "total_classes": model_service.get_total_classes(),
            "framework": "FastAPI",
            "version": settings.API_VERSION,
            "environment": settings.ENVIRONMENT,
            "supported_languages": len(settings.SUPPORTED_LANGUAGES)
        }
    )


@router.get("/status", response_model=StatusResponse)
async def status() -> StatusResponse:
    """Quick status check"""
    return StatusResponse(
        status="online",
        framework="FastAPI",
        version=settings.API_VERSION,
        timestamp=datetime.utcnow().isoformat()
    )
