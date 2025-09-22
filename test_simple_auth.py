#!/usr/bin/env python3
"""
Simple authentication test bypassing AuthService
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

def test_simple_auth():
    """Test simple database query without AuthService"""
    try:
        from app.database.database import get_engine
        from sqlalchemy import text
        
        # Get database engine
        engine = get_engine()
        
        with engine.connect() as conn:
            # Test simple query
            result = conn.execute(text("""
                SELECT id, email, username, hashed_password, is_active 
                FROM users 
                WHERE email = :email
            """), {"email": "admin@prontivus.com"})
            
            user = result.fetchone()
            
            if user:
                print(f"✅ User found: {user[1]} (ID: {user[0]})")
                print(f"   Username: {user[2]}")
                print(f"   Password Hash: {user[3][:20]}...")
                print(f"   Active: {user[4]}")
                
                # Test password verification
                from passlib.context import CryptContext
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                
                if pwd_context.verify("admin123", user[3]):
                    print("✅ Password verification successful!")
                else:
                    print("❌ Password verification failed!")
            else:
                print("❌ User not found!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_auth()
