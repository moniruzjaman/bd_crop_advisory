
"""
Security Module
JWT Authentication, Rate Limiting, Input Validation
"""

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
from typing import Optional

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Rate limiting storage (use Redis in production)
rate_limit_store = {}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def rate_limiter(identifier: str, max_requests: int = 10, window_seconds: int = 60):
    """
    Simple rate limiter
    In production, use Redis with proper expiration
    """
    now = datetime.utcnow()

    if identifier not in rate_limit_store:
        rate_limit_store[identifier] = []

    # Clean old entries
    rate_limit_store[identifier] = [
        ts for ts in rate_limit_store[identifier]
        if (now - ts).total_seconds() < window_seconds
    ]

    if len(rate_limit_store[identifier]) >= max_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later."
        )

    rate_limit_store[identifier].append(now)

def validate_image_size(image_size: int, max_size_mb: int = 10):
    """Validate image size"""
    max_size_bytes = max_size_mb * 1024 * 1024
    if image_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image size exceeds {max_size_mb}MB limit"
        )

def sanitize_input(text: str) -> str:
    """Basic input sanitization"""
    # Remove potentially dangerous characters
    dangerous = ['<', '>', '"', "'", ';', '--', '/*', '*/']
    for char in dangerous:
        text = text.replace(char, '')
    return text.strip()
