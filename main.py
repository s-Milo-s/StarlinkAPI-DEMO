from fastapi import FastAPI, HTTPException, Header, Query, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from typing import Optional, List
from datetime import datetime, timezone
import uuid

from models import (
    TelemetryIngestRequest, TelemetryIngestResponse, TerminalListResponse,
    TerminalDetail, MetricsResponse, AlertsListResponse, FleetHealthResponse,
    ErrorResponse, HealthStatus, AlertSeverity, AlertStatus, Interval
)
from mock_data import (
    get_mock_terminals, get_mock_terminal_detail, generate_metrics_data,
    get_mock_alerts, get_mock_fleet_health, generate_request_id
)
from config import SERVER_HOST, SERVER_PORT

app = FastAPI(
    title="Starlink Enterprise Dashboard API (Demo)",
    version="0.1.0",
    description="Mock API server for Starlink Enterprise Dashboard with realistic data"
)

security = HTTPBearer(auto_error=False)


async def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Mock JWT verification - accepts any bearer token for demo purposes"""
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=401, detail="Missing or invalid bearer token")
    return credentials.credentials


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom exception handler that returns our ErrorResponse format"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail.lower().replace(" ", "_"),
            "message": exc.detail,
            "request_id": generate_request_id()
        }
    )


@app.post("/v1/telemetry", response_model=TelemetryIngestResponse, status_code=202)
async def ingest_telemetry(
    data: TelemetryIngestRequest,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
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


@app.get("/v1/terminals", response_model=TerminalListResponse)
async def list_terminals(
    status: Optional[str] = Query(None, regex="^(online|offline|degraded)$"),
    limit: int = Query(100, ge=1, le=500),
    cursor: Optional[str] = None,
    token: str = Depends(verify_token)
):
    """
    List terminals for an account (inventory + health)
    
    Returns a paginated list of terminals with their current health status.
    Use the cursor parameter for pagination through large datasets.
    """
    terminals = get_mock_terminals()
    
    # Filter by status if provided
    if status:
        terminals = [t for t in terminals if t.status.value == status]
    
    # Simple pagination simulation
    start_idx = 0
    if cursor:
        try:
            start_idx = int(cursor)
        except ValueError:
            start_idx = 0
    
    end_idx = start_idx + limit
    page_terminals = terminals[start_idx:end_idx]
    
    # Set next cursor if there are more results
    next_cursor = None
    if end_idx < len(terminals):
        next_cursor = str(end_idx)
    
    return TerminalListResponse(
        items=page_terminals,
        next_cursor=next_cursor
    )


@app.get("/v1/terminals/{terminal_id}", response_model=TerminalDetail)
async def get_terminal_detail(
    terminal_id: str,
    token: str = Depends(verify_token)
):
    """
    Get terminal detail (health + last seen + metadata)
    
    Returns detailed information about a specific terminal including:
    - Current health status and contributing factors
    - Last seen timestamp
    - Firmware version and account information
    """
    terminals = get_mock_terminals()
    terminal_exists = any(t.terminal_id == terminal_id for t in terminals)
    
    if not terminal_exists:
        raise HTTPException(status_code=404, detail="Terminal not found")
    
    return get_mock_terminal_detail(terminal_id)


@app.get("/v1/terminals/{terminal_id}/metrics", response_model=MetricsResponse)
async def get_terminal_metrics(
    terminal_id: str,
    from_time: datetime = Query(..., alias="from", description="RFC3339 timestamp (inclusive)"),
    to_time: datetime = Query(..., alias="to", description="RFC3339 timestamp (exclusive)"),
    interval: Interval = Query(Interval.five_minutes, description="Aggregation level"),
    metrics: Optional[str] = Query(None, description="Comma-separated metric keys"),
    token: str = Depends(verify_token)
):
    """
    Get time-series metrics for a terminal
    
    Returns time-series data for specified metrics within the given time range.
    Available metrics: latency_ms, packet_loss_pct, uptime_pct, downlink_mbps, uplink_mbps
    """
    terminals = get_mock_terminals()
    terminal_exists = any(t.terminal_id == terminal_id for t in terminals)
    
    if not terminal_exists:
        raise HTTPException(status_code=404, detail="Terminal not found")
    
    # Validate time range
    if from_time >= to_time:
        raise HTTPException(status_code=400, detail="Invalid time range: 'from' must be before 'to'")
    
    # Generate metrics data
    all_metrics = generate_metrics_data(terminal_id, from_time, to_time, interval.value)
    
    # Filter metrics if specified
    if metrics:
        requested_metrics = [m.strip() for m in metrics.split(",")]
        filtered_metrics = {k: v for k, v in all_metrics.items() if k in requested_metrics}
        if not filtered_metrics:
            raise HTTPException(status_code=400, detail="No valid metrics specified")
        all_metrics = filtered_metrics
    
    return MetricsResponse(
        terminal_id=terminal_id,
        from_time=from_time,
        to_time=to_time,
        interval=interval,
        series=all_metrics
    )


@app.get("/v1/alerts", response_model=AlertsListResponse)
async def list_alerts(
    status: AlertStatus = Query(AlertStatus.open, description="Filter by alert status"),
    severity: Optional[AlertSeverity] = Query(None, description="Filter by severity"),
    terminal_id: Optional[str] = Query(None, description="Filter by terminal"),
    from_time: Optional[datetime] = Query(None, alias="from", description="Filter by creation time"),
    to_time: Optional[datetime] = Query(None, alias="to", description="Filter by creation time"),
    limit: int = Query(100, ge=1, le=500),
    cursor: Optional[str] = None,
    token: str = Depends(verify_token)
):
    """
    List alerts (dashboard alerts page)
    
    Returns a filtered and paginated list of alerts for the dashboard.
    Supports filtering by status, severity, terminal, and time range.
    """
    alerts = get_mock_alerts(50)  # Generate more alerts for filtering
    
    # Convert query datetime parameters to UTC if they exist
    if from_time:
        if from_time.tzinfo is None:
            from_time = from_time.replace(tzinfo=timezone.utc)
        else:
            from_time = from_time.astimezone(timezone.utc)
    
    if to_time:
        if to_time.tzinfo is None:
            to_time = to_time.replace(tzinfo=timezone.utc)
        else:
            to_time = to_time.astimezone(timezone.utc)

    # Apply filters
    if status:
        alerts = [a for a in alerts if a.status == status]
    
    if severity:
        alerts = [a for a in alerts if a.severity == severity]
    
    if terminal_id:
        alerts = [a for a in alerts if a.terminal_id == terminal_id]
    
    if from_time:
        alerts = [a for a in alerts if a.created_at >= from_time]
    
    if to_time:
        alerts = [a for a in alerts if a.created_at < to_time]
    
    # Sort by creation time (newest first)
    alerts.sort(key=lambda x: x.created_at, reverse=True)
    
    # Pagination
    start_idx = 0
    if cursor:
        try:
            start_idx = int(cursor)
        except ValueError:
            start_idx = 0
    
    end_idx = start_idx + limit
    page_alerts = alerts[start_idx:end_idx]
    
    next_cursor = None
    if end_idx < len(alerts):
        next_cursor = str(end_idx)
    
    return AlertsListResponse(
        items=page_alerts,
        next_cursor=next_cursor
    )


@app.get("/v1/fleet/health", response_model=FleetHealthResponse)
async def get_fleet_health(
    from_time: datetime = Query(..., alias="from", description="Start time for health summary"),
    to_time: datetime = Query(..., alias="to", description="End time for health summary"),
    token: str = Depends(verify_token)
):
    """
    Fleet health summary (top-level dashboard tiles)
    
    Returns aggregate health statistics for the entire fleet including:
    - Counts of terminals by health status
    - Top issues affecting the fleet
    """
    if from_time >= to_time:
        raise HTTPException(status_code=400, detail="Invalid time range: 'from' must be before 'to'")
    
    fleet_data = get_mock_fleet_health(from_time, to_time)
    
    return FleetHealthResponse(
        from_time=from_time,
        to_time=to_time,
        counts=fleet_data["counts"],
        top_issues=fleet_data["top_issues"]
    )


@app.get("/")
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


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
