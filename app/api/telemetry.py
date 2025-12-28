"""
API route handlers for telemetry endpoints
"""
from fastapi import APIRouter, HTTPException, Header, Depends
from app.models.models import TelemetryIngestRequest, TelemetryIngestResponse
from app.core.auth import verify_token
from app.core.mock_data import get_mock_terminals, generate_request_id

router = APIRouter( tags=["telemetry"])


@router.post("/telemetry", response_model=TelemetryIngestResponse, status_code=202)
async def ingest_telemetry(
    data: TelemetryIngestRequest,
    idempotency_key: int = Header(..., alias="Idempotency-Key"),  # this is a str
    token: str = Depends(verify_token)
):
    """
    Ingest telemetry datapoints (idempotent)
    
    This endpoint accepts telemetry data from terminals and returns an acceptance response.
    In a real implementation, this would:
    - Validate the terminal_id exists
    - Store the telemetry data in a time-series database
    - Handle idempotency using the provided key
    """
    request_id = generate_request_id()
    
    # Mock validation - check if terminal exists
    terminals = get_mock_terminals()
    terminal_exists = any(t.terminal_id == data.terminal_id for t in terminals)
    
    if not terminal_exists:
        raise HTTPException(status_code=400, detail=f"Terminal {data.terminal_id} not found")
    
    return TelemetryIngestResponse(
        request_id=request_id,
        accepted=True
    )
