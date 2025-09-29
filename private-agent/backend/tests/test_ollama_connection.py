"""Tests for Ollama client connectivity."""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.core.ollama_client import OllamaClient

class TestOllamaConnection:
    """Test Ollama client connection and health checks."""
    
    @pytest.mark.asyncio
    async def test_health_check_success(self):
        """Test successful health check."""
        client = OllamaClient()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await client.health_check()
            assert result is True
    
    @pytest.mark.asyncio
    async def test_health_check_failure(self):
        """Test failed health check."""
        client = OllamaClient()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = Exception("Connection failed")
            
            result = await client.health_check()
            assert result is False
    
    @pytest.mark.asyncio
    async def test_generate_success(self):
        """Test successful text generation."""
        client = OllamaClient()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"response": "Test response"}
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await client.generate("Test prompt")
            assert result == "Test response"
    
    @pytest.mark.asyncio
    async def test_generate_with_system_prompt(self):
        """Test generation with system prompt."""
        client = OllamaClient()
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"response": "Test response"}
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await client.generate(
                "Test prompt",
                system_prompt="You are a helpful assistant"
            )
            assert result == "Test response"
    
    @pytest.mark.asyncio
    async def test_generate_timeout(self):
        """Test generation timeout handling."""
        client = OllamaClient()
        
        with patch('httpx.AsyncClient') as mock_client:
            import httpx
            mock_client.return_value.__aenter__.return_value.post.side_effect = httpx.TimeoutException("Timeout")
            
            with pytest.raises(Exception, match="Request timed out"):
                await client.generate("Test prompt")