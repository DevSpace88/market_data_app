from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from ...models.database import get_db
from ...auth import get_current_active_user
from ...models.user import User
from ...schemas.ai_settings import (
    AISettingsUpdate, 
    AISettingsResponse, 
    AIProviderInfo,
    AI_PROVIDERS
)
from ...services.ai_provider_service import ai_provider_service

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/providers", response_model=Dict[str, AIProviderInfo])
async def get_ai_providers():
    """Get available AI providers and their information"""
    return AI_PROVIDERS

@router.get("/", response_model=AISettingsResponse)
async def get_ai_settings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's AI settings"""
    return AISettingsResponse(
        ai_provider=current_user.ai_provider,
        ai_model=current_user.ai_model,
        ai_temperature=float(current_user.ai_temperature),
        ai_max_tokens=current_user.ai_max_tokens,
        has_api_key=bool(current_user.ai_api_key)
    )

@router.put("/", response_model=AISettingsResponse)
async def update_ai_settings(
    settings: AISettingsUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update user's AI settings"""
    try:
        # Update AI settings
        current_user.ai_provider = settings.ai_provider.value
        current_user.ai_model = settings.ai_model
        current_user.ai_temperature = str(settings.ai_temperature)
        current_user.ai_max_tokens = settings.ai_max_tokens
        
        # Store API key in plaintext if provided
        if settings.ai_api_key:
            current_user.ai_api_key = settings.ai_api_key
        
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"Updated AI settings for user {current_user.username}")
        
        return AISettingsResponse(
            ai_provider=current_user.ai_provider,
            ai_model=current_user.ai_model,
            ai_temperature=float(current_user.ai_temperature),
            ai_max_tokens=current_user.ai_max_tokens,
            has_api_key=bool(current_user.ai_api_key)
        )
        
    except Exception as e:
        logger.error(f"Failed to update AI settings for user {current_user.username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update AI settings")

@router.post("/test-connection")
async def test_ai_connection(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Test AI provider connection"""
    try:
        if not current_user.ai_api_key:
            raise HTTPException(status_code=400, detail="No API key configured")
        
        # Read API key directly (no encryption)
        api_key = current_user.ai_api_key
        
        # Test connection
        result = ai_provider_service.test_api_connection(
            provider=current_user.ai_provider,
            model=current_user.ai_model,
            api_key=api_key
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to test AI connection for user {current_user.username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to test connection")

@router.delete("/api-key")
async def clear_api_key(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear user's API key"""
    try:
        current_user.ai_api_key = None
        db.commit()
        
        logger.info(f"Cleared API key for user {current_user.username}")
        
        return {"message": "API key cleared successfully"}
        
    except Exception as e:
        logger.error(f"Failed to clear API key for user {current_user.username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear API key")
