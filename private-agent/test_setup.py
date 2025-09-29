#!/usr/bin/env python3
"""
Test script to verify that sentence-transformers and other dependencies are working correctly.
"""

import sys
import os

# Add the backend to Python path
sys.path.insert(0, '/workspace/private-agent/backend')

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import sentence_transformers
        print("✓ sentence-transformers imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import sentence-transformers: {e}")
        return False
    
    try:
        from app.core.embeddings import EmbeddingGenerator
        print("✓ EmbeddingGenerator imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import EmbeddingGenerator: {e}")
        return False
    
    try:
        from app.main import app
        print("✓ FastAPI app imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import FastAPI app: {e}")
        return False
    
    return True

def test_embeddings():
    """Test that embeddings can be generated."""
    print("\nTesting embedding generation...")
    
    try:
        # Set environment variables
        os.environ['EMBEDDINGS_PROVIDER'] = 'sentence_transformers'
        os.environ['EMBEDDING_MODEL'] = 'sentence-transformers/all-MiniLM-L6-v2'
        
        from app.core.embeddings import EmbeddingGenerator
        
        generator = EmbeddingGenerator()
        embeddings = generator.get_embeddings(['This is a test sentence.'])
        
        if embeddings and len(embeddings) > 0 and len(embeddings[0]) > 0:
            print(f"✓ Generated embedding with dimension: {len(embeddings[0])}")
            return True
        else:
            print("✗ Failed to generate embeddings")
            return False
            
    except Exception as e:
        print(f"✗ Embedding generation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Private Agent Backend Setup Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test embeddings if imports are OK
    embeddings_ok = False
    if imports_ok:
        embeddings_ok = test_embeddings()
    
    print("\n" + "=" * 40)
    if imports_ok and embeddings_ok:
        print("✓ All tests passed! The backend is ready to run.")
        print("\nTo start the backend, run:")
        print("  ./run_backend.sh")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())