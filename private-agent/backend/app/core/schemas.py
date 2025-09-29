"""Pydantic schemas for the private agent platform."""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    agent_id: str = "default"
    message: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    answer: str
    sources: List[Dict[str, Any]]
    model: str
    timestamp: datetime

class UploadResponse(BaseModel):
    """Response schema for upload endpoint."""
    message: str
    chunks_created: int
    filename: str
    file_size: int

class MemoryItem(BaseModel):
    """Schema for memory items."""
    id: str
    text: str
    metadata: Dict[str, Any]
    filename: Optional[str] = None
    chunk_id: Optional[str] = None

class AgentConfig(BaseModel):
    """Schema for agent configuration."""
    agent_id: str
    name: str
    system_prompt: str
    model_override: Optional[str] = None
    created_at: datetime

class HealthResponse(BaseModel):
    """Response schema for health endpoint."""
    status: str
    ollama_connected: bool
    chroma_connected: bool
    timestamp: datetime