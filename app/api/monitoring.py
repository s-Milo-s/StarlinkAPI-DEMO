"""
API route handlers for alerts and fleet health endpoints
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from datetime import datetime, timezone
from app.models.models import (
    AlertsListResponse, FleetHealthResponse, AlertStatus, AlertSeverity
)
from app.core.auth import verify_token
from app.core.mock_data import get_mock_alerts, get_mock_fleet_health

router = APIRouter( tags=["monitoring"])


@router.get("/alerts", response_model=AlertsListResponse)
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


@router.get("/fleet/health", response_model=FleetHealthResponse)
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
