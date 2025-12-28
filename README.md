# Starlink Enterprise Dashboard API - Mock Server

A FastAPI-based mock server implementing the Starlink Enterprise Dashboard API specification with realistic sample data.

## 📁 Project Structure

```
Backend/
├── app/                    # Main application package
│   ├── api/               # API route handlers
│   │   ├── __init__.py
│   │   ├── telemetry.py   # Telemetry endpoints
│   │   ├── terminals.py   # Terminal management endpoints
│   │   ├── monitoring.py  # Alerts and fleet health endpoints
│   │   └── system.py      # Health check and system info
│   ├── core/              # Core utilities and configuration
│   │   ├── __init__.py
│   │   ├── config.py      # Application configuration
│   │   ├── auth.py        # Authentication utilities
│   │   └── mock_data.py   # Mock data generators
│   ├── models/            # Data models and schemas
│   │   ├── __init__.py
│   │   └── models.py      # Pydantic models
│   ├── __init__.py
│   └── main.py            # FastAPI application factory
├── docs/                  # Documentation and API specs
│   ├── openapi.yaml       # OpenAPI specification
│   └── openapi/           # Generated OpenAPI files
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_api.py        # API integration tests
├── scripts/               # Utility scripts
│   └── generate_openapi.py
├── main.py                # Application entrypoint
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── dev.sh               # Development server script
├── start_server.sh      # Production server script
└── README.md            # This file
```

## Features

- ✅ All endpoints from the OpenAPI spec implemented
- 🎭 Realistic mock data for terminals, alerts, metrics, and fleet health
- 🔐 JWT Bearer token authentication (mock - accepts any token)
- 📊 Time-series metrics generation
- 📄 Automatic API documentation with Swagger UI
- 🚀 Ready to run and extend
- 🏗️ Clean, modular architecture with separated concerns

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Development

### Development Server

For development with auto-reload:

```bash
./dev.sh
```

Or manually:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Project Structure

The project follows a modular FastAPI structure:
- `app/api/`: Route handlers organized by domain
- `app/core/`: Shared utilities, configuration, and authentication
- `app/models/`: Pydantic models and schemas
- `tests/`: Test files
- `docs/`: API documentation and specifications

## API Endpoints

### Authentication
All endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your-token>
```
*Note: This mock server accepts any token for demonstration purposes.*

### Telemetry
- `POST /v1/telemetry` - Ingest telemetry data from terminals

### Terminals
- `GET /v1/terminals` - List terminals with health status
- `GET /v1/terminals/{terminal_id}` - Get detailed terminal information
- `GET /v1/terminals/{terminal_id}/metrics` - Get time-series metrics for a terminal

### Alerts
- `GET /v1/alerts` - List and filter alerts

### Fleet Management
- `GET /v1/fleet/health` - Get fleet-wide health summary

## Sample API Calls

### List Terminals
```bash
curl -H "Authorization: Bearer demo-token" \
  "http://localhost:8000/v1/terminals?limit=10&status=online"
```

### Get Terminal Metrics
```bash
curl -H "Authorization: Bearer demo-token" \
  "http://localhost:8000/v1/terminals/TERM-1001/metrics?from=2024-01-01T00:00:00Z&to=2024-01-01T01:00:00Z&interval=5m"
```

### Ingest Telemetry
```bash
curl -X POST \
  -H "Authorization: Bearer demo-token" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: unique-key-123" \
  -d '{
    "terminal_id": "TERM-1001",
    "timestamp": "2024-01-01T12:00:00Z",
    "metrics": {
      "latency_ms": 52.3,
      "packet_loss_pct": 0.2,
      "uptime_pct": 99.98,
      "downlink_mbps": 140.2,
      "uplink_mbps": 18.4
    }
  }' \
  "http://localhost:8000/v1/telemetry"
```

## Project Structure

```
Backend/
├── main.py              # FastAPI application with all endpoints
├── models.py            # Pydantic models matching OpenAPI schemas
├── mock_data.py         # Mock data generators
├── requirements.txt     # Python dependencies
├── openapi.yaml         # Original API specification
└── README.md           # This file
```

## Mock Data

The server generates realistic mock data including:

- **50 terminals** across major US cities
- **Randomized health status** (70% healthy, 20% degraded, 10% offline)
- **Time-series metrics** with realistic values for latency, packet loss, throughput
- **Alert system** with different severities and statuses
- **Fleet health summaries** with aggregate statistics

## Customizing the Server

### Adding New Endpoints

1. Add the endpoint function to `main.py`
2. Create any new models in `models.py`
3. Add mock data generators in `mock_data.py`

Example:
```python
@app.get("/v1/custom-endpoint")
async def custom_endpoint(token: str = Depends(verify_token)):
    return {"message": "Custom endpoint response"}
```

### Modifying Mock Data

Edit `mock_data.py` to customize:
- Terminal locations and counts
- Health status distributions
- Metrics ranges and patterns
- Alert types and frequencies

### Authentication

Currently uses mock authentication. To integrate real JWT validation:

1. Install `python-jose[cryptography]`
2. Replace the `verify_token` function in `main.py`
3. Add proper JWT secret key and validation logic

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload
```

### Testing the API

Use the interactive Swagger UI at http://localhost:8000/docs to test all endpoints.

### Error Handling

The server implements proper HTTP status codes and error responses following the OpenAPI specification:

- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (missing/invalid token)
- `404` - Not Found (terminal not found)
- `500` - Internal Server Error

## Production Considerations

For production deployment, consider:

1. **Real Authentication**: Implement proper JWT validation
2. **Database**: Replace mock data with real database (PostgreSQL, MongoDB)
3. **Rate Limiting**: Add rate limiting middleware
4. **Logging**: Implement structured logging
5. **Monitoring**: Add health checks and metrics
6. **CORS**: Configure CORS for web frontend
7. **Environment Config**: Use environment variables for configuration

## Contributing

1. Follow the existing code structure
2. Add comprehensive docstrings to new functions
3. Update this README when adding new features
4. Test new endpoints using the Swagger UI
