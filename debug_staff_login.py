#!/usr/bin/env python3
"""
Debug staff login issue
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

def debug_staff_login():
    """Debug staff login step by step"""
    try:
        from app.database.database import get_engine
        from sqlalchemy import text
        from passlib.context import CryptContext
        
        # Password hashing
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
        
        # Get database engine
        engine = get_engine()
        
        with engine.connect() as conn:
            print("🔍 Step 1: Checking if admin user exists...")
            result = conn.execute(text("""
                SELECT id, email, username, hashed_password, is_active, tenant_id, is_superuser
                FROM users
                WHERE email = :email
            """), {"email": "admin@prontivus.com"})
            
            user_row = result.fetchone()
            
            if user_row:
                user_id, email, username, hashed_password, is_active, tenant_id, is_superuser = user_row
                print(f"✅ User found: {email} (ID: {user_id})")
                print(f"   Username: {username}")
                print(f"   Password Hash: {hashed_password[:20]}...")
                print(f"   Active: {is_active}")
                print(f"   Superuser: {is_superuser}")
                print(f"   Tenant ID: {tenant_id}")
                
                print("\n🔍 Step 2: Testing password verification...")
                if pwd_context.verify("admin123", hashed_password):
                    print("✅ Password verification successful!")
                else:
                    print("❌ Password verification failed!")
                    
                print("\n🔍 Step 3: Testing with email_or_cpf field...")
                result2 = conn.execute(text("""
                    SELECT id, email, username, hashed_password, is_active, tenant_id, is_superuser
                    FROM users
                    WHERE email = :email_or_cpf OR cpf = :email_or_cpf
                """), {"email_or_cpf": "admin@prontivus.com"})
                
                user_row2 = result2.fetchone()
                if user_row2:
                    print("✅ User found with email_or_cpf query")
                else:
                    print("❌ User not found with email_or_cpf query")
                    
            else:
                print("❌ User not found!")
                
                # Let's see what users exist
                print("\n🔍 All users in database:")
                all_users = conn.execute(text("SELECT id, email, username FROM users LIMIT 10"))
                for user in all_users:
                    print(f"   ID: {user[0]}, Email: {user[1]}, Username: {user[2]}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_staff_login()
