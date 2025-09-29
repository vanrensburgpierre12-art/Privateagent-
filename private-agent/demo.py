#!/usr/bin/env python3
"""Demo script for the Private Agent Platform API."""

import requests
import json
import time

API_BASE = "http://localhost:8000/api"

def upload_sample_document():
    """Upload the sample document."""
    print("📄 Uploading sample document...")
    
    try:
        with open("sample_document.txt", "rb") as f:
            files = {"file": ("sample_document.txt", f, "text/plain")}
            response = requests.post(f"{API_BASE}/upload", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Document uploaded successfully!")
            print(f"   Chunks created: {data['chunks_created']}")
            print(f"   File size: {data['file_size']} bytes")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def test_chat():
    """Test chat functionality."""
    print("\n💬 Testing chat functionality...")
    
    test_questions = [
        "What is the Private Agent Platform?",
        "What are the key features mentioned in the documentation?",
        "What is the technical stack used?",
        "What are the security and privacy features?"
    ]
    
    for question in test_questions:
        print(f"\n🤔 Question: {question}")
        
        try:
            payload = {
                "agent_id": "default",
                "message": question,
                "history": []
            }
            
            response = requests.post(f"{API_BASE}/chat", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"🤖 Answer: {data['answer']}")
                print(f"📚 Model: {data['model']}")
                
                if data.get('sources'):
                    print("📖 Sources:")
                    for source in data['sources']:
                        print(f"   - {source['filename']} (chunk {source['chunk_id']})")
            else:
                print(f"❌ Chat failed: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Chat error: {e}")
        
        time.sleep(1)  # Small delay between requests

def test_memory():
    """Test memory functionality."""
    print("\n🧠 Testing memory functionality...")
    
    try:
        response = requests.get(f"{API_BASE}/memory")
        
        if response.status_code == 200:
            memories = response.json()
            print(f"✅ Found {len(memories)} memories in the store")
            
            if memories:
                print("📋 Sample memories:")
                for i, memory in enumerate(memories[:3]):  # Show first 3
                    print(f"   {i+1}. {memory['text'][:100]}...")
                    print(f"      File: {memory.get('filename', 'N/A')}")
        else:
            print(f"❌ Memory retrieval failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Memory error: {e}")

def test_agents():
    """Test agent functionality."""
    print("\n🤖 Testing agent functionality...")
    
    try:
        response = requests.get(f"{API_BASE}/agents")
        
        if response.status_code == 200:
            agents = response.json()
            print(f"✅ Found {len(agents)} agents")
            
            for agent in agents:
                print(f"   - {agent['name']} (ID: {agent['agent_id']})")
        else:
            print(f"❌ Agent retrieval failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Agent error: {e}")

def test_health():
    """Test health endpoint."""
    print("\n🏥 Testing health endpoint...")
    
    try:
        response = requests.get(f"{API_BASE}/health")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ System status: {data['status']}")
            print(f"   Ollama connected: {data['ollama_connected']}")
            print(f"   ChromaDB connected: {data['chroma_connected']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Health check error: {e}")

def main():
    """Run the demo."""
    print("🚀 Private Agent Platform Demo")
    print("=" * 50)
    
    # Test health first
    test_health()
    
    # Upload document
    if upload_sample_document():
        # Test other functionality
        test_agents()
        test_memory()
        test_chat()
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("\nYou can now:")
    print("1. Open http://localhost:5173 to use the web interface")
    print("2. Try uploading your own documents")
    print("3. Create custom agents with different system prompts")
    print("4. Explore the memory store and manage your data")

if __name__ == "__main__":
    main()