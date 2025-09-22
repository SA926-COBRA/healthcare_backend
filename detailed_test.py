#!/usr/bin/env python3
"""
Detailed test of the authentication endpoints
"""

import os
import sys
import json
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables
os.environ["DATABASE_URL"] = "postgresql://prontibus_user:j1TNfXAeaD1fyNY5RPV68psq0JmwodLV@dpg-d38mtsogjchc73d6ovdg-a.oregon-postgres.render.com/prontibus"
os.environ["USE_SQLITE"] = "false"
os.environ["USE_DATABASE"] = "true"

def detailed_test():
    """Detailed test of authentication endpoints"""
    try:
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        # Test staff login with detailed logging
        print("🔍 Testing staff login endpoint...")
        print("Request payload:", {"email_or_cpf": "admin@prontivus.com", "password": "admin123"})
        
        response = client.post("/api/v1/auth/login", json={
            "email_or_cpf": "admin@prontivus.com",
            "password": "admin123"
        })
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Staff login successful!")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Role: {data.get('user_role')}")
        else:
            print(f"❌ Staff login failed!")
        
        print("\n" + "="*50 + "\n")
        
        # Test patient login with detailed logging
        print("🔍 Testing patient login endpoint...")
        print("Request payload:", {"email_or_cpf": "patient@prontivus.com", "password": "patient123"})
        
        response = client.post("/api/v1/patient-auth/login", json={
            "email_or_cpf": "patient@prontivus.com",
            "password": "patient123"
        })
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Patient login successful!")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Role: {data.get('user_role')}")
        else:
            print(f"❌ Patient login failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    detailed_test()
