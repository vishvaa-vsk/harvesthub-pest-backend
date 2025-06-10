"""
HarvestHub Pest Detection API - Cloud Run Optimized FastAPI Application
Ensures consistent ML model predictions with optimized configuration
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# Set TensorFlow configuration before importing TensorFlow
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
os.environ.setdefault('TF_ENABLE_ONEDNN_OPTS', '0')
os.environ.setdefault('PYTHONHASHSEED', '0')

# Configure TensorFlow for deterministic behavior
import tensorflow as tf
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)

from app.api.routes import health, prediction, languages, docs
from app.core.config import settings
from app.core.exceptions import add_exception_handlers
from app.core.middleware import add_custom_middleware
from app.services.model_service import ModelService

# Configure logging for Cloud Run
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler optimized for Cloud Run"""
    # Startup
    logger.info("🚀 HarvestHub FastAPI server starting up on Cloud Run...")
    
    # Initialize model service with optimized settings
    model_service = ModelService()
    await model_service.initialize()
    
    # Store in app state
    app.state.model_service = model_service
    
    # Log initialization status
    logger.info(f"📊 Model loaded: {model_service.is_model_loaded()}")
    logger.info(f"🏷️ Labels loaded: {model_service.get_total_classes()} classes")
    logger.info(f"🌐 Supported languages: {len(settings.SUPPORTED_LANGUAGES)}")
    logger.info("✅ FastAPI server ready for Cloud Run!")
    
    yield
    
    # Shutdown
    logger.info("🛑 HarvestHub FastAPI server shutting down...")


# Create FastAPI application with Cloud Run optimizations
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

# Add middleware with Cloud Run optimizations
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
    """Root endpoint with Cloud Run deployment info"""
    return {
        "message": "HarvestHub Pest Detection API",
        "version": settings.API_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "deployment": "Cloud Run",
        "docs": "/docs",
        "health": "/health"
    }


# Cloud Run health check endpoint
@app.get("/_health", include_in_schema=False)
async def cloud_run_health():
    """Health check endpoint specifically for Cloud Run"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_cloudrun:app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        access_log=True,
        loop="uvloop",
        http="httptools"
    )
