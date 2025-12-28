"""
API route handlers for terminal endpoints
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from datetime import datetime
from app.models.models import (
    TerminalListResponse, TerminalDetail, MetricsResponse, Interval
)
from app.core.auth import verify_token
from app.core.mock_data import (
    get_mock_terminals, get_mock_terminal_detail, generate_metrics_data
)

router = APIRouter( tags=["terminals"])


@router.get("/terminals", response_model=TerminalListResponse)
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


@router.get("/terminals/{terminal_id}", response_model=TerminalDetail)
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


@router.get("/terminals/{terminal_id}/metrics", response_model=MetricsResponse)
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
