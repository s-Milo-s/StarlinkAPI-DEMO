from datetime import datetime, timedelta, timezone
from typing import List
import random
import uuid
from models import (
    TerminalSummary, TerminalDetail, HealthStatus, TerminalStatus, 
    Location, Alert, AlertSeverity, AlertStatus, MetricPoint,
    HealthFactor, FleetCounts, TopIssue
)
from config import (
    DEFAULT_TERMINAL_COUNT, HEALTH_STATUS_WEIGHTS, ALERT_STATUS_WEIGHTS,
    METRICS_CONFIG, TERMINAL_LOCATIONS, ALERT_TYPES
)


def generate_terminal_id() -> str:
    """Generate a mock terminal ID"""
    return f"TERM-{random.randint(1000, 9999)}"


def generate_request_id() -> str:
    """Generate a mock request ID"""
    return f"req_{uuid.uuid4().hex[:8]}"


def get_mock_terminals(count: int = DEFAULT_TERMINAL_COUNT) -> List[TerminalSummary]:
    """Generate mock terminal data"""
    terminals = []
    
    for i in range(count):
        terminal_id = f"TERM-{1000 + i}"
        health_status = random.choices(
            [HealthStatus.healthy, HealthStatus.degraded, HealthStatus.offline],
            weights=[HEALTH_STATUS_WEIGHTS["healthy"], HEALTH_STATUS_WEIGHTS["degraded"], HEALTH_STATUS_WEIGHTS["offline"]]
        )[0]
        
        # Map health status to terminal status
        if health_status == HealthStatus.healthy:
            status = TerminalStatus.online
        elif health_status == HealthStatus.degraded:
            status = TerminalStatus.degraded
        else:
            status = TerminalStatus.offline
            
        location_data = random.choice(TERMINAL_LOCATIONS)
        
        terminal = TerminalSummary(
            terminal_id=terminal_id,
            name=f"Terminal {i+1}",
            health_status=health_status,
            last_seen=datetime.now(timezone.utc) - timedelta(minutes=random.randint(1, 60)),
            status=status,
            location=Location(**location_data)
        )
        terminals.append(terminal)
    
    return terminals


def get_mock_terminal_detail(terminal_id: str) -> TerminalDetail:
    """Generate detailed mock terminal data"""
    # Find the terminal from our mock data
    terminals = get_mock_terminals()
    base_terminal = next((t for t in terminals if t.terminal_id == terminal_id), None)
    
    if not base_terminal:
        # Create a new one if not found
        base_terminal = TerminalSummary(
            terminal_id=terminal_id,
            name=f"Terminal {terminal_id.split('-')[1]}",
            health_status=HealthStatus.healthy,
            last_seen=datetime.now(timezone.utc) - timedelta(minutes=random.randint(1, 60)),
            status=TerminalStatus.online,
            location=Location(label="Unknown Location", lat=0.0, lon=0.0)
        )
    
    # Add detailed information
    health_factors = []
    if base_terminal.health_status == HealthStatus.degraded:
        health_factors = [
            HealthFactor(
                factor="packet_loss_pct",
                value=2.5,
                threshold=2.0,
                message="Packet loss above threshold"
            ),
            HealthFactor(
                factor="latency_ms",
                value=85.2,
                threshold=80.0,
                message="Latency higher than expected"
            )
        ]
    
    return TerminalDetail(
        **base_terminal.dict(),
        firmware_version=f"v{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        account_id=f"acc_{uuid.uuid4().hex[:8]}",
        health_factors=health_factors
    )


def generate_metrics_data(terminal_id: str, from_time: datetime, to_time: datetime, interval: str) -> dict:
    """Generate mock metrics time series data"""
    # Calculate number of points based on interval
    if interval == "1m":
        delta = timedelta(minutes=1)
    elif interval == "5m":
        delta = timedelta(minutes=5)
    else:  # 1h
        delta = timedelta(hours=1)
    
    points = []
    current_time = from_time
    while current_time < to_time:
        points.append(current_time)
        current_time += delta
    
    # Generate mock data for different metrics using config
    metrics = {}
    for metric_name, config in METRICS_CONFIG.items():
        metrics[metric_name] = [
            MetricPoint(t=t, v=random.uniform(config["min"], config["max"])) for t in points
        ]
    
    return metrics


def get_mock_alerts(count: int = 20) -> List[Alert]:
    """Generate mock alert data"""
    alerts = []
    terminals = get_mock_terminals()
    
    for i in range(count):
        alert_type = random.choice(ALERT_TYPES)
        alert = Alert(
            alert_id=f"alert_{uuid.uuid4().hex[:8]}",
            terminal_id=random.choice(terminals).terminal_id,
            severity=random.choice(list(AlertSeverity)),
            type=alert_type,
            message=f"Alert {i+1}: {alert_type.replace('_', ' ').title()}",
            created_at=datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 48)),
            status=random.choices(
                list(AlertStatus),
                weights=[ALERT_STATUS_WEIGHTS["open"], ALERT_STATUS_WEIGHTS["acknowledged"], ALERT_STATUS_WEIGHTS["resolved"]]
            )[0]
        )
        alerts.append(alert)
    
    return alerts


def get_mock_fleet_health(from_time: datetime, to_time: datetime) -> dict:
    """Generate mock fleet health data"""
    terminals = get_mock_terminals()
    
    # Count terminals by health status
    healthy_count = sum(1 for t in terminals if t.health_status == HealthStatus.healthy)
    degraded_count = sum(1 for t in terminals if t.health_status == HealthStatus.degraded)
    offline_count = sum(1 for t in terminals if t.health_status == HealthStatus.offline)
    
    top_issues = [
        TopIssue(
            type="packet_loss_spike",
            count=5,
            message="Elevated packet loss detected"
        ),
        TopIssue(
            type="latency_high",
            count=3,
            message="High latency affecting performance"
        ),
        TopIssue(
            type="signal_degraded",
            count=2,
            message="Signal quality degradation"
        )
    ]
    
    return {
        "counts": FleetCounts(
            healthy=healthy_count,
            degraded=degraded_count,
            offline=offline_count
        ),
        "top_issues": top_issues
    }
