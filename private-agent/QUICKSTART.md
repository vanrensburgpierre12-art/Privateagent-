# Quick Start Guide

Get the Private Agent Platform running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Ollama installed locally

## Step 1: Install Ollama

```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Or visit https://ollama.com/docs for other platforms
```

## Step 2: Pull a Model

```bash
# For powerful hardware (GPU recommended)
ollama pull llama-3.2-70b

# For moderate hardware
ollama pull llama-3.2-13b

# For limited hardware
ollama pull llama-3.2-8b
```

## Step 3: Start Ollama

```bash
ollama serve
```

## Step 4: Configure Environment

```bash
cp .env.example .env
# Edit .env to set your preferred model
```

## Step 5: Start the Platform

```bash
make build
make up
```

## Step 6: Test Everything

```bash
python test_setup.py
```

## Step 7: Try the Demo

```bash
python demo.py
```

## Step 8: Open the Web Interface

Visit http://localhost:5173 in your browser!

## Troubleshooting

**Ollama not found?**
```bash
curl http://localhost:11434/api/tags
```

**Out of memory?**
- Switch to a smaller model in `.env`
- Reduce `MAX_CONTEXT_TOKENS`

**Services not starting?**
```bash
docker-compose logs
```

## Next Steps

1. Upload documents using the Upload tab
2. Start chatting with your private agent
3. Explore the memory store
4. Create custom agents

Happy chatting! 🚀