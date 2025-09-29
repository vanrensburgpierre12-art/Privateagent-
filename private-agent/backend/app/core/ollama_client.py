"""Ollama client for interacting with local Ollama API."""
import os
import httpx
import asyncio
import logging
from typing import Optional, AsyncGenerator, Dict, Any
from ..config import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = 600  # 10 minutes for large models
        
    async def health_check(self) -> bool:
        """Check if Ollama is accessible."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False
    
    async def generate(
        self, 
        prompt: str, 
        model_name: Optional[str] = None,
        max_tokens: int = 512, 
        stream: bool = False, 
        system_prompt: Optional[str] = None,
        stop: Optional[List[str]] = None
    ) -> AsyncGenerator[str, None] | str:
        """Generate text using Ollama API."""
        model = model_name or self.model
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        if stop:
            payload["options"]["stop"] = stop
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if stream:
                    async with client.stream(
                        "POST", 
                        f"{self.base_url}/api/generate", 
                        json=payload
                    ) as response:
                        response.raise_for_status()
                        async for line in response.aiter_lines():
                            if line.strip():
                                try:
                                    import json
                                    data = json.loads(line)
                                    if "response" in data:
                                        yield data["response"]
                                    if data.get("done", False):
                                        break
                                except:
                                    continue
                else:
                    response = await client.post(
                        f"{self.base_url}/api/generate", 
                        json=payload
                    )
                    response.raise_for_status()
                    data = response.json()
                    return data.get("response", "")
                    
        except httpx.TimeoutException:
            logger.error("Ollama request timed out")
            raise Exception("Request timed out - model may be too large for available resources")
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error: {e}")
            raise Exception(f"Ollama API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Ollama request failed: {e}")
            raise Exception(f"Failed to generate response: {str(e)}")

# Global client instance
ollama_client = OllamaClient()