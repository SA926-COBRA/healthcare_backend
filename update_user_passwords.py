#!/usr/bin/env python3
"""
Update existing users with known passwords for testing
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.database import get_engine
from sqlalchemy import text
from passlib.context import CryptContext

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

def update_user_passwords():
    """Update existing users with known passwords"""
    
    # Set environment variables
    os.environ["DATABASE_URL"] = "postgresql://prontibus_user:j1TNfXAeaD1fyNY5RPV68psq0JmwodLV@dpg-d38mtsogjchc73d6ovdg-a.oregon-postgres.render.com/prontibus"
    os.environ["USE_SQLITE"] = "false"
    os.environ["USE_DATABASE"] = "true"
    
    try:
        # Get database engine
        engine = get_engine()
        
        with engine.connect() as conn:
            # Hash passwords
            admin_password = pwd_context.hash("admin123")
            doctor_password = pwd_context.hash("doctor123")
            secretary_password = pwd_context.hash("secretary123")
            patient_password = pwd_context.hash("patient123")
            test_password = pwd_context.hash("test123")
            
            # Update existing users with known passwords
            users_to_update = [
                ("admin@prontivus.com", admin_password, "admin123"),
                ("doctor@prontivus.com", doctor_password, "doctor123"),
                ("secretary@prontivus.com", secretary_password, "secretary123"),
                ("patient@prontivus.com", patient_password, "patient123"),
            ]
            
            for email, hashed_password, plain_password in users_to_update:
                # Check if user exists
                result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": email})
                user = result.fetchone()
                
                if user:
                    # Update password
                    conn.execute(text("""
                        UPDATE users 
                        SET hashed_password = :password, 
                            updated_at = NOW()
                        WHERE email = :email
                    """), {"password": hashed_password, "email": email})
                    print(f"✅ Updated {email} with password: {plain_password}")
                else:
                    print(f"⚠️ User {email} not found")
            
            # Create a new test user if it doesn't exist
            test_user_result = conn.execute(text("SELECT id FROM users WHERE email = :email"), {"email": "test@prontivus.com"})
            test_user = test_user_result.fetchone()
            
            if not test_user:
                # Insert new test user
                conn.execute(text("""
                    INSERT INTO users (
                        tenant_id, email, username, full_name, hashed_password, 
                        is_active, is_verified, is_superuser, must_reset_password,
                        created_at, updated_at
                    ) VALUES (
                        1, :email, :username, :full_name, :password,
                        true, true, true, false,
                        NOW(), NOW()
                    )
                """), {
                    "email": "test@prontivus.com",
                    "username": "testuser",
                    "full_name": "Test User",
                    "password": test_password
                })
                print(f"✅ Created test@prontivus.com with password: test123")
            else:
                # Update existing test user
                conn.execute(text("""
                    UPDATE users 
                    SET hashed_password = :password, 
                        updated_at = NOW()
                    WHERE email = :email
                """), {"password": test_password, "email": "test@prontivus.com"})
                print(f"✅ Updated test@prontivus.com with password: test123")
            
            # Commit changes
            conn.commit()
            
            print("\n🎉 User passwords updated successfully!")
            print("📧 Test credentials:")
            print("   admin@prontivus.com / admin123")
            print("   doctor@prontivus.com / doctor123")
            print("   secretary@prontivus.com / secretary123")
            print("   patient@prontivus.com / patient123")
            print("   test@prontivus.com / test123")
        
    except Exception as e:
        print(f"❌ Error updating passwords: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_user_passwords()
