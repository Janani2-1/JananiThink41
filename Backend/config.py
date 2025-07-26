from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "E-commerce Customer Support Chatbot"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./chatbot.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Redis Configuration (for caching and sessions)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Chatbot Configuration
    CHATBOT_NAME: str = "StyleBot"
    CHATBOT_WELCOME_MESSAGE: str = "Hello! I'm StyleBot, your fashion assistant. How can I help you today?"
    MAX_CONVERSATION_HISTORY: int = 50
    
    # Product Catalog
    PRODUCTS_PER_PAGE: int = 20
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 