"""Memory management API endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List
from ..core.schemas import MemoryItem
from ..core.chroma_store import chroma_store

router = APIRouter()

@router.get("/memory", response_model=List[MemoryItem])
async def list_memories():
    """List all memories in the vector store."""
    try:
        memories = chroma_store.list_memories()
        return [
            MemoryItem(
                id=memory["id"],
                text=memory["text"],
                metadata=memory["metadata"],
                filename=memory["metadata"].get("filename"),
                chunk_id=memory["metadata"].get("chunk_id")
            )
            for memory in memories
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/memory/{memory_id}")
async def delete_memory(memory_id: str):
    """Delete a specific memory by ID."""
    try:
        success = chroma_store.delete_memory(memory_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Memory {memory_id} not found")
        
        return {"message": f"Memory {memory_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/memory")
async def clear_all_memories():
    """Clear all memories from the vector store."""
    try:
        success = chroma_store.clear_store()
        if not success:
            raise HTTPException(status_code=500, detail="Failed to clear memories")
        
        return {"message": "All memories cleared successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))