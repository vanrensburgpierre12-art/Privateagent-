"""Embedding generation using local models."""
import logging
from typing import List
import numpy as np
from ..config import settings

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generate embeddings using local models."""
    
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self._model = None
        self._tokenizer = None
        
    def _load_model(self):
        """Lazy load the embedding model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading embedding model: {self.model_name}")
                self._model = SentenceTransformer(self.model_name)
                logger.info("Embedding model loaded successfully")
            except ImportError:
                logger.error("sentence-transformers not installed. Install with: pip install sentence-transformers")
                raise Exception("Embedding model not available")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise Exception(f"Failed to load embedding model: {str(e)}")
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        if not texts:
            return []
            
        self._load_model()
        
        try:
            # Generate embeddings
            embeddings = self._model.encode(texts, convert_to_tensor=False)
            
            # Convert to list of lists
            if isinstance(embeddings, np.ndarray):
                embeddings = embeddings.tolist()
            
            logger.info(f"Generated embeddings for {len(texts)} texts, dimension: {len(embeddings[0]) if embeddings else 0}")
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise Exception(f"Embedding generation failed: {str(e)}")
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model."""
        self._load_model()
        # Generate a dummy embedding to get dimension
        dummy_embedding = self.get_embeddings(["dummy text"])
        return len(dummy_embedding[0]) if dummy_embedding else 0

# Global embedding generator instance
embedding_generator = EmbeddingGenerator()