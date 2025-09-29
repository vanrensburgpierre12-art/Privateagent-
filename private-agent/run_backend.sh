#!/bin/bash

# Script to run the backend with the virtual environment
# This fixes the sentence-transformers installation issue

echo "Starting Private Agent Backend..."

# Activate virtual environment
source venv/bin/activate

# Set environment variables (you can modify these as needed)
export OLLAMA_URL=${OLLAMA_URL:-http://34.58.166.165:11535}
export OLLAMA_MODEL=${OLLAMA_MODEL:-llama2:latest}
export CHROMA_PERSIST_DIR=${CHROMA_PERSIST_DIR:-./data/chroma}
export EMBEDDINGS_PROVIDER=${EMBEDDINGS_PROVIDER:-sentence_transformers}
export OLLAMA_EMBEDDING_MODEL=${OLLAMA_EMBEDDING_MODEL:-nomic-embed-text}
export EMBEDDING_MODEL=${EMBEDDING_MODEL:-sentence-transformers/all-MiniLM-L6-v2}
export MAX_CONTEXT_TOKENS=${MAX_CONTEXT_TOKENS:-4000}
export CHUNK_SIZE=${CHUNK_SIZE:-500}
export CHUNK_OVERLAP=${CHUNK_OVERLAP:-50}
export CORS_ORIGINS=${CORS_ORIGINS:-http://34.58.166.165:5173,http://34.58.166.165:3000}
export LOG_LEVEL=${LOG_LEVEL:-INFO}

# Set Python path
export PYTHONPATH=/workspace/private-agent/backend

# Create chroma directory if it doesn't exist
mkdir -p ./data/chroma

# Change to backend directory
cd backend

# Run the FastAPI application
echo "Starting FastAPI server on http://0.0.0.0:8000"
echo "API documentation available at http://0.0.0.0:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload