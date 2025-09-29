"""Health check API endpoints."""
from fastapi import APIRouter
from datetime import datetime
from ..core.schemas import HealthResponse
from ..core.ollama_client import ollama_client
from ..core.chroma_store import chroma_store

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health of all services."""
    try:
        # Check Ollama connectivity
        ollama_connected = await ollama_client.health_check()
        
        # Check ChromaDB connectivity
        chroma_connected = True
        try:
            chroma_store.list_memories()
        except Exception:
            chroma_connected = False
        
        # Determine overall status
        if ollama_connected and chroma_connected:
            status = "healthy"
        elif ollama_connected or chroma_connected:
            status = "degraded"
        else:
            status = "unhealthy"
        
        return HealthResponse(
            status=status,
            ollama_connected=ollama_connected,
            chroma_connected=chroma_connected,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        return HealthResponse(
            status="error",
            ollama_connected=False,
            chroma_connected=False,
            timestamp=datetime.now()
        )