"""
Schema modules for the HarvestHub API
"""

from .responses import (
    HealthResponse,
    DetailedHealthResponse,
    LanguagesResponse,
    ErrorResponse,
    StatusResponse
)

from .requests import PredictionRequest

from .prediction import (
    PredictionResponse,
    LanguageInfo,
    RecommendationData,
    PredictionResult
)

__all__ = [
    "HealthResponse",
    "DetailedHealthResponse", 
    "LanguagesResponse",
    "ErrorResponse",
    "StatusResponse",
    "PredictionRequest",
    "PredictionResponse",
    "LanguageInfo",
    "RecommendationData",
    "PredictionResult"
]
