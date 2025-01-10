import bcrypt
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode
from typing import Optional
import os
import logging

class SecurityManager:
    """Handles all security-related operations including password hashing and data encryption."""
    
    def __init__(self):
        """Initialize security manager with encryption key."""
        self.setup_logging()
        self._encryption_key = self._load_or_create_key()
        self._fernet = Fernet(self._encryption_key)
    
    def setup_logging(self):
        """Configure logging for security operations."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_or_create_key(self) -> bytes:
        """Load existing encryption key or create a new one."""
        key_file = "encryption_key.key"
        try:
            if os.path.exists(key_file):
                with open(key_file, "rb") as f:
                    return f.read()
            else:
                key = Fernet.generate_key()
                with open(key_file, "wb") as f:
                    f.write(key)
                return key
        except Exception as e:
            self.logger.error(f"Error handling encryption key: {str(e)}")
            raise
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return b64encode(hashed).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Password hashing error: {str(e)}")
            raise
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            if not password or not hashed_password:
                return False
            stored_hash = b64decode(hashed_password.encode('utf-8'))
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        except Exception as e:
            self.logger.error(f"Password verification error: {str(e)}")
            return False
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data using Fernet (AES)."""
        try:
            encrypted = self._fernet.encrypt(data.encode('utf-8'))
            return b64encode(encrypted).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Data encryption error: {str(e)}")
            raise
    
    def decrypt_data(self, encrypted_data: str) -> Optional[str]:
        """Decrypt encrypted data."""
        try:
            decrypted = self._fernet.decrypt(b64decode(encrypted_data.encode('utf-8')))
            return decrypted.decode('utf-8')
        except Exception as e:
            self.logger.error(f"Data decryption error: {str(e)}")
            return None