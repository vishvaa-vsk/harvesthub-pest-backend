"""
HarvestHub Pest Detection API - FastAPI Application
A modern, async-first API for multilingual pest detection and recommendations.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.api.routes import health, prediction, languages, docs
from app.core.config import settings
from app.core.exceptions import add_exception_handlers
from app.core.middleware import add_custom_middleware
from app.services.model_service import ModelService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    print("🚀 HarvestHub FastAPI server starting up...")
    
    # Initialize model service
    model_service = ModelService()
    await model_service.initialize()
    
    # Store in app state
    app.state.model_service = model_service
    
    print(f"📊 Model loaded: {model_service.is_model_loaded()}")
    print(f"🏷️ Labels loaded: {model_service.get_total_classes()} classes")
    print(f"🌐 Supported languages: {len(settings.SUPPORTED_LANGUAGES)}")
    print("✅ FastAPI server ready!")
    
    yield
    
    # Shutdown
    print("🛑 HarvestHub FastAPI server shutting down...")
    print("✅ Cleanup completed!")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "HarvestHub Team",
        "email": "support@harvesthub.ai",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Add custom middleware
add_custom_middleware(app)

# Add exception handlers
add_exception_handlers(app)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(prediction.router, tags=["Prediction"])
app.include_router(languages.router, tags=["Languages"])
app.include_router(docs.router, tags=["Documentation"])


# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint redirect to docs"""
    return {
        "message": "Welcome to HarvestHub Pest Detection API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/health",
        "status": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL
    )
