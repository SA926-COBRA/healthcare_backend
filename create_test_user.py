#!/usr/bin/env python3
"""
Create a test user with known credentials for frontend testing
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.database import get_engine, get_db
from app.services.auth_service import AuthService
from app.schemas.auth import StaffRegister
from app.models.user import User
from sqlalchemy.orm import Session
from sqlalchemy import text

def create_test_user():
    """Create a test user with known credentials"""
    
    # Set environment variables
    os.environ["DATABASE_URL"] = "postgresql://prontibus_user:j1TNfXAeaD1fyNY5RPV68psq0JmwodLV@dpg-d38mtsogjchc73d6ovdg-a.oregon-postgres.render.com/prontibus"
    os.environ["USE_SQLITE"] = "false"
    os.environ["USE_DATABASE"] = "true"
    
    try:
        # Get database session
        db = next(get_db())
        
        # Create auth service
        auth_service = AuthService(db)
        
        # Check if test user already exists
        existing_user = db.query(User).filter(
            User.email == "test@prontivus.com"
        ).first()
        
        if existing_user:
            print(f"✅ Test user already exists: {existing_user.email}")
            # Update password
            auth_service.set_password(existing_user, "test123")
            db.commit()
            print("✅ Password updated to: test123")
        else:
            # Create test user data
            test_user_data = StaffRegister(
                email="test@prontivus.com",
                username="testuser",
                full_name="Test User",
                password="test123",
                role="admin",
                crm=None,
                specialty=None
            )
            
            # Create user
            user = auth_service.register_staff(test_user_data, 1)  # Created by admin (ID 1)
            print(f"✅ Test user created: {user.email}")
            print(f"   Username: {user.username}")
            print(f"   Password: test123")
            print(f"   Role: admin")
        
        # Also create a patient test user
        patient_data = StaffRegister(
            email="patient@test.com",
            username="testpatient",
            full_name="Test Patient",
            password="patient123",
            role="patient",
            crm=None,
            specialty=None
        )
        
        existing_patient = db.query(User).filter(
            User.email == "patient@test.com"
        ).first()
        
        if existing_patient:
            print(f"✅ Test patient already exists: {existing_patient.email}")
            auth_service.set_password(existing_patient, "patient123")
            db.commit()
            print("✅ Patient password updated to: patient123")
        else:
            patient = auth_service.register_staff(patient_data, 1)
            print(f"✅ Test patient created: {patient.email}")
            print(f"   Username: {patient.username}")
            print(f"   Password: patient123")
            print(f"   Role: patient")
        
        print("\n🎉 Test users ready for frontend testing!")
        print("📧 Admin: test@prontivus.com / test123")
        print("📧 Patient: patient@test.com / patient123")
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    create_test_user()
