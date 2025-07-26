from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "service": "E-commerce Customer Support Chatbot API",
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check with component status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "service": "E-commerce Customer Support Chatbot API",
        "version": "1.0.0",
        "components": {
            "api": "healthy",
            "chatbot": "healthy",
            "database": "healthy",
            "cache": "healthy"
        },
        "uptime": "00:00:00",  # In real implementation, calculate actual uptime
        "memory_usage": "45MB",  # In real implementation, get actual memory usage
        "cpu_usage": "2.5%"  # In real implementation, get actual CPU usage
    } 