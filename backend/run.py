#!/usr/bin/env python3
"""
Insurance Quote Comparison Backend Server
Run this script to start the backend API server
"""

import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting Insurance Quote Comparison Backend API...")
    print("📋 Professional backend for Next.js frontend integration")
    print("🔗 Backend API will be available at: http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/docs")
    print("📚 API Redoc: http://localhost:5000/redoc")
    print("🌐 Production URL: https://mailbroker.ddns.net:5000")
    print("🔗 Frontend URL: https://mailbroker.ddns.net:3000")
    print("\n" + "="*60)
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=5000, 
        reload=True,
        log_level="info"
    ) 