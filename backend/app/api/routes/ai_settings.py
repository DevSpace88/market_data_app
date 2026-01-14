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
from ...services.api_token_service import APITokenService

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
    # Migrate legacy key if needed
    if current_user.ai_api_key and not current_user.api_key_token:
        try:
            APITokenService.migrate_legacy_key(db, current_user)
        except Exception as e:
            logger.warning(f"Failed to migrate legacy API key for user {current_user.username}: {e}")

    return AISettingsResponse(
        ai_provider=current_user.ai_provider,
        ai_model=current_user.ai_model,
        ai_temperature=float(current_user.ai_temperature),
        ai_max_tokens=current_user.ai_max_tokens,
        has_api_key=APITokenService.has_api_key(current_user)
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

        logger.info(f"[AI SETTINGS DEBUG] Received settings for user {current_user.username}")
        logger.info(f"[AI SETTINGS DEBUG] ai_provider: {settings.ai_provider.value}")
        logger.info(f"[AI SETTINGS DEBUG] ai_model: {settings.ai_model}")
        logger.info(f"[AI SETTINGS DEBUG] ai_api_key provided: {bool(settings.ai_api_key)}")
        if settings.ai_api_key:
            logger.info(f"[AI SETTINGS DEBUG] ai_api_key length: {len(settings.ai_api_key)}")

        # Store API key with encryption if provided
        if settings.ai_api_key:
            APITokenService.store_api_key(db, current_user, settings.ai_api_key)
            logger.info(f"Stored API key for user {current_user.username}")

        db.commit()
        db.refresh(current_user)

        logger.info(f"Updated AI settings for user {current_user.username}")

        return AISettingsResponse(
            ai_provider=current_user.ai_provider,
            ai_model=current_user.ai_model,
            ai_temperature=float(current_user.ai_temperature),
            ai_max_tokens=current_user.ai_max_tokens,
            has_api_key=APITokenService.has_api_key(current_user)
        )

    except ValueError as e:
        logger.error(f"Failed to update AI settings for user {current_user.username}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to update AI settings for user {current_user.username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update AI settings")


@router.post("/test-connection")
async def test_ai_connection(
    settings: AISettingsUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Test AI provider connection.

    Accepts settings in request body to test before saving.
    """
    try:
        if not settings.ai_api_key:
            raise HTTPException(status_code=400, detail="API key is required for testing")

        # Test connection with provided key
        result = ai_provider_service.test_api_connection(
            provider=settings.ai_provider.value,
            model=settings.ai_model,
            api_key=settings.ai_api_key
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to test AI connection for user {current_user.username}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to test connection: {str(e)}")


@router.delete("/api-key")
async def clear_api_key(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Clear user's API key"""
    try:
        APITokenService.delete_api_key(db, current_user)

        logger.info(f"Cleared API key for user {current_user.username}")

        return {"message": "API key cleared successfully"}

    except Exception as e:
        logger.error(f"Failed to clear API key for user {current_user.username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear API key")


@router.post("/rotate-token")
async def rotate_api_token(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Rotate the API key reference token.

    This generates a new token without changing the actual API key.
    Useful if the token is accidentally exposed.
    """
    try:
        new_token = APITokenService.rotate_token(db, current_user)

        logger.info(f"Rotated API token for user {current_user.username}")

        return {
            "message": "API token rotated successfully",
            "token": new_token
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to rotate API token for user {current_user.username}: {e}")
        raise HTTPException(status_code=500, detail="Failed to rotate token")
