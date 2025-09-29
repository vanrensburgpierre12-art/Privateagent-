# Private Agent Platform

A private, local agent platform that uses Ollama as the LLM host, ChromaDB as the vector store, and provides a React frontend for interaction. This system implements Retrieval-Augmented Generation (RAG) with multi-tool agent behavior and short/long term memory.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Ollama installed locally (see [Ollama Installation](#ollama-installation))

### 1. Clone and Setup

```bash
git clone <repository-url>
cd private-agent
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file with your settings:

```bash
# Ollama Configuration
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama-3.2-70b

# For smaller models (recommended for local development)
# OLLAMA_MODEL=llama-3.2-13b
# OLLAMA_MODEL=llama-3.2-8b
# OLLAMA_MODEL=mistral:7b
```

### 3. Start Services

```bash
# Using Makefile (recommended)
make build
make up

# Or using Docker Compose directly
docker-compose up --build
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🏗️ Architecture

### Components

- **Backend**: FastAPI application with RAG capabilities
- **Frontend**: React + Vite + Tailwind CSS
- **Vector Store**: ChromaDB with local persistence
- **LLM**: Ollama with configurable models
- **Embeddings**: Local sentence-transformers models

### Tech Stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn, LangChain
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS
- **Vector DB**: ChromaDB
- **LLM**: Ollama (LLaMA-3.2-70B, configurable)
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2

## 📋 Ollama Installation

### Install Ollama

Visit [Ollama Official Documentation](https://ollama.com/docs) for installation instructions.

**Quick install (Linux/macOS):**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Pull Models

```bash
# For powerful hardware (GPU recommended)
ollama pull llama-3.2-70b

# For moderate hardware
ollama pull llama-3.2-13b

# For limited hardware
ollama pull llama-3.2-8b
ollama pull mistral:7b
```

### Start Ollama Server

```bash
# Start Ollama server
ollama serve

# Or run in background
ollama serve &
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama-3.2-70b` | Model to use for generation |
| `CHROMA_PERSIST_DIR` | `./chroma_persist` | ChromaDB persistence directory |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |
| `MAX_CONTEXT_TOKENS` | `4000` | Maximum context tokens |
| `CHUNK_SIZE` | `500` | Document chunk size |
| `CHUNK_OVERLAP` | `50` | Chunk overlap size |

### Model Recommendations

| Hardware | Recommended Model | Memory Required |
|----------|------------------|-----------------|
| High-end GPU (24GB+) | `llama-3.2-70b` | ~40GB RAM |
| Mid-range GPU (8-16GB) | `llama-3.2-13b` | ~16GB RAM |
| CPU/Low-end GPU | `llama-3.2-8b` | ~8GB RAM |
| Very limited | `mistral:7b` | ~4GB RAM |

## 🛠️ Development

### Running Components Separately

#### Backend Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run with hot reload
make dev-backend
# or
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Development

```bash
# Install dependencies
cd frontend
npm install

# Run with hot reload
make dev-frontend
# or
npm run dev
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
docker-compose run --rm backend python -m pytest tests/test_ollama_connection.py -v
```

## 📚 API Endpoints

### Chat
- `POST /api/chat` - Send message to agent
- `GET /api/agents` - List available agents
- `POST /api/agents` - Create new agent

### Document Management
- `POST /api/upload` - Upload document (PDF, DOCX, TXT)
- `POST /api/upload-text` - Upload raw text

### Memory Management
- `GET /api/memory` - List all memories
- `DELETE /api/memory/{id}` - Delete specific memory
- `DELETE /api/memory` - Clear all memories

### System
- `GET /api/health` - Health check

### Example API Usage

```bash
# Upload a document
curl -X POST "http://localhost:8000/api/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"

# Send a chat message
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "default",
    "message": "What is the main topic of the uploaded document?",
    "history": []
  }'

# Check system health
curl "http://localhost:8000/api/health"
```

## 🎯 Features

### Chat Interface
- Real-time conversation with agents
- Source document references
- Agent selection and management
- Conversation history

### Document Upload
- Support for PDF, DOCX, TXT files
- Automatic text extraction and chunking
- Vector embedding generation
- Metadata tracking

### Memory Management
- View all stored memories
- Delete individual memories
- Clear entire memory store
- Search and filter capabilities

### Agent Management
- Default agent with RAG capabilities
- Create custom agents with system prompts
- Model override per agent
- Agent configuration management

## 🔒 Security & Privacy

- **Local Processing**: All data processed locally
- **No Cloud Dependencies**: No external API calls (except Ollama)
- **File Sanitization**: Uploaded files are validated and sanitized
- **CORS Protection**: Configured for specific origins

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags
   
   # Start Ollama if not running
   ollama serve
   ```

2. **Model Not Found**
   ```bash
   # List available models
   ollama list
   
   # Pull the required model
   ollama pull llama-3.2-70b
   ```

3. **Out of Memory**
   - Switch to a smaller model (8B or 7B)
   - Reduce `MAX_CONTEXT_TOKENS`
   - Close other applications

4. **ChromaDB Issues**
   ```bash
   # Clear ChromaDB data
   docker-compose down
   rm -rf ./data/chroma
   docker-compose up --build
   ```

### Logs

```bash
# View all service logs
make logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
```

## 📁 Project Structure

```
private-agent/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── api/                 # API endpoints
│   │   │   ├── chat.py
│   │   │   ├── upload.py
│   │   │   ├── agents.py
│   │   │   ├── memory.py
│   │   │   └── health.py
│   │   └── core/                # Core functionality
│   │       ├── ollama_client.py
│   │       ├── embeddings.py
│   │       ├── chroma_store.py
│   │       ├── agent_manager.py
│   │       └── schemas.py
│   ├── tests/                   # Unit tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Chat.tsx
│   │   │   ├── Upload.tsx
│   │   │   └── MemoryViewer.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── Makefile
├── .env.example
└── README.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) for local LLM hosting
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [LangChain](https://langchain.com/) for RAG orchestration
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://reactjs.org/) for the frontend framework