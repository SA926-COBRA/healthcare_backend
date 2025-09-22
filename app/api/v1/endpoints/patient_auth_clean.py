"""
Patient Portal Authentication Endpoints
Patients can only access the patient portal, not the main system
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Any

from app.database.database import get_db
from app.core.exceptions import AuthenticationError, ValidationError
from app.schemas.auth import Token, UserLogin
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/login", response_model=Token)
async def patient_login(
    login_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
) -> Any:
    """Patient portal login - Only patients allowed"""
    try:
        # Use AuthService for authentication
        auth_service = AuthService(db)
        token = auth_service.authenticate_user(login_data.email_or_cpf, login_data.password, request)
        return token
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/logout")
async def patient_logout(
    request: Request,
    db: Session = Depends(get_db)
) -> Any:
    """Patient portal logout"""
    try:
        # Simple logout - just return success
        return {"message": "Logged out successfully from patient portal"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout error: {str(e)}"
        )
