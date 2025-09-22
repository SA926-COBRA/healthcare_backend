#!/usr/bin/env python3
"""
Debug staff login endpoint step by step
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

def debug_staff_endpoint():
    """Debug staff login endpoint step by step"""
    try:
        from app.database.database import get_db
        from sqlalchemy import text
        from passlib.context import CryptContext
        from jose import jwt
        from datetime import datetime, timedelta
        from app.core.config import settings
        
        # Password hashing
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
        
        # Get database session
        db = next(get_db())
        
        email_or_cpf = "admin@prontivus.com"
        password = "admin123"
        
        print(f"🔍 Step 1: Looking for user with email_or_cpf: {email_or_cpf}")
        
        # Find user by email or CPF using direct SQL
        cursor = db.execute(text("""
            SELECT id, email, username, hashed_password, is_active, tenant_id, is_superuser
            FROM users
            WHERE email = :email_or_cpf OR cpf = :email_or_cpf
        """), {"email_or_cpf": email_or_cpf})

        user_row = cursor.fetchone()
        if not user_row:
            print("❌ User not found!")
            return

        user_id, email, username, hashed_password, is_active, tenant_id, is_superuser = user_row
        print(f"✅ User found: {email} (ID: {user_id})")
        print(f"   Username: {username}")
        print(f"   Password Hash: {hashed_password[:20]}...")
        print(f"   Active: {is_active}")
        print(f"   Superuser: {is_superuser}")
        print(f"   Tenant ID: {tenant_id}")

        print(f"\n🔍 Step 2: Checking if user is active...")
        if not is_active:
            print("❌ User is not active!")
            return
        print("✅ User is active")

        print(f"\n🔍 Step 3: Verifying password...")
        if not pwd_context.verify(password, hashed_password):
            print("❌ Password verification failed!")
            return
        print("✅ Password verification successful!")

        print(f"\n🔍 Step 4: Determining user role...")
        if is_superuser is True:
            user_role = "admin"
        elif "doctor" in email.lower():
            user_role = "doctor"
        elif "secretary" in email.lower():
            user_role = "secretary"
        elif "patient" in email.lower():
            user_role = "patient"
        else:
            user_role = "user"
        print(f"✅ User role: {user_role}")

        print(f"\n🔍 Step 5: Creating tokens...")
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_data = {
            "sub": email,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "type": "access",
            "exp": datetime.utcnow() + access_token_expires
        }
        
        access_token = jwt.encode(access_token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        print(f"✅ Access token created: {access_token[:50]}...")

        # Create refresh token
        refresh_token_expires = timedelta(days=7)
        refresh_token_data = {
            "sub": email,
            "user_id": user_id,
            "tenant_id": tenant_id,
            "type": "refresh",
            "exp": datetime.utcnow() + refresh_token_expires
        }
        
        refresh_token = jwt.encode(refresh_token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        print(f"✅ Refresh token created: {refresh_token[:50]}...")

        print(f"\n🎉 All steps completed successfully!")
        print(f"   User ID: {user_id}")
        print(f"   Role: {user_role}")
        print(f"   Type: {'staff' if user_role != 'patient' else 'patient'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    debug_staff_endpoint()
