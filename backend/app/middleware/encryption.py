"""
Encryption service for securing API keys and sensitive data.

Uses Fernet symmetric encryption (AES-128-CBC + HMAC) for API key storage.
"""
import os
import base64
from pathlib import Path
from typing import Optional
from cryptography.fernet import Fernet


class EncryptionService:
    """
    Service for encrypting and decrypting sensitive data.

    Uses Fernet (symmetric encryption) with a master key.
    The master key can be provided via:
    1. MASTER_KEY environment variable (URL-safe base64 encoded)
    2. MASTER_KEY_FILE environment variable (path to file containing key)
    3. Auto-generated and stored in .master_key file (development only)
    """

    def __init__(self):
        self._fernet: Optional[Fernet] = None
        self._initialize()

    def _initialize(self):
        """Initialize Fernet with master key from various sources."""
        master_key = self._load_master_key()
        if master_key:
            self._fernet = Fernet(master_key)
        else:
            # Generate and store new key for development
            new_key = Fernet.generate_key()
            self._fernet = Fernet(new_key)
            self._store_master_key(new_key)

    def _load_master_key(self) -> Optional[bytes]:
        """Load master key from environment or file."""
        # 1. Check MASTER_KEY env variable
        env_key = os.getenv("MASTER_KEY")
        if env_key:
            try:
                return base64.urlsafe_b64decode(env_key.encode())
            except Exception:
                pass

        # 2. Check MASTER_KEY_FILE env variable
        key_file = os.getenv("MASTER_KEY_FILE")
        if key_file and Path(key_file).exists():
            try:
                with open(key_file, "rb") as f:
                    return f.read().strip()
            except Exception:
                pass

        # 3. Check .master_key file in project root (development)
        master_key_path = Path(__file__).parent.parent.parent / ".master_key"
        if master_key_path.exists():
            try:
                with open(master_key_path, "rb") as f:
                    return f.read().strip()
            except Exception:
                pass

        return None

    def _store_master_key(self, key: bytes):
        """Store master key to .master_key file (development only)."""
        master_key_path = Path(__file__).parent.parent.parent / ".master_key"
        try:
            with open(master_key_path, "wb") as f:
                f.write(key)
            # Restrict file permissions (owner read/write only)
            os.chmod(master_key_path, 0o600)
        except Exception:
            pass

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext string.

        Args:
            plaintext: The string to encrypt

        Returns:
            URL-safe base64 encoded ciphertext

        Raises:
            ValueError: If encryption service is not initialized
        """
        if not self._fernet:
            raise ValueError("Encryption service not initialized")

        if not plaintext:
            return ""

        plaintext_bytes = plaintext.encode("utf-8")
        ciphertext = self._fernet.encrypt(plaintext_bytes)
        return ciphertext.decode("utf-8")

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext string.

        Args:
            ciphertext: The URL-safe base64 encoded ciphertext

        Returns:
            Decrypted plaintext string

        Raises:
            ValueError: If decryption fails or service not initialized
        """
        if not self._fernet:
            raise ValueError("Encryption service not initialized")

        if not ciphertext:
            return ""

        try:
            ciphertext_bytes = ciphertext.encode("utf-8")
            plaintext = self._fernet.decrypt(ciphertext_bytes)
            return plaintext.decode("utf-8")
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def generate_key(self) -> str:
        """
        Generate a new Fernet key.

        Returns:
            URL-safe base64 encoded key
        """
        key = Fernet.generate_key()
        return key.decode("utf-8")

    def rotate_key(self, old_ciphertext: str, new_master_key: Optional[bytes] = None) -> str:
        """
        Rotate encryption key and re-encrypt data.

        Args:
            old_ciphertext: Data encrypted with old key
            new_master_key: New master key (auto-generated if None)

        Returns:
            Data encrypted with new key
        """
        # Decrypt with current key
        plaintext = self.decrypt(old_ciphertext)

        # Re-initialize with new key if provided
        if new_master_key:
            self._fernet = Fernet(new_master_key)

        # Re-encrypt with new key
        return self.encrypt(plaintext)


# Singleton instance
_encryption_service: Optional[EncryptionService] = None


def get_encryption_service() -> EncryptionService:
    """Get or create the singleton encryption service instance."""
    global _encryption_service
    if _encryption_service is None:
        _encryption_service = EncryptionService()
    return _encryption_service


def encrypt_api_key(api_key: str) -> str:
    """Convenience function to encrypt an API key."""
    return get_encryption_service().encrypt(api_key)


def decrypt_api_key(ciphertext: str) -> str:
    """Convenience function to decrypt an API key."""
    return get_encryption_service().decrypt(ciphertext)
