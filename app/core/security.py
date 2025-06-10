"""
Security utilities for HarvestHub application
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional


security = HTTPBearer(auto_error=False)


async def get_api_key(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[str]:
    """
    Extract API key from Authorization header
    Optional for now, can be made required later
    """
    if credentials:
        return credentials.credentials
    return None


def validate_file_type(filename: str, allowed_extensions: set) -> bool:
    """
    Validate file extension
    
    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in allowed_extensions


def validate_file_size(file_size: int, max_size: int) -> bool:
    """
    Validate file size
    
    Args:
        file_size: Size of the file in bytes
        max_size: Maximum allowed size in bytes
    
    Returns:
        bool: True if valid, False otherwise
    """
    return file_size <= max_size
