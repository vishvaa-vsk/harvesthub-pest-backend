"""
Prediction endpoints
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from io import BytesIO
from datetime import datetime

from app.api.dependencies import (
    get_model_service, get_recommendation_service, 
    validate_language, validate_image_file
)
from app.core.config import settings
from app.schemas.prediction import PredictionResult, PredictionResponse, LanguageInfo, RecommendationData
from app.services.model_service import ModelService
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("/{lang}", response_model=PredictionResult)
async def predict_with_language(
    lang: str = Depends(validate_language),
    file: UploadFile = Depends(validate_image_file),
    model_service: ModelService = Depends(get_model_service),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
) -> PredictionResult:
    """Predict pest/disease with language-specific recommendations"""
    try:
        # Read image file
        image_data = BytesIO(await file.read())
        
        # Get prediction from model
        prediction_result = await model_service.predict_async(image_data)
        
        if not prediction_result:
            raise HTTPException(status_code=500, detail="Model prediction failed")
        
        # Get recommendation
        recommendation_data = await recommendation_service.get_recommendation_async(
            prediction_result['label'], lang
        )
        
        # Format response
        return PredictionResult(
            status="success",
            prediction=PredictionResponse(
                label=prediction_result['label'],
                confidence=prediction_result['confidence'],
                index=prediction_result['index'],
                timestamp=datetime.utcnow().isoformat()
            ),
            recommendation=RecommendationData(
                diagnosis=recommendation_data['data']['diagnosis'],
                causal_agent=recommendation_data['data']['causal_agent'],
                treatments=recommendation_data['data']['treatments']
            ),
            language=LanguageInfo(
                code=lang,
                name=settings.SUPPORTED_LANGUAGES[lang]
            ),
            source=recommendation_data['source'],
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("", response_model=PredictionResult)
async def predict_default(
    file: UploadFile = Depends(validate_image_file),
    model_service: ModelService = Depends(get_model_service),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
) -> PredictionResult:
    """Predict pest/disease with default (English) recommendations"""
    return await predict_with_language("en", file, model_service, recommendation_service)
