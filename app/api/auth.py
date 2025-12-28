"""
Authentication endpoints for the API
"""
import secrets
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException, status
from app.models.models import TokenRequest, TokenResponse

router = APIRouter()


@router.post("/auth/token", response_model=TokenResponse)
async def refresh_token(request: TokenRequest):
    """
    Refresh authentication token.
    
    This is a mock endpoint that accepts any API secret and returns a mock token.
    In a real implementation, this would validate the API secret against a database.
    """
    # Mock validation - in production, validate the api_secret properly
    if not request.api_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API secret"
        )
    
    # Generate mock token (in production, use proper JWT generation)
    mock_token = f"mock_token_{secrets.token_urlsafe(32)}"
    
    # Set expiration time (1 hour from now)
    expires_in = 3600  # 1 hour in seconds
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
    
    return TokenResponse(
        access_token=mock_token,
        token_type="bearer",
        expires_in=expires_in,
        expires_at=expires_at
    )
