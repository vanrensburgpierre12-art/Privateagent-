"""Agent manager for handling RAG-based conversations."""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from ..config import settings
from .ollama_client import ollama_client
from .chroma_store import chroma_store
from .schemas import ChatResponse

logger = logging.getLogger(__name__)

class AgentManager:
    """Manages agents and their interactions."""
    
    def __init__(self):
        self.agents = {
            "default": {
                "name": "Default Assistant",
                "system_prompt": """You are a helpful private assistant. Use only explicitly provided documents and knowledge from the private vector store to answer user queries. If the information is missing, say you don't know and ask clarifying questions. When you include facts from documents, annotate each answer with a "SOURCES:" section listing the filename and chunk id used.""",
                "model_override": None,
                "created_at": datetime.now()
            }
        }
    
    async def ask_agent(
        self, 
        agent_id: str, 
        user_input: str, 
        history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Process a user query with the specified agent."""
        if history is None:
            history = []
        
        try:
            # Get agent configuration
            agent_config = self.agents.get(agent_id)
            if not agent_config:
                raise Exception(f"Agent {agent_id} not found")
            
            # Retrieve relevant documents
            relevant_docs = chroma_store.query(user_input, top_k=5)
            
            # Build context from retrieved documents
            context = self._build_context(relevant_docs)
            
            # Build system prompt with context
            system_prompt = self._build_system_prompt(agent_config["system_prompt"], context)
            
            # Build conversation history
            conversation_history = self._build_conversation_history(history, user_input)
            
            # Generate response
            model_name = agent_config.get("model_override") or settings.OLLAMA_MODEL
            response_text = await ollama_client.generate(
                prompt=conversation_history,
                model_name=model_name,
                max_tokens=settings.MAX_CONTEXT_TOKENS,
                system_prompt=system_prompt,
                stream=False
            )
            
            # Store conversation in memory
            self._store_conversation(user_input, response_text, agent_id)
            
            # Format sources
            sources = self._format_sources(relevant_docs)
            
            return {
                "answer": response_text,
                "sources": sources,
                "model": model_name,
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Agent query failed: {e}")
            raise Exception(f"Agent query failed: {str(e)}")
    
    def _build_context(self, relevant_docs: List[Dict[str, Any]]) -> str:
        """Build context string from relevant documents."""
        if not relevant_docs:
            return "No relevant documents found in the knowledge base."
        
        context_parts = ["Relevant documents from knowledge base:"]
        for i, doc in enumerate(relevant_docs, 1):
            filename = doc["metadata"].get("filename", "unknown")
            chunk_id = doc["metadata"].get("chunk_id", "unknown")
            text = doc["text"][:500] + "..." if len(doc["text"]) > 500 else doc["text"]
            context_parts.append(f"{i}. From {filename} (chunk {chunk_id}): {text}")
        
        return "\n\n".join(context_parts)
    
    def _build_system_prompt(self, base_prompt: str, context: str) -> str:
        """Build the complete system prompt with context."""
        return f"{base_prompt}\n\n{context}"
    
    def _build_conversation_history(self, history: List[Dict[str, str]], current_input: str) -> str:
        """Build conversation history string."""
        if not history:
            return current_input
        
        history_parts = []
        for msg in history[-5:]:  # Keep last 5 messages
            role = msg.get("role", "user")
            content = msg.get("content", "")
            history_parts.append(f"{role}: {content}")
        
        history_parts.append(f"user: {current_input}")
        return "\n".join(history_parts)
    
    def _format_sources(self, relevant_docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Format sources for response."""
        sources = []
        for doc in relevant_docs:
            sources.append({
                "filename": doc["metadata"].get("filename", "unknown"),
                "chunk_id": doc["metadata"].get("chunk_id", "unknown"),
                "text": doc["text"][:200] + "..." if len(doc["text"]) > 200 else doc["text"],
                "distance": doc.get("distance", 0.0)
            })
        return sources
    
    def _store_conversation(self, user_input: str, response: str, agent_id: str):
        """Store conversation in memory."""
        try:
            # Create conversation chunks
            conversation_text = f"User: {user_input}\nAssistant: {response}"
            
            # Split conversation into chunks
            from langchain.text_splitter import CharacterTextSplitter
            splitter = CharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            chunks = splitter.split_text(conversation_text)
            
            # Generate embeddings and store
            from .embeddings import embedding_generator
            embeddings = embedding_generator.get_embeddings(chunks)
            
            import uuid
            ids = [str(uuid.uuid4()) for _ in chunks]
            metadatas = [{
                "type": "conversation",
                "agent_id": agent_id,
                "timestamp": datetime.now().isoformat(),
                "filename": "conversation",
                "chunk_id": f"conv_{i}"
            } for i in range(len(chunks))]
            
            chroma_store.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            
        except Exception as e:
            logger.warning(f"Failed to store conversation: {e}")
    
    def create_agent(self, agent_id: str, name: str, system_prompt: str, model_override: Optional[str] = None) -> Dict[str, Any]:
        """Create a new agent."""
        if agent_id in self.agents:
            raise Exception(f"Agent {agent_id} already exists")
        
        self.agents[agent_id] = {
            "name": name,
            "system_prompt": system_prompt,
            "model_override": model_override,
            "created_at": datetime.now()
        }
        
        logger.info(f"Created new agent: {agent_id}")
        return self.agents[agent_id]
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all available agents."""
        return [
            {
                "agent_id": agent_id,
                "name": config["name"],
                "system_prompt": config["system_prompt"],
                "model_override": config.get("model_override"),
                "created_at": config["created_at"]
            }
            for agent_id, config in self.agents.items()
        ]
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent configuration."""
        return self.agents.get(agent_id)

# Global agent manager instance
agent_manager = AgentManager()