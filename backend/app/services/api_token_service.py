"""
API Token Service for secure API key management using reference tokens.

Instead of storing API keys directly, we:
1. Generate a unique reference token
2. Encrypt the API key with Fernet
3. Store the encrypted key with the reference token
4. Return only the reference token to the client
"""
import secrets
import hashlib
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.user import User
from app.middleware.encryption import encrypt_api_key, decrypt_api_key


class APITokenService:
    """
    Service for managing API keys using reference tokens.

    This provides a more secure alternative to storing API keys directly:
    - Keys are encrypted at rest using Fernet
    - Only reference tokens are exposed to clients
    - Tokens can be rotated without changing the actual key
    """

    # Token format: "tok_" + 32 random characters (base64)
    TOKEN_PREFIX = "tok_"
    TOKEN_LENGTH = 32

    @staticmethod
    def generate_token() -> str:
        """
        Generate a unique reference token.

        Returns:
            A token in format "tok_<random_base64>"
        """
        random_bytes = secrets.token_bytes(APITokenService.TOKEN_LENGTH)
        token_hash = hashlib.sha256(random_bytes).hexdigest()[:APITokenService.TOKEN_LENGTH]
        return f"{APITokenService.TOKEN_PREFIX}{token_hash}"

    @staticmethod
    def is_valid_token_format(token: str) -> bool:
        """Check if token has valid format."""
        if not token:
            return False
        return token.startswith(APITokenService.TOKEN_PREFIX) and len(token) > len(APITokenService.TOKEN_PREFIX)

    @staticmethod
    def store_api_key(db: Session, user: User, api_key: str) -> str:
        """
        Encrypt and store an API key, returning a reference token.

        Args:
            db: Database session
            user: User object
            api_key: The plaintext API key to store

        Returns:
            Reference token for the stored key

        Raises:
            ValueError: If api_key is empty
        """
        if not api_key:
            raise ValueError("API key cannot be empty")

        # Generate unique token
        token = APITokenService.generate_token()

        # Check for token collision (very unlikely)
        existing = db.query(User).filter(User.api_key_token == token).first()
        while existing:
            token = APITokenService.generate_token()
            existing = db.query(User).filter(User.api_key_token == token).first()

        # Encrypt the API key
        encrypted_key = encrypt_api_key(api_key)

        # Store encrypted key and token
        user.api_key_token = token
        user.ai_api_key = encrypted_key
        db.commit()

        return token

    @staticmethod
    def get_api_key(db: Session, user: User) -> Optional[str]:
        """
        Retrieve and decrypt API key using reference token.

        Args:
            db: Database session
            user: User object with api_key_token

        Returns:
            Decrypted API key or None if not found

        Raises:
            ValueError: If token is invalid or decryption fails
        """
        if not user.api_key_token:
            return None

        if not user.ai_api_key:
            return None

        try:
            # Decrypt the stored key
            return decrypt_api_key(user.ai_api_key)
        except Exception as e:
            raise ValueError(f"Failed to decrypt API key: {str(e)}")

    @staticmethod
    def rotate_token(db: Session, user: User) -> str:
        """
        Rotate the reference token without changing the API key.

        Args:
            db: Database session
            user: User object

        Returns:
            New reference token

        Raises:
            ValueError: If no API key is stored
        """
        if not user.api_key_token or not user.ai_api_key:
            raise ValueError("No API key to rotate")

        # Generate new token
        new_token = APITokenService.generate_token()

        # Update token (keep encrypted key the same)
        user.api_key_token = new_token
        db.commit()

        return new_token

    @staticmethod
    def delete_api_key(db: Session, user: User) -> None:
        """
        Delete the stored API key and token.

        Args:
            db: Database session
            user: User object
        """
        user.api_key_token = None
        user.ai_api_key = None
        db.commit()

    @staticmethod
    def has_api_key(user: User) -> bool:
        """Check if user has an API key stored."""
        return bool(user.api_key_token and user.ai_api_key)

    @staticmethod
    def migrate_legacy_key(db: Session, user: User) -> Optional[str]:
        """
        Migrate a legacy plaintext API key to encrypted token system.

        This handles the transition from the old plaintext system.
        If a user has an ai_api_key but no api_key_token, this will:
        1. Check if the key is already encrypted
        2. If plaintext, encrypt it and create a token
        3. Return the new token

        Args:
            db: Database session
            user: User object

        Returns:
            Reference token or None if no migration needed
        """
        # Skip if already has token
        if user.api_key_token:
            return None

        # Skip if no API key
        if not user.ai_api_key:
            return None

        # Check if key is already encrypted (Fernet tokens are base64-like)
        # If it fails decryption, assume it's plaintext
        try:
            decrypt_api_key(user.ai_api_key)
            # Successfully decrypted, just need a token
            token = APITokenService.generate_token()
            user.api_key_token = token
            db.commit()
            return token
        except Exception:
            # Decryption failed, assume plaintext and encrypt
            try:
                plaintext_key = user.ai_api_key
                token = APITokenService.store_api_key(db, user, plaintext_key)
                return token
            except Exception as e:
                raise ValueError(f"Failed to migrate API key: {str(e)}")


# Singleton instance
_api_token_service: Optional[APITokenService] = None


def get_api_token_service() -> APITokenService:
    """Get or create the singleton API token service instance."""
    global _api_token_service
    if _api_token_service is None:
        _api_token_service = APITokenService()
    return _api_token_service
