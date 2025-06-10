"""
Response schemas for API endpoints
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class HealthResponse(BaseModel):
    """Response model for basic health check"""
    status: str
    message: str
    version: str
    features: List[str]


class DetailedHealthResponse(BaseModel):
    """Response model for detailed health check"""
    status: str
    health: Dict[str, Any]


class LanguagesResponse(BaseModel):
    """Response model for supported languages"""
    status: str
    supported_languages: Dict[str, str]
    total_languages: int


class ErrorResponse(BaseModel):
    """Response model for error responses"""
    status: str
    message: str
    detail: Optional[str] = None
    path: Optional[str] = None


class StatusResponse(BaseModel):
    """Response model for status endpoint"""
    status: str
    framework: str
    version: str
    timestamp: str
