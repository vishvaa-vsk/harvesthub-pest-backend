"""
Request schemas for API endpoints
"""
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import UploadFile


class PredictionRequest(BaseModel):
    """Request model for prediction endpoints"""
    language_code: str = Field(..., description="Language code for recommendations")
    
    class Config:
        json_schema_extra = {
            "example": {
                "language_code": "en"
            }
        }
