"""
Main API router that includes all route modules
"""
from fastapi import APIRouter

from app.api.routes import health, languages, prediction, docs

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(health.router)
api_router.include_router(languages.router)
api_router.include_router(prediction.router)
api_router.include_router(docs.router)
