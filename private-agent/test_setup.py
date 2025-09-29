#!/usr/bin/env python3
"""Test script to verify the Private Agent Platform setup."""

import os
import sys
import asyncio
import requests
from pathlib import Path

def test_ollama_connection():
    """Test Ollama connection."""
    print("Testing Ollama connection...")
    try:
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        response = requests.get(f"{ollama_url}/api/tags", timeout=10)
        if response.status_code == 200:
            print("✅ Ollama is running and accessible")
            return True
        else:
            print("❌ Ollama returned status code:", response.status_code)
            return False
    except Exception as e:
        print("❌ Ollama connection failed:", str(e))
        return False

def test_backend_connection():
    """Test backend API connection."""
    print("Testing backend connection...")
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is running")
            print(f"   Ollama connected: {data.get('ollama_connected', False)}")
            print(f"   ChromaDB connected: {data.get('chroma_connected', False)}")
            return True
        else:
            print("❌ Backend returned status code:", response.status_code)
            return False
    except Exception as e:
        print("❌ Backend connection failed:", str(e))
        return False

def test_frontend_connection():
    """Test frontend connection."""
    print("Testing frontend connection...")
    try:
        response = requests.get("http://localhost:5173", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is running")
            return True
        else:
            print("❌ Frontend returned status code:", response.status_code)
            return False
    except Exception as e:
        print("❌ Frontend connection failed:", str(e))
        return False

def test_file_structure():
    """Test if all required files exist."""
    print("Testing file structure...")
    required_files = [
        "backend/app/main.py",
        "backend/app/config.py",
        "backend/requirements.txt",
        "backend/Dockerfile",
        "frontend/src/App.tsx",
        "frontend/package.json",
        "frontend/Dockerfile",
        "docker-compose.yml",
        ".env.example",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Run all tests."""
    print("🔍 Private Agent Platform Setup Test")
    print("=" * 50)
    
    tests = [
        test_file_structure,
        test_ollama_connection,
        test_backend_connection,
        test_frontend_connection
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
        print()
    
    print("=" * 50)
    print("📊 Test Results:")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 All tests passed! The platform is ready to use.")
        print("\nNext steps:")
        print("1. Open http://localhost:5173 in your browser")
        print("2. Upload a document using the Upload tab")
        print("3. Start chatting with your private agent!")
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("\nTroubleshooting:")
        print("1. Make sure Docker is running")
        print("2. Run 'docker-compose up --build' to start services")
        print("3. Install Ollama and pull a model: ollama pull llama-3.2-8b")
        print("4. Check the logs: docker-compose logs")

if __name__ == "__main__":
    main()