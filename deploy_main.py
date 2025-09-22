#!/usr/bin/env python3
"""
Deployment-ready FastAPI application for Prontivus
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables explicitly for Render deployment
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "postgresql://prontibus_user:j1TNfXAeaD1fyNY5RPV68psq0JmwodLV@dpg-d38mtsogjchc73d6ovdg-a.oregon-postgres.render.com/prontibus"

if not os.getenv("USE_SQLITE"):
    os.environ["USE_SQLITE"] = "false"

if not os.getenv("USE_DATABASE"):
    os.environ["USE_DATABASE"] = "true"

if not os.getenv("ENVIRONMENT"):
    os.environ["ENVIRONMENT"] = "production"

if not os.getenv("DEBUG"):
    os.environ["DEBUG"] = "false"

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import our application
from app.main import app as clinicore_app

# Initialize FastAPI app with deployment settings
app = FastAPI(
    title="Prontivus Medical Management System",
    version="1.0.0",
    description="Comprehensive medical management system for clinics and hospitals in Brazil",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
# Default origins including Vercel frontend
default_origins = [
    "https://healthcare-frontend-3.vercel.app",
    "https://healthcare-frontend-3.vercel.app/",
    "http://localhost:3000",
    "http://localhost:8080"
]

allowed_origins = os.getenv("ALLOWED_ORIGINS", ",".join(default_origins)).split(",")
print(f"🌐 CORS Allowed Origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes from our main app
app.include_router(clinicore_app.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Prontivus Medical Management System",
        "version": "1.0.0",
        "status": "online",
        "database": "PostgreSQL" if os.getenv("USE_SQLITE", "true").lower() == "false" else "SQLite"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }

# Setup OAuth2 scheme for Swagger UI login flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Custom OpenAPI schema with security configuration
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Apply global security requirement
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Run the app using Uvicorn when executed directly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Prontivus Backend Server...")
    print(f"📡 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    print("=" * 60)
    
    uvicorn.run(
        "deploy_main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info",
        access_log=True
    )
