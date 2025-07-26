from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    id: Optional[str] = None
    content: str = Field(..., min_length=1, max_length=1000)
    message_type: MessageType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    message: str
    session_id: str
    timestamp: datetime
    suggestions: Optional[List[str]] = None
    quick_replies: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class Conversation(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime
    user_id: Optional[str] = None
    status: str = "active"

class ChatSession(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    last_activity: datetime
    message_count: int = 0
    is_active: bool = True 