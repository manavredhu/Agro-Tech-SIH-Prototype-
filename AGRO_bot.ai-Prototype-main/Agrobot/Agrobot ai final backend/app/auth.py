# app/auth.py
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
import hashlib
import secrets
import base64
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.db import get_database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

ALGORITHM = "HS256"

def get_password_hash(password: str) -> str:
    """Hash a password using PBKDF2 with SHA-256"""
    # Generate a random salt
    salt = secrets.token_bytes(32)
    # Hash the password
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Combine salt and hash, then encode as base64
    return base64.b64encode(salt + pwdhash).decode('ascii')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash"""
    try:
        # Decode the stored hash
        stored = base64.b64decode(hashed.encode('ascii'))
        # Extract salt (first 32 bytes) and hash (rest)
        salt = stored[:32]
        stored_hash = stored[32:]
        # Hash the provided password with the same salt
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        # Compare hashes
        return pwdhash == stored_hash
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError):
        raise credentials_exception
    
    db = get_database()
    user = await db.users.find_one({"username": username})
    if user is None:
        raise credentials_exception
    
    # Convert MongoDB _id to string and remove sensitive data
    user["id"] = str(user["_id"])
    user.pop("_id", None)
    user.pop("hashed_password", None)
    return user