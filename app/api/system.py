"""
API route handlers for health and informational endpoints
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter(tags=["system"])


@router.get("/")
async def root():
    """API Root - provides basic information about the service"""
    return {
        "name": "Starlink Enterprise Dashboard API",
        "version": "0.1.0",
        "description": "Mock API server with realistic Starlink terminal data",
        "endpoints": {
            "telemetry": "/v1/telemetry",
            "terminals": "/v1/terminals",
            "alerts": "/v1/alerts",
            "fleet_health": "/v1/fleet/health",
            "docs": "/docs"
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
