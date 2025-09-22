#!/usr/bin/env python3
"""
Simple authentication service for database mode
Bypasses complex model relationships
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func

# Set environment variables
os.environ["USE_SQLITE"] = "true"
os.environ["USE_DATABASE"] = "true"
os.environ["ENVIRONMENT"] = "development"
os.environ["DEBUG"] = "true"

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import settings

# Create a simple base for our models
SimpleBase = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SimpleUser(SimpleBase):
    """Simple User model without complex relationships"""
    __tablename__ = "simple_users"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, nullable=True, default=1)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=True)
    full_name = Column(String(255), nullable=False)
    cpf = Column(String(14), unique=True, index=True, nullable=True)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    crm = Column(String(20), nullable=True)
    specialty = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime, nullable=True)

class SimpleAuthService:
    """Simple authentication service"""
    
    def __init__(self):
        self.engine = self._get_engine()
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def _get_engine(self):
        """Get database engine"""
        # Use SQLite for simplicity
        DATABASE_URL = "sqlite:///./clinicore_simple.db"
        return create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=False
        )
    
    def hash_password(self, password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: dict) -> str:
        """Create access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            raise Exception("Invalid token")
    
    def get_user_by_email(self, email: str) -> Optional[SimpleUser]:
        """Get user by email"""
        db = self.SessionLocal()
        try:
            return db.query(SimpleUser).filter(SimpleUser.email == email).first()
        finally:
            db.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[SimpleUser]:
        """Get user by ID"""
        db = self.SessionLocal()
        try:
            return db.query(SimpleUser).filter(SimpleUser.id == user_id).first()
        finally:
            db.close()
    
    def authenticate_user(self, email: str, password: str) -> Optional[SimpleUser]:
        """Authenticate user"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_tables(self):
        """Create tables"""
        SimpleBase.metadata.create_all(bind=self.engine)
    
    def create_sample_users(self):
        """Create sample users"""
        db = self.SessionLocal()
        try:
            # Check if users already exist
            if db.query(SimpleUser).first():
                print("✅ Users already exist")
                return
            
            # Create admin user
            admin_user = SimpleUser(
                id=1,
                tenant_id=1,
                email="admin@clinicore.com",
                username="admin",
                full_name="Administrator",
                cpf="12345678901",
                phone="11999999999",
                hashed_password=self.hash_password("admin123"),
                is_active=True,
                is_verified=True,
                is_superuser=True,
                crm="12345",
                specialty="General Medicine",
                created_at=datetime.now(),
                last_login=datetime.now()
            )
            db.add(admin_user)
            
            # Create doctor user
            doctor_user = SimpleUser(
                id=2,
                tenant_id=1,
                email="doctor@clinicore.com",
                username="doctor",
                full_name="Dr. João Silva",
                cpf="98765432100",
                phone="11988888888",
                hashed_password=self.hash_password("doctor123"),
                is_active=True,
                is_verified=True,
                crm="54321",
                specialty="Cardiology",
                created_at=datetime.now(),
                last_login=datetime.now()
            )
            db.add(doctor_user)
            
            # Create secretary user
            secretary_user = SimpleUser(
                id=3,
                tenant_id=1,
                email="secretary@clinicore.com",
                username="secretary",
                full_name="Maria Santos",
                cpf="11122233344",
                phone="11977777777",
                hashed_password=self.hash_password("secretary123"),
                is_active=True,
                is_verified=True,
                created_at=datetime.now(),
                last_login=datetime.now()
            )
            db.add(secretary_user)
            
            db.commit()
            print("✅ Sample users created")
            
            print("\n📋 Login Credentials:")
            print("   Admin: admin@clinicore.com / admin123")
            print("   Doctor: doctor@clinicore.com / doctor123")
            print("   Secretary: secretary@clinicore.com / secretary123")
            
        except Exception as e:
            print(f"❌ Error creating users: {e}")
            db.rollback()
            raise
        finally:
            db.close()

def main():
    """Main initialization function"""
    print("🗄️ Setting up Simple Database Authentication...")
    print("=" * 60)
    
    auth_service = SimpleAuthService()
    
    # Create tables
    print("🏗️ Creating database tables...")
    auth_service.create_tables()
    print("✅ Tables created")
    
    # Create sample users
    print("👤 Creating sample users...")
    auth_service.create_sample_users()
    
    print("=" * 60)
    print("✅ Simple database setup completed!")
    print("🚀 You can now start the server with: python run_server.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
