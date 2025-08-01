#!/usr/bin/env python3
"""
SmartCloud AI - Startup Script
Run this to start the application
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    print("🚀 Starting SmartCloud AI...")
    print(f"📡 Server will be available at http://localhost:{port}")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    ) 