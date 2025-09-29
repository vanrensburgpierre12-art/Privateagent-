"""Agent management API endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ..core.agent_manager import agent_manager
from ..core.schemas import AgentConfig

router = APIRouter()

class CreateAgentRequest(BaseModel):
    agent_id: str
    name: str
    system_prompt: str
    model_override: Optional[str] = None

@router.get("/agents", response_model=List[AgentConfig])
async def list_agents():
    """List all available agents."""
    try:
        agents = agent_manager.list_agents()
        return [
            AgentConfig(
                agent_id=agent["agent_id"],
                name=agent["name"],
                system_prompt=agent["system_prompt"],
                model_override=agent.get("model_override"),
                created_at=agent["created_at"]
            )
            for agent in agents
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agents", response_model=AgentConfig)
async def create_agent(request: CreateAgentRequest):
    """Create a new agent."""
    try:
        agent_config = agent_manager.create_agent(
            agent_id=request.agent_id,
            name=request.name,
            system_prompt=request.system_prompt,
            model_override=request.model_override
        )
        
        return AgentConfig(
            agent_id=request.agent_id,
            name=agent_config["name"],
            system_prompt=agent_config["system_prompt"],
            model_override=agent_config.get("model_override"),
            created_at=agent_config["created_at"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/agents/{agent_id}", response_model=AgentConfig)
async def get_agent(agent_id: str):
    """Get a specific agent configuration."""
    try:
        agent = agent_manager.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        return AgentConfig(
            agent_id=agent_id,
            name=agent["name"],
            system_prompt=agent["system_prompt"],
            model_override=agent.get("model_override"),
            created_at=agent["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))