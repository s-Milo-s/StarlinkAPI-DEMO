#!/usr/bin/env python3
"""
Test script for the Starlink Enterprise Dashboard API
Demonstrates all endpoints with sample requests
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"
HEADERS = {
    "Authorization": "Bearer demo-token",
    "Content-Type": "application/json"
}

def test_api():
    print("🚀 Testing Starlink Enterprise Dashboard API")
    print("=" * 50)
    
    # Test authentication token endpoint
    print("\n1. Testing authentication token...")
    try:
        token_request = {
            "api_secret": "demo-secret-key"
        }
        response = requests.post(f"{BASE_URL}/v1/auth/token", json=token_request)
        print(f"✅ Token request: {response.status_code}")
        token_data = response.json()
        print(f"   Token type: {token_data['token_type']}")
        print(f"   Expires in: {token_data['expires_in']} seconds")
        if 'expires_at' in token_data and token_data['expires_at']:
            print(f"   Expires at: {token_data['expires_at']}")
        
        # Update headers with new token for subsequent requests
        global HEADERS
        HEADERS["Authorization"] = f"Bearer {token_data['access_token']}"
    except Exception as e:
        print(f"❌ Token request failed: {e}")
    
    # Test health check
    print("\n2. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test terminals list
    print("\n3. Testing terminals list...")
    try:
        response = requests.get(f"{BASE_URL}/v1/terminals?limit=5", headers=HEADERS)
        print(f"✅ Terminals list: {response.status_code}")
        terminals = response.json()
        print(f"   Found {len(terminals['items'])} terminals")
        if terminals['items']:
            terminal_id = terminals['items'][0]['terminal_id']
            print(f"   Sample terminal: {terminal_id}")
        else:
            print("   No terminals found")
            return
    except Exception as e:
        print(f"❌ Terminals list failed: {e}")
        return
    
    # Test terminal detail
    print("\n4. Testing terminal detail...")
    try:
        response = requests.get(f"{BASE_URL}/v1/terminals/{terminal_id}", headers=HEADERS)
        print(f"✅ Terminal detail: {response.status_code}")
        terminal = response.json()
        print(f"   Terminal: {terminal['name']} ({terminal['health_status']})")
    except Exception as e:
        print(f"❌ Terminal detail failed: {e}")
    
    # Test metrics
    print("\n5. Testing terminal metrics...")
    try:
        now = datetime.utcnow()
        from_time = (now - timedelta(hours=1)).isoformat() + "Z"
        to_time = now.isoformat() + "Z"
        
        response = requests.get(
            f"{BASE_URL}/v1/terminals/{terminal_id}/metrics",
            headers=HEADERS,
            params={
                "from": from_time,
                "to": to_time,
                "interval": "5m",
                "metrics": "latency_ms,packet_loss_pct"
            }
        )
        print(f"✅ Terminal metrics: {response.status_code}")
        metrics = response.json()
        print(f"   Metrics available: {list(metrics['series'].keys())}")
    except Exception as e:
        print(f"❌ Terminal metrics failed: {e}")
    
    # Test alerts
    print("\n6. Testing alerts...")
    try:
        response = requests.get(f"{BASE_URL}/v1/alerts?limit=5", headers=HEADERS)
        print(f"✅ Alerts: {response.status_code}")
        alerts = response.json()
        print(f"   Found {len(alerts['items'])} alerts")
    except Exception as e:
        print(f"❌ Alerts failed: {e}")
    
    # Test fleet health
    print("\n7. Testing fleet health...")
    try:
        now = datetime.utcnow()
        from_time = (now - timedelta(hours=1)).isoformat() + "Z"
        to_time = now.isoformat() + "Z"
        
        response = requests.get(
            f"{BASE_URL}/v1/fleet/health",
            headers=HEADERS,
            params={"from": from_time, "to": to_time}
        )
        print(f"✅ Fleet health: {response.status_code}")
        fleet = response.json()
        counts = fleet['counts']
        print(f"   Fleet status: {counts['healthy']} healthy, {counts['degraded']} degraded, {counts['offline']} offline")
    except Exception as e:
        print(f"❌ Fleet health failed: {e}")
    
    # Test telemetry ingestion
    print("\n8. Testing telemetry ingestion...")
    try:
        telemetry_data = {
            "terminal_id": terminal_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "metrics": {
                "latency_ms": 52.3,
                "packet_loss_pct": 0.2,
                "uptime_pct": 99.98,
                "downlink_mbps": 140.2,
                "uplink_mbps": 18.4
            }
        }
        
        headers_with_idempotency = HEADERS.copy()
        headers_with_idempotency["Idempotency-Key"] = "test-key-123"
        
        response = requests.post(
            f"{BASE_URL}/v1/telemetry",
            headers=headers_with_idempotency,
            json=telemetry_data
        )
        print(f"✅ Telemetry ingestion: {response.status_code}")
        result = response.json()
        print(f"   Accepted: {result['accepted']}, Request ID: {result['request_id']}")
    except Exception as e:
        print(f"❌ Telemetry ingestion failed: {e}")
    
    print("\n🎉 API testing completed!")
    print(f"📚 Visit {BASE_URL}/docs for interactive API documentation")

if __name__ == "__main__":
    test_api()
