"""
Cloud Run optimized configuration for HarvestHub FastAPI
Ensures consistent ML model predictions and performance
"""
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os


class CloudRunSettings(BaseSettings):
    """Cloud Run optimized settings"""
    
    # API Configuration
    API_TITLE: str = "HarvestHub Pest Detection API"
    API_DESCRIPTION: str = "AI-powered multilingual pest detection and recommendation system"
    API_VERSION: str = "3.0.0"
    
    # Server Configuration - Optimized for Cloud Run
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "8000"))
    WORKERS: int = 1  # Single worker for Cloud Run
    RELOAD: bool = False
    LOG_LEVEL: str = "info"
    
    # CORS Configuration
    ALLOWED_ORIGINS: Union[List[str], str] = ["*"]
    ALLOWED_METHODS: Union[List[str], str] = ["*"]
    ALLOWED_HEADERS: Union[List[str], str] = ["*"]
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: set = {"png", "jpg", "jpeg", "gif", "bmp"}
    
    # Model Configuration - Optimized for consistent predictions
    MODEL_PATH: str = "app/data/model.h5"
    LABELS_PATH: str = "app/data/labels.txt"
    IMAGE_SIZE: tuple = (224, 224)
    
    # TensorFlow Configuration for consistency
    TF_CPP_MIN_LOG_LEVEL: str = "2"
    TF_ENABLE_ONEDNN_OPTS: str = "0"
    PYTHONHASHSEED: str = "0"
    
    # External API Configuration
    GEMINI_API_KEY: Optional[str] = None
    FIREBASE_KEY_PATH: str = "app/firebase-key.json"
    
    # Cache Configuration
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    
    # Environment
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    
    # Supported languages
    SUPPORTED_LANGUAGES: dict = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'bn': 'Bengali',
        'pa': 'Punjabi',
        'or': 'Odia',
        'as': 'Assamese'
    }
    
    @field_validator('ALLOWED_ORIGINS', mode='before')
    @classmethod
    def validate_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @field_validator('ALLOWED_METHODS', mode='before')
    @classmethod
    def validate_methods(cls, v):
        if isinstance(v, str):
            return [method.strip() for method in v.split(',')]
        return v
    
    @field_validator('ALLOWED_HEADERS', mode='before')
    @classmethod
    def validate_headers(cls, v):
        if isinstance(v, str):
            return [header.strip() for header in v.split(',')]
        return v
    
    class Config:
        env_file = ".env.production"
        case_sensitive = True


# Use CloudRunSettings for production deployment
if os.getenv("ENVIRONMENT") == "production":
    from app.core.config import Settings
    # Override settings class
    settings = CloudRunSettings()
else:
    from app.core.config import settings
