"""
Prediction related schemas
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PredictionResponse(BaseModel):
    """Model prediction response"""
    label: str
    confidence: float
    index: int
    timestamp: str


class LanguageInfo(BaseModel):
    """Language information"""
    code: str
    name: str


class RecommendationData(BaseModel):
    """Pest management recommendation data"""
    diagnosis: str
    causal_agent: str
    treatments: List[str]


class PredictionResult(BaseModel):
    """Complete prediction result with recommendations"""
    status: str
    prediction: PredictionResponse
    recommendation: RecommendationData
    language: LanguageInfo
    source: str
    timestamp: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "prediction": {
                    "label": "Tomato Late Blight",
                    "confidence": 0.95,
                    "index": 3,
                    "timestamp": "2025-06-10T19:30:00"
                },
                "recommendation": {
                    "diagnosis": "Late blight is a serious disease affecting tomato plants...",
                    "causal_agent": "Phytophthora infestans (fungus)",
                    "treatments": [
                        "Apply copper-based fungicide",
                        "Improve air circulation",
                        "Remove affected leaves",
                        "Avoid overhead watering"
                    ]
                },
                "language": {
                    "code": "en",
                    "name": "English"
                },
                "source": "gemini",
                "timestamp": "2025-06-10T19:30:00"
            }
        }
