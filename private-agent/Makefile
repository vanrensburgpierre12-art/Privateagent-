.PHONY: help build up down test clean dev-backend dev-frontend

# Default target
help:
	@echo "Available commands:"
	@echo "  build          - Build all Docker images"
	@echo "  up             - Start all services"
	@echo "  down           - Stop all services"
	@echo "  test           - Run backend tests"
	@echo "  clean          - Clean up containers and volumes"
	@echo "  dev-backend    - Run backend in development mode"
	@echo "  dev-frontend   - Run frontend in development mode"
	@echo "  logs           - Show logs from all services"

# Build all images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# Run tests
test:
	docker-compose run --rm backend python -m pytest tests/ -v

# Clean up
clean:
	docker-compose down -v
	docker system prune -f

# Development mode - backend
dev-backend:
	cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Development mode - frontend
dev-frontend:
	cd frontend && npm run dev

# Show logs
logs:
	docker-compose logs -f

# Install Ollama (macOS/Linux)
install-ollama:
	@echo "Installing Ollama..."
	@echo "Visit https://ollama.com/docs for installation instructions"
	@echo "After installation, run: ollama pull llama-3.2-70b"

# Pull model
pull-model:
	ollama pull llama-3.2-70b

# Start Ollama server
start-ollama:
	ollama serve