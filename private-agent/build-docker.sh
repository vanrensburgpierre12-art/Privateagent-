#!/bin/bash

# Private Agent Platform - Docker Build Script
# This script builds and runs the platform with proper sentence transformers support

set -e

echo "🚀 Building Private Agent Platform with Sentence Transformers..."

# Create data directory if it doesn't exist
mkdir -p ./data/chroma

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down || true

# Remove old images to force rebuild
echo "🗑️  Removing old images..."
docker-compose down --rmi all || true

# Build with no cache to ensure fresh dependencies
echo "🔨 Building fresh images..."
docker-compose build --no-cache

# Start the services
echo "▶️  Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
if curl -s http://localhost:8000/api/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "❌ Backend failed to start"
    docker-compose logs backend
    exit 1
fi

if curl -s http://localhost:5173 > /dev/null; then
    echo "✅ Frontend is running at http://localhost:5173"
else
    echo "❌ Frontend failed to start"
    docker-compose logs frontend
    exit 1
fi

echo ""
echo "🎉 Private Agent Platform is ready!"
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop services: docker-compose down"
echo "  Restart: docker-compose restart"
echo ""
echo "⚠️  Note: Make sure Ollama is running locally for AI functionality"
echo "   Install: curl -fsSL https://ollama.com/install.sh | sh"
echo "   Start: ollama serve"
echo "   Pull model: ollama pull llama-3.2-70b"