"""
Recommendation service for pest management advice
"""
import asyncio
from typing import Dict, Any, Optional

from app.core.config import settings, LANGUAGE_NAMES
from app.core.exceptions import ExternalAPIException
from app.helpers_async import (
    get_pest_recommendation_async as get_recommendation,
    get_from_firestore_cache_async,
    cache_to_firestore_async,
    generate_gemini_recommendation_async,
    get_fallback_recommendation
)


class RecommendationService:
    """Service for handling pest management recommendations"""
    
    def __init__(self):
        """Initialize recommendation service"""
        self.cache_enabled = settings.CACHE_ENABLED
        self.cache_ttl = settings.CACHE_TTL
    
    async def get_recommendation_async(self, pest_label: str, language_code: str) -> Dict[str, Any]:
        """
        Get pest management recommendation for given pest and language
        
        Args:
            pest_label: The pest/disease label from model prediction
            language_code: Language code for the recommendation
            
        Returns:
            Dictionary containing recommendation data and metadata
        """
        try:
            # Validate language
            if language_code not in settings.SUPPORTED_LANGUAGES:
                raise ValueError(f"Unsupported language: {language_code}")
            
            # Get recommendation using the existing async helper
            recommendation = await get_recommendation(pest_label, language_code)
            
            return recommendation
            
        except Exception as e:
            print(f"Error getting recommendation: {e}")
            # Return fallback recommendation
            fallback = get_fallback_recommendation(pest_label, language_code)
            return {'data': fallback, 'source': 'fallback'}

    async def get_recommendation(self, pest_label: str, language_code: str) -> Dict[str, Any]:
        """Alias for backward compatibility"""
        return await self.get_recommendation_async(pest_label, language_code)
    
    async def get_cached_recommendation(self, pest_label: str, language_code: str) -> Optional[Dict[str, Any]]:
        """
        Get recommendation from cache
        
        Args:
            pest_label: The pest/disease label
            language_code: Language code
            
        Returns:
            Cached recommendation data or None
        """
        if not self.cache_enabled:
            return None
        
        cache_key = f"{pest_label}::{language_code}"
        return await get_from_firestore_cache_async(cache_key)
    
    async def cache_recommendation(self, pest_label: str, language_code: str, recommendation: Dict[str, Any]) -> None:
        """
        Cache recommendation for future use
        
        Args:
            pest_label: The pest/disease label
            language_code: Language code
            recommendation: Recommendation data to cache
        """
        if not self.cache_enabled:
            return
        
        cache_key = f"{pest_label}::{language_code}"
        await cache_to_firestore_async(cache_key, recommendation)
    
    async def generate_new_recommendation(self, pest_label: str, language_code: str) -> Optional[Dict[str, Any]]:
        """
        Generate new recommendation using Gemini AI
        
        Args:
            pest_label: The pest/disease label
            language_code: Language code
            
        Returns:
            Generated recommendation data or None if failed
        """
        try:
            return await generate_gemini_recommendation_async(pest_label, language_code)
        except Exception as e:
            print(f"Error generating recommendation with Gemini: {e}")
            return None
    
    def get_fallback_recommendation(self, pest_label: str, language_code: str) -> Dict[str, Any]:
        """
        Get fallback recommendation when other methods fail
        
        Args:
            pest_label: The pest/disease label
            language_code: Language code
            
        Returns:
            Fallback recommendation data
        """
        return get_fallback_recommendation(pest_label, language_code)
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return settings.SUPPORTED_LANGUAGES
    
    def is_language_supported(self, language_code: str) -> bool:
        """Check if language is supported"""
        return language_code in settings.SUPPORTED_LANGUAGES