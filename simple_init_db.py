#!/usr/bin/env python3
"""
Simple database initialization script for CliniCore
Creates only essential tables and basic data
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Set environment variables
os.environ["USE_SQLITE"] = "true"
os.environ["USE_DATABASE"] = "true"
os.environ["ENVIRONMENT"] = "development"
os.environ["DEBUG"] = "true"

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.database.database import get_engine, test_connection
from app.models.base import Base
from app.models.user import User, Role, UserRole
from app.services.auth_service import AuthService
from sqlalchemy.orm import sessionmaker

def create_minimal_tables():
    """Create only the essential tables"""
    print("🏗️ Creating essential database tables...")
    
    engine = get_engine()
    
    # Create only the essential tables
    Base.metadata.create_all(bind=engine, tables=[
        User.__table__,
        Role.__table__,
        UserRole.__table__
    ])
    
    print("✅ Essential tables created")

def create_basic_data():
    """Create basic user data"""
    print("👤 Creating basic user data...")
    
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    auth_service = AuthService(db)
    
    try:
        # Create admin role
        admin_role = Role(
            id=1,
            name="admin",
            description="System Administrator",
            permissions=["read", "write", "admin"],
            created_at=datetime.now()
        )
        db.add(admin_role)
        db.flush()
        
        # Create doctor role
        doctor_role = Role(
            id=2,
            name="doctor",
            description="Medical Doctor",
            permissions=["read", "write"],
            created_at=datetime.now()
        )
        db.add(doctor_role)
        db.flush()
        
        # Create secretary role
        secretary_role = Role(
            id=3,
            name="secretary",
            description="Secretary/Receptionist",
            permissions=["read", "write"],
            created_at=datetime.now()
        )
        db.add(secretary_role)
        db.flush()
        
        # Create admin user
        admin_user = User(
            id=1,
            tenant_id=1,
            email="admin@clinicore.com",
            username="admin",
            full_name="Administrator",
            cpf="12345678901",
            phone="11999999999",
            hashed_password=auth_service.hash_password("admin123"),
            is_active=True,
            is_verified=True,
            is_superuser=True,
            crm="12345",
            specialty="General Medicine",
            created_at=datetime.now(),
            last_login=datetime.now()
        )
        db.add(admin_user)
        db.flush()
        
        # Assign admin role
        admin_user_role = UserRole(
            user_id=admin_user.id,
            role_id=admin_role.id,
            tenant_id=1,
            created_at=datetime.now()
        )
        db.add(admin_user_role)
        
        # Create doctor user
        doctor_user = User(
            id=2,
            tenant_id=1,
            email="doctor@clinicore.com",
            username="doctor",
            full_name="Dr. João Silva",
            cpf="98765432100",
            phone="11988888888",
            hashed_password=auth_service.hash_password("doctor123"),
            is_active=True,
            is_verified=True,
            crm="54321",
            specialty="Cardiology",
            created_at=datetime.now(),
            last_login=datetime.now()
        )
        db.add(doctor_user)
        db.flush()
        
        # Assign doctor role
        doctor_user_role = UserRole(
            user_id=doctor_user.id,
            role_id=doctor_role.id,
            tenant_id=1,
            created_at=datetime.now()
        )
        db.add(doctor_user_role)
        
        # Create secretary user
        secretary_user = User(
            id=3,
            tenant_id=1,
            email="secretary@clinicore.com",
            username="secretary",
            full_name="Maria Santos",
            cpf="11122233344",
            phone="11977777777",
            hashed_password=auth_service.hash_password("secretary123"),
            is_active=True,
            is_verified=True,
            created_at=datetime.now(),
            last_login=datetime.now()
        )
        db.add(secretary_user)
        db.flush()
        
        # Assign secretary role
        secretary_user_role = UserRole(
            user_id=secretary_user.id,
            role_id=secretary_role.id,
            tenant_id=1,
            created_at=datetime.now()
        )
        db.add(secretary_user_role)
        
        db.commit()
        print("✅ Basic user data created")
        
        print("\n📋 Login Credentials:")
        print("   Admin: admin@clinicore.com / admin123")
        print("   Doctor: doctor@clinicore.com / doctor123")
        print("   Secretary: secretary@clinicore.com / secretary123")
        
    except Exception as e:
        print(f"❌ Error creating basic data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def main():
    """Main initialization function"""
    print("🗄️ Initializing CliniCore Database (Minimal Setup)...")
    print("=" * 60)
    
    # Test database connection
    if not test_connection():
        print("❌ Database connection failed!")
        return False
    
    # Create minimal tables
    create_minimal_tables()
    
    # Create basic data
    create_basic_data()
    
    print("=" * 60)
    print("✅ Minimal database initialization completed!")
    print("🚀 You can now start the server with: python run_server.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
