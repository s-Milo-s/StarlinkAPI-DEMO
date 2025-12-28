"""
Authentication utilities for the API
"""
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional


security = HTTPBearer(auto_error=False)


async def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Mock JWT verification - accepts any bearer token for demo purposes"""
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing or invalid bearer token")
    return credentials.credentials
