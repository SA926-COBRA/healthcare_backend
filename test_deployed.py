#!/usr/bin/env python3
"""
Test the deployed endpoints on Render.com
"""

import requests
import json

def test_deployed_endpoints():
    """Test the deployed authentication endpoints"""
    base_url = "https://prontibus.onrender.com"
    
    # Test staff login
    print("🔍 Testing deployed staff login endpoint...")
    staff_payload = {
        "email_or_cpf": "admin@prontivus.com",
        "password": "admin123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/auth/login",
            json=staff_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Staff login successful!")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Role: {data.get('user_role')}")
        else:
            print(f"❌ Staff login failed!")
            
    except Exception as e:
        print(f"❌ Staff login error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test patient login
    print("🔍 Testing deployed patient login endpoint...")
    patient_payload = {
        "email_or_cpf": "patient@prontivus.com",
        "password": "patient123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/v1/patient-auth/login",
            json=patient_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Patient login successful!")
            print(f"   User ID: {data.get('user_id')}")
            print(f"   Role: {data.get('user_role')}")
        else:
            print(f"❌ Patient login failed!")
            
    except Exception as e:
        print(f"❌ Patient login error: {e}")

if __name__ == "__main__":
    test_deployed_endpoints()
