"""
Simple authentication endpoint that bypasses complex ORM relationships
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Any
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.database.database import get_db
from app.schemas.auth import Token, UserLogin
from app.core.config import settings

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

@router.post("/login", response_model=Token)
async def simple_login(
    login_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
) -> Any:
    """Simple login using direct SQL queries"""
    try:
        # Find user by email or CPF using direct SQL
        cursor = db.execute(text("""
            SELECT id, email, username, hashed_password, is_active, tenant_id, is_superuser
            FROM users
            WHERE email = :email_or_cpf OR cpf = :email_or_cpf
        """), {"email_or_cpf": login_data.email_or_cpf})

        user_row = cursor.fetchone()
        if not user_row:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        user_id, email, username, hashed_password, is_active, tenant_id, is_superuser = user_row

        # Check if user is active
        if not is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )

        # Verify password
        if not pwd_context.verify(login_data.password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # Determine user role
        if is_superuser:
            user_role = "admin"
        elif "doctor" in email.lower():
            user_role = "doctor"
        elif "secretary" in email.lower():
            user_role = "secretary"
        elif "patient" in email.lower():
            user_role = "patient"
        else:
            user_role = "user"

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

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user_id=user_id,
            user_role=user_role,
            user_type="staff" if user_role != "patient" else "patient",
            requires_2fa=False,
            must_reset_password=False
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )
