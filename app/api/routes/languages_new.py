"""
Language-related endpoints
"""
from fastapi import APIRouter

from app.core.config import settings
from app.schemas.responses import LanguagesResponse

router = APIRouter(prefix="/languages", tags=["Languages"])


@router.get("", response_model=LanguagesResponse)
async def get_supported_languages() -> LanguagesResponse:
    """Get list of supported languages"""
    return LanguagesResponse(
        status="success",
        supported_languages=settings.SUPPORTED_LANGUAGES,
        total_languages=len(settings.SUPPORTED_LANGUAGES)
    )
