"""Chat API endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List
from ..core.schemas import ChatRequest, ChatResponse
from ..core.agent_manager import agent_manager

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message with the specified agent."""
    try:
        result = await agent_manager.ask_agent(
            agent_id=request.agent_id,
            user_input=request.message,
            history=request.history
        )
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            model=result["model"],
            timestamp=result["timestamp"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))