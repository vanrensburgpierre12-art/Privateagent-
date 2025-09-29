"""Tests for embedding generation."""
import pytest
from unittest.mock import patch, MagicMock
from app.core.embeddings import EmbeddingGenerator

class TestEmbeddings:
    """Test embedding generation functionality."""
    
    def test_get_embeddings_success(self):
        """Test successful embedding generation."""
        generator = EmbeddingGenerator()
        
        with patch('sentence_transformers.SentenceTransformer') as mock_model:
            mock_model_instance = MagicMock()
            mock_model_instance.encode.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
            mock_model.return_value = mock_model_instance
            
            generator._model = mock_model_instance
            
            texts = ["Hello world", "Test text"]
            embeddings = generator.get_embeddings(texts)
            
            assert len(embeddings) == 2
            assert len(embeddings[0]) == 3
            assert len(embeddings[1]) == 3
    
    def test_get_embeddings_empty_input(self):
        """Test embedding generation with empty input."""
        generator = EmbeddingGenerator()
        
        embeddings = generator.get_embeddings([])
        assert embeddings == []
    
    def test_get_embedding_dimension(self):
        """Test getting embedding dimension."""
        generator = EmbeddingGenerator()
        
        with patch.object(generator, 'get_embeddings') as mock_get_embeddings:
            mock_get_embeddings.return_value = [[0.1, 0.2, 0.3]]
            
            dimension = generator.get_embedding_dimension()
            assert dimension == 3
    
    def test_model_loading_error(self):
        """Test error handling when model loading fails."""
        generator = EmbeddingGenerator()
        
        with patch('sentence_transformers.SentenceTransformer') as mock_model:
            mock_model.side_effect = ImportError("Module not found")
            
            with pytest.raises(Exception, match="Embedding model not available"):
                generator.get_embeddings(["test"])
    
    def test_embedding_generation_error(self):
        """Test error handling during embedding generation."""
        generator = EmbeddingGenerator()
        
        with patch('sentence_transformers.SentenceTransformer') as mock_model:
            mock_model_instance = MagicMock()
            mock_model_instance.encode.side_effect = Exception("Generation failed")
            mock_model.return_value = mock_model_instance
            
            generator._model = mock_model_instance
            
            with pytest.raises(Exception, match="Embedding generation failed"):
                generator.get_embeddings(["test"])