"""Embedding generation using local or Ollama-provided models."""
import logging
from typing import List
import numpy as np
import httpx
from ..config import settings

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generate embeddings using either sentence-transformers or Ollama embeddings API."""

    def __init__(self):
        self.provider = settings.EMBEDDINGS_PROVIDER.lower()
        self.model_name = (
            settings.OLLAMA_EMBEDDING_MODEL
            if self.provider == "ollama"
            else settings.EMBEDDING_MODEL
        )
        self._model = None

    def _load_sentence_transformers(self) -> None:
        """Lazy-load the sentence-transformers model."""
        if self._model is not None:
            return
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

    def _ollama_embed_one(self, client: httpx.Client, text: str) -> List[float]:
        """Request a single embedding vector from Ollama (synchronous)."""
        try:
            response = client.post(
                f"{settings.OLLAMA_URL}/api/embeddings",
                json={"model": self.model_name, "input": text},
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            vector = data.get("embedding") or (data.get("data") or [{}])[0].get("embedding")
            if not vector:
                raise Exception("No embedding returned from Ollama")
            return vector
        except Exception as e:
            logger.error(f"Ollama embedding failed: {e}")
            raise Exception(f"Embedding generation failed: {str(e)}")

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        if not texts:
            return []

        if self.provider == "ollama":
            results: List[List[float]] = []
            with httpx.Client() as client:
                for text in texts:
                    vec = self._ollama_embed_one(client, text)
                    results.append(vec)
            embeddings = results
            logger.info(
                f"Generated embeddings via Ollama for {len(texts)} texts, dimension: {len(embeddings[0]) if embeddings else 0}"
            )
            return embeddings

        # Fallback to sentence-transformers provider
        self._load_sentence_transformers()
        try:
            embeddings = self._model.encode(texts, convert_to_tensor=False)
            if isinstance(embeddings, np.ndarray):
                embeddings = embeddings.tolist()
            logger.info(
                f"Generated embeddings for {len(texts)} texts, dimension: {len(embeddings[0]) if embeddings else 0}"
            )
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise Exception(f"Embedding generation failed: {str(e)}")

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by this model."""
        dummy = self.get_embeddings(["dummy text"])
        return len(dummy[0]) if dummy else 0

# Global embedding generator instance
embedding_generator = EmbeddingGenerator()