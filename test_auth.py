#!/usr/bin/env python3
"""
Test authentication locally to debug issues
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables
os.environ["DATABASE_URL"] = "postgresql://prontibus_user:j1TNfXAeaD1fyNY5RPV68psq0JmwodLV@dpg-d38mtsogjchc73d6ovdg-a.oregon-postgres.render.com/prontibus"
os.environ["USE_SQLITE"] = "false"
os.environ["USE_DATABASE"] = "true"

def test_auth():
    """Test authentication locally"""
    try:
        from app.database.database import get_db
        from app.services.auth_service import AuthService
        from app.schemas.auth import UserLogin
        from fastapi import Request
        
        # Get database session
        db = next(get_db())
        
        # Create auth service
        auth_service = AuthService(db)
        
        # Test data
        login_data = UserLogin(
            email_or_cpf="admin@prontivus.com",
            password="admin123"
        )
        
        # Create a mock request
        class MockRequest:
            def __init__(self):
                self.headers = {}
                self.client = type('Client', (), {'host': 'localhost'})()
        
        request = MockRequest()
        
        print("🔍 Testing authentication...")
        print(f"📧 Email: {login_data.email_or_cpf}")
        print(f"🔑 Password: {login_data.password}")
        
        # Test authentication
        token = auth_service.authenticate_user(
            login_data.email_or_cpf, 
            login_data.password, 
            request
        )
        
        print(f"✅ Authentication successful!")
        print(f"🎫 Token: {token.access_token[:50]}...")
        print(f"👤 User ID: {token.user_id}")
        print(f"🏷️ Role: {token.user_role}")
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    test_auth()
