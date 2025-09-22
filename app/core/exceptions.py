"""
Custom exceptions for CliniCore
"""

from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class CliniCoreException(Exception):
    """Base exception for CliniCore"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class AuthenticationError(CliniCoreException):
    """Authentication related errors"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class AuthorizationError(CliniCoreException):
    """Authorization related errors"""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )

class ValidationError(CliniCoreException):
    """Validation related errors"""
    
    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )

class NotFoundError(CliniCoreException):
    """Resource not found errors"""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

class ConflictError(CliniCoreException):
    """Resource conflict errors"""
    
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT
        )

class LicenseError(CliniCoreException):
    """License related errors"""
    
    def __init__(self, message: str = "License error"):
        super().__init__(
            message=message,
            status_code=status.HTTP_402_PAYMENT_REQUIRED
        )

class MedicalRecordError(CliniCoreException):
    """Medical record related errors"""
    
    def __init__(self, message: str = "Medical record error"):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )

async def clini_core_exception_handler(request, exc: CliniCoreException):
    """Handle CliniCore exceptions"""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "message": exc.message,
            "details": exc.details
        }
    )
