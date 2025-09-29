"""ChromaDB vector store for document storage and retrieval."""
import os
import uuid
import logging
from typing import List, Dict, Any, Optional, Tuple
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import CharacterTextSplitter
from ..config import settings
from .embeddings import embedding_generator

# Disable ChromaDB telemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"

logger = logging.getLogger(__name__)

class ChromaStore:
    """ChromaDB vector store manager."""
    
    def __init__(self):
        self.persist_directory = settings.CHROMA_PERSIST_DIR
        self.collection_name = "private_agent"
        
        # Ensure persist directory exists
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
                is_persistent=True
            )
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except Exception:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Private agent document store"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
        
        # Initialize text splitter
        self.text_splitter = CharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separator="\n"
        )
    
    def ingest_document(self, file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest a document into the vector store."""
        try:
            # Extract text from file
            text = self._extract_text_from_file(file_path)
            if not text.strip():
                raise Exception("No text content found in file")
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            logger.info(f"Split document into {len(chunks)} chunks")
            
            # Generate embeddings
            embeddings = embedding_generator.get_embeddings(chunks)
            
            # Prepare data for ChromaDB
            ids = [str(uuid.uuid4()) for _ in chunks]
            metadatas = []
            
            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    "filename": os.path.basename(file_path),
                    "chunk_id": f"chunk_{i}",
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "file_path": file_path,
                    **metadata
                }
                metadatas.append(chunk_metadata)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas
            )
            
            logger.info(f"Successfully ingested document: {file_path}")
            return {
                "chunks_created": len(chunks),
                "filename": os.path.basename(file_path),
                "file_size": len(text)
            }
            
        except Exception as e:
            logger.error(f"Failed to ingest document {file_path}: {e}")
            raise Exception(f"Document ingestion failed: {str(e)}")
    
    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Query the vector store for relevant documents."""
        try:
            # Generate query embedding
            query_embedding = embedding_generator.get_embeddings([query_text])[0]
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "text": doc,
                        "metadata": results["metadatas"][0][i],
                        "distance": results["distances"][0][i] if results["distances"] else 0.0
                    })
            
            logger.info(f"Query returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise Exception(f"Query failed: {str(e)}")
    
    def list_memories(self) -> List[Dict[str, Any]]:
        """List all memories in the store."""
        try:
            results = self.collection.get(include=["documents", "metadatas"])
            
            memories = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"]):
                    memories.append({
                        "id": results["ids"][i],
                        "text": doc,
                        "metadata": results["metadatas"][i]
                    })
            
            logger.info(f"Retrieved {len(memories)} memories")
            return memories
            
        except Exception as e:
            logger.error(f"Failed to list memories: {e}")
            raise Exception(f"Failed to list memories: {str(e)}")
    
    def delete_memory(self, memory_id: str) -> bool:
        """Delete a specific memory by ID."""
        try:
            self.collection.delete(ids=[memory_id])
            logger.info(f"Deleted memory: {memory_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete memory {memory_id}: {e}")
            return False
    
    def clear_store(self) -> bool:
        """Clear all memories from the store."""
        try:
            # Delete the collection and recreate it
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Private agent document store"}
            )
            logger.info("Cleared all memories from store")
            return True
        except Exception as e:
            logger.error(f"Failed to clear store: {e}")
            return False
    
    def _extract_text_from_file(self, file_path: str) -> str:
        """Extract text from various file formats."""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_ext == '.pdf':
            try:
                import pypdf
                with open(file_path, 'rb') as f:
                    reader = pypdf.PdfReader(f)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                raise Exception("pypdf not installed. Install with: pip install pypdf")
        
        elif file_ext in ['.docx', '.doc']:
            try:
                from docx import Document
                doc = Document(file_path)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text
            except ImportError:
                raise Exception("python-docx not installed. Install with: pip install python-docx")
        
        else:
            raise Exception(f"Unsupported file format: {file_ext}")

# Global ChromaDB store instance
chroma_store = ChromaStore()