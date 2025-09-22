#!/usr/bin/env python3
"""
Update admin user to be superuser
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

def update_admin():
    """Update admin user to be superuser"""
    try:
        from app.database.database import get_engine
        from sqlalchemy import text
        
        # Get database engine
        engine = get_engine()
        
        with engine.connect() as conn:
            # Update admin user to be superuser
            result = conn.execute(text("""
                UPDATE users 
                SET is_superuser = true 
                WHERE email = 'admin@prontivus.com'
            """))
            
            conn.commit()
            print("✅ Updated admin user to superuser")
            
            # Verify the update
            result = conn.execute(text("""
                SELECT email, is_superuser 
                FROM users 
                WHERE email = 'admin@prontivus.com'
            """))
            
            user = result.fetchone()
            if user:
                print(f"✅ Verification: {user[0]} is_superuser = {user[1]}")
            else:
                print("❌ User not found")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    update_admin()
