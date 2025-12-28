"""
FastAPI application factory
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import telemetry, terminals, monitoring, system, auth

def create_app() -> FastAPI:
    app = FastAPI(
        title="Starlink Terminal Management API",
        description="API for managing Starlink terminals and monitoring telemetry data",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this properly for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth.router, prefix="/v1", tags=["authentication"])
    app.include_router(telemetry.router, prefix="/v1", tags=["telemetry"])
    app.include_router(terminals.router, prefix="/v1", tags=["terminals"])
    app.include_router(monitoring.router, prefix="/v1", tags=["monitoring"])
    app.include_router(system.router, prefix="/v1", tags=["system"])
    
    @app.get("/")
    async def root():
        return {"message": "Starlink Terminal Management API", "version": "1.0.0"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "timestamp": "2024-12-27T10:00:00Z"}
    
    return app

# Create the app instance that ASGI will look for
app = create_app()