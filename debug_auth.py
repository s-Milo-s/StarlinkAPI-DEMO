#!/usr/bin/env python3
"""
Simple test script to debug the auth endpoint
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth_endpoint():
    print("🔧 Testing auth endpoint...")
    
    # Test with correct payload
    print("\n1. Testing with correct payload...")
    try:
        token_request = {
            "api_secret": "demo-secret-key"
        }
        response = requests.post(
            f"{BASE_URL}/v1/auth/token", 
            json=token_request,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Success! Token: {token_data['access_token'][:20]}...")
        else:
            print(f"❌ Failed with {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test with missing field
    print("\n2. Testing with missing api_secret...")
    try:
        response = requests.post(
            f"{BASE_URL}/v1/auth/token", 
            json={},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test with wrong field name
    print("\n3. Testing with wrong field name...")
    try:
        response = requests.post(
            f"{BASE_URL}/v1/auth/token", 
            json={"secret": "demo-secret-key"},
            headers={"Content-Type": "application/json"}
        )
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_auth_endpoint()
