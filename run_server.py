#!/usr/bin/env python3
"""
Robust server startup script for CliniCore Backend
"""

import os
import sys
import uvicorn
import signal
import time
from pathlib import Path

# Set environment variables (only if not already set)
if "USE_SQLITE" not in os.environ:
    os.environ["USE_SQLITE"] = "true"  # Use SQLite for development
if "USE_DATABASE" not in os.environ:
    os.environ["USE_DATABASE"] = "true"  # Use database endpoints for Prontivus
if "ENVIRONMENT" not in os.environ:
    os.environ["ENVIRONMENT"] = "development"
if "DEBUG" not in os.environ:
    os.environ["DEBUG"] = "true"

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print('\n🛑 Shutting down server gracefully...')
    sys.exit(0)

def main():
    """Main server startup function"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Determine mode based on environment variables
    use_database = os.environ.get("USE_DATABASE", "false").lower() == "true"
    use_sqlite = os.environ.get("USE_SQLITE", "true").lower() == "true"
    
    print("🚀 Starting Prontivus Backend Server...")
    if use_database:
        if use_sqlite:
            print("📱 Using SQLite Database (Offline Mode)")
        else:
            print("🌐 Using PostgreSQL Database (Online Mode)")
        print("🔐 Database Authentication Enabled")
    else:
        print("🎭 Using Mock Endpoints (Development)")
    
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host="localhost",
            port=8000,
            reload=False,  # Disable reload for stability
            log_level="info",
            access_log=True,
            loop="asyncio"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
