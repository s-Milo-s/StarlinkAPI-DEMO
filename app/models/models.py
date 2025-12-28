from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum


class HealthStatus(str, Enum):
    healthy = "healthy"
    degraded = "degraded"
    offline = "offline"


class TerminalStatus(str, Enum):
    online = "online"
    offline = "offline"
    degraded = "degraded"


class AlertSeverity(str, Enum):
    info = "info"
    warn = "warn"
    critical = "critical"


class AlertStatus(str, Enum):
    open = "open"
    acknowledged = "acknowledged"
    resolved = "resolved"


class Interval(str, Enum):
    one_minute = "1m"
    five_minutes = "5m"
    one_hour = "1h"


class ErrorResponse(BaseModel):
    error: str
    message: str
    request_id: str


# Authentication Models
class TokenRequest(BaseModel):
    """Token request payload."""
    api_secret: str


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    expires_at: Optional[datetime] = None


class Location(BaseModel):
    label: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


class TelemetryIngestRequest(BaseModel):
    terminal_id: str
    timestamp: datetime
    metrics: Dict[str, Any]


class TelemetryIngestResponse(BaseModel):
    request_id: str
    accepted: bool


class TerminalSummary(BaseModel):
    terminal_id: str
    name: Optional[str] = None
    health_status: HealthStatus
    last_seen: datetime
    status: TerminalStatus
    location: Optional[Location] = None


class HealthFactor(BaseModel):
    factor: str
    value: float
    threshold: float
    message: str


class TerminalDetail(TerminalSummary):
    firmware_version: Optional[str] = None
    account_id: Optional[str] = None
    health_factors: Optional[List[HealthFactor]] = None


class TerminalListResponse(BaseModel):
    items: List[TerminalSummary]
    next_cursor: Optional[str] = None


class MetricPoint(BaseModel):
    t: datetime
    v: float


class MetricsResponse(BaseModel):
    terminal_id: str
    from_time: datetime
    to_time: datetime
    interval: Interval
    series: Dict[str, List[MetricPoint]]

    class Config:
        fields = {"from_time": "from", "to_time": "to"}


class Alert(BaseModel):
    alert_id: str
    terminal_id: str
    severity: AlertSeverity
    type: str
    message: str
    created_at: datetime
    status: AlertStatus


class AlertsListResponse(BaseModel):
    items: List[Alert]
    next_cursor: Optional[str] = None


class FleetCounts(BaseModel):
    healthy: int
    degraded: int
    offline: int


class TopIssue(BaseModel):
    type: str
    count: int
    message: str


class FleetHealthResponse(BaseModel):
    from_time: datetime
    to_time: datetime
    counts: FleetCounts
    top_issues: Optional[List[TopIssue]] = None

    class Config:
        fields = {"from_time": "from", "to_time": "to"}
