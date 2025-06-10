"""
Configuration settings for HarvestHub FastAPI application
"""
import os
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_TITLE: str = "HarvestHub Pest Detection API"
    API_DESCRIPTION: str = "AI-powered multilingual pest detection and recommendation system"
    API_VERSION: str = "3.0.0"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    RELOAD: bool = False
    LOG_LEVEL: str = "info"
    
    # CORS Configuration
    ALLOWED_ORIGINS: Union[List[str], str] = ["*"]
    ALLOWED_METHODS: Union[List[str], str] = ["*"]
    ALLOWED_HEADERS: Union[List[str], str] = ["*"]
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: set = {"png", "jpg", "jpeg", "gif", "bmp"}
    
    # Model Configuration
    MODEL_PATH: str = "app/data/model.h5"
    LABELS_PATH: str = "app/data/labels.txt"
    IMAGE_SIZE: tuple = (224, 224)
    
    # External API Configuration
    GEMINI_API_KEY: Optional[str] = None
    FIREBASE_KEY_PATH: str = "app/firebase-key.json"
    
    # Cache Configuration
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # 1 hour
    
    # Environment
    ENVIRONMENT: str = "development"
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
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    @field_validator('ALLOWED_METHODS', mode='before')
    @classmethod
    def parse_cors_methods(cls, v):
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            return [method.strip() for method in v.split(",") if method.strip()]
        return v
    
    @field_validator('ALLOWED_HEADERS', mode='before')
    @classmethod
    def parse_cors_headers(cls, v):
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            return [header.strip() for header in v.split(",") if header.strip()]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Supported languages configuration
SUPPORTED_LANGUAGES = {
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

# Language mappings for Gemini prompts
LANGUAGE_NAMES = {
    'en': 'English',
    'hi': 'Hindi (हिन्दी)',
    'ta': 'Tamil (தமிழ்)',
    'te': 'Telugu (తెలుగు)',
    'kn': 'Kannada (ಕನ್ನಡ)',
    'ml': 'Malayalam (മലയാളം)',
    'mr': 'Marathi (मराठी)',
    'gu': 'Gujarati (ગુજરાતી)',
    'bn': 'Bengali (বাংলা)',
    'pa': 'Punjabi (ਪੰਜਾਬੀ)',
    'or': 'Odia (ଓଡ଼ିଆ)',
    'as': 'Assamese (অসমীয়া)'
}
