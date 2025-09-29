"""Tests for ChromaDB ingestion and querying."""
import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from app.core.chroma_store import ChromaStore

class TestChromaStore:
    """Test ChromaDB store functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.store = ChromaStore()
        self.store.persist_directory = self.temp_dir
    
    def teardown_method(self):
        """Clean up test environment."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_ingest_text_file(self):
        """Test ingesting a text file."""
        # Create a temporary text file
        test_content = "This is a test document with some content for testing purposes."
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            temp_file = f.name
        
        try:
            with patch.object(self.store, 'collection') as mock_collection:
                mock_collection.add = MagicMock()
                
                with patch.object(self.store, 'embedding_generator') as mock_embeddings:
                    mock_embeddings.get_embeddings.return_value = [[0.1, 0.2, 0.3]]
                    
                    result = self.store.ingest_document(temp_file, {"test": "metadata"})
                    
                    assert result["chunks_created"] > 0
                    assert result["filename"] == os.path.basename(temp_file)
                    assert result["file_size"] > 0
                    
                    # Verify collection.add was called
                    mock_collection.add.assert_called_once()
        
        finally:
            os.unlink(temp_file)
    
    def test_query_documents(self):
        """Test querying documents."""
        with patch.object(self.store, 'collection') as mock_collection:
            mock_collection.query.return_value = {
                "documents": [["Test document content"]],
                "metadatas": [[{"filename": "test.txt", "chunk_id": "chunk_0"}]],
                "distances": [[0.1]]
            }
            
            with patch.object(self.store, 'embedding_generator') as mock_embeddings:
                mock_embeddings.get_embeddings.return_value = [[0.1, 0.2, 0.3]]
                
                results = self.store.query("test query", top_k=5)
                
                assert len(results) == 1
                assert results[0]["text"] == "Test document content"
                assert results[0]["metadata"]["filename"] == "test.txt"
                assert results[0]["distance"] == 0.1
    
    def test_list_memories(self):
        """Test listing memories."""
        with patch.object(self.store, 'collection') as mock_collection:
            mock_collection.get.return_value = {
                "documents": ["Memory content"],
                "metadatas": [{"filename": "memory.txt"}],
                "ids": ["memory_id_1"]
            }
            
            memories = self.store.list_memories()
            
            assert len(memories) == 1
            assert memories[0]["text"] == "Memory content"
            assert memories[0]["metadata"]["filename"] == "memory.txt"
            assert memories[0]["id"] == "memory_id_1"
    
    def test_delete_memory(self):
        """Test deleting a memory."""
        with patch.object(self.store, 'collection') as mock_collection:
            mock_collection.delete = MagicMock()
            
            result = self.store.delete_memory("memory_id_1")
            
            assert result is True
            mock_collection.delete.assert_called_once_with(ids=["memory_id_1"])
    
    def test_clear_store(self):
        """Test clearing the store."""
        with patch.object(self.store, 'client') as mock_client:
            mock_client.delete_collection = MagicMock()
            mock_client.create_collection = MagicMock()
            
            result = self.store.clear_store()
            
            assert result is True
            mock_client.delete_collection.assert_called_once()
            mock_client.create_collection.assert_called_once()
    
    def test_unsupported_file_format(self):
        """Test handling unsupported file formats."""
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            temp_file = f.name
        
        try:
            with pytest.raises(Exception, match="Unsupported file format"):
                self.store.ingest_document(temp_file, {})
        
        finally:
            os.unlink(temp_file)
    
    def test_empty_file(self):
        """Test handling empty files."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("")  # Empty file
            temp_file = f.name
        
        try:
            with pytest.raises(Exception, match="No text content found"):
                self.store.ingest_document(temp_file, {})
        
        finally:
            os.unlink(temp_file)