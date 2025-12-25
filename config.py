"""
Configuration settings for the Starlink Enterprise Dashboard API
Customize these settings to modify the mock server behavior
"""

# Server Configuration
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000
DEBUG = True

# Mock Data Configuration
DEFAULT_TERMINAL_COUNT = 50
DEFAULT_ALERT_COUNT = 20

# Health Status Distribution (percentages)
HEALTH_STATUS_WEIGHTS = {
    "healthy": 70,
    "degraded": 20, 
    "offline": 10
}

# Alert Status Distribution (percentages)
ALERT_STATUS_WEIGHTS = {
    "open": 60,
    "acknowledged": 25,
    "resolved": 15
}

# Metrics Configuration
METRICS_CONFIG = {
    "latency_ms": {"min": 45, "max": 85},
    "packet_loss_pct": {"min": 0, "max": 5},
    "uptime_pct": {"min": 95, "max": 100},
    "downlink_mbps": {"min": 100, "max": 200},
    "uplink_mbps": {"min": 15, "max": 25}
}

# Terminal Locations (add more as needed)
TERMINAL_LOCATIONS = [
    {"label": "Los Angeles, CA", "lat": 34.0522, "lon": -118.2437},
    {"label": "New York, NY", "lat": 40.7128, "lon": -74.0060},
    {"label": "Chicago, IL", "lat": 41.8781, "lon": -87.6298},
    {"label": "Houston, TX", "lat": 29.7604, "lon": -95.3698},
    {"label": "Phoenix, AZ", "lat": 33.4484, "lon": -112.0740},
    {"label": "Philadelphia, PA", "lat": 39.9526, "lon": -75.1652},
    {"label": "San Antonio, TX", "lat": 29.4241, "lon": -98.4936},
    {"label": "San Diego, CA", "lat": 32.7157, "lon": -117.1611},
    {"label": "Dallas, TX", "lat": 32.7767, "lon": -96.7970},
    {"label": "San Jose, CA", "lat": 37.3382, "lon": -121.8863},
    {"label": "Austin, TX", "lat": 30.2672, "lon": -97.7431},
    {"label": "Seattle, WA", "lat": 47.6062, "lon": -122.3321},
    {"label": "Denver, CO", "lat": 39.7392, "lon": -104.9903},
    {"label": "Boston, MA", "lat": 42.3601, "lon": -71.0589},
    {"label": "Miami, FL", "lat": 25.7617, "lon": -80.1918}
]

# Alert Types
ALERT_TYPES = [
    "latency_spike",
    "packet_loss_high", 
    "connection_unstable",
    "firmware_outdated",
    "signal_degraded",
    "thermal_warning",
    "power_fluctuation",
    "weather_interference",
    "obstruction_detected",
    "maintenance_required"
]

# Authentication (for future implementation)
JWT_SECRET_KEY = "your-secret-key-here"  # Change in production
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
