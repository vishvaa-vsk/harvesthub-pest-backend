"""
API dependency injection for HarvestHub application
"""
from fastapi import Depends, HTTPException, UploadFile, File
from typing import Optional

from app.core.config import settings
from app.services.model_service import ModelService
from app.services.recommendation_service import RecommendationService


# Service dependencies
def get_model_service() -> ModelService:
    """Get model service instance"""
    return ModelService()


def get_recommendation_service() -> RecommendationService:
    """Get recommendation service instance"""
    return RecommendationService()


# Validation dependencies
def validate_language(lang: str) -> str:
    """
    Validate language code
    
    Args:
        lang: Language code to validate
    
    Returns:
        str: Validated language code
    
    Raises:
        HTTPException: If language is not supported
    """
    if lang not in settings.SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language code: {lang}. "
            f"Supported languages: {list(settings.SUPPORTED_LANGUAGES.keys())}"
        )
    return lang


def validate_image_file(file: UploadFile = File(...)) -> UploadFile:
    """
    Validate uploaded image file
    
    Args:
        file: Uploaded file to validate
    
    Returns:
        UploadFile: Validated file
    
    Raises:
        HTTPException: If file validation fails
    """
    # Check if file is provided
    if not file.filename:
        raise HTTPException(status_code=400, detail="No image file selected")
    
    # Check file extension
    if file.filename:
        file_extension = file.filename.rsplit('.', 1)[-1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            allowed = ", ".join(settings.ALLOWED_EXTENSIONS).upper()
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Supported: {allowed}"
            )
    
    return file
