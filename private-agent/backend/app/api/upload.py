"""Document upload API endpoints."""
import os
import tempfile
import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from ..core.schemas import UploadResponse
from ..core.chroma_store import chroma_store

logger = logging.getLogger(__name__)
router = APIRouter()

ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.docx', '.doc'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and ingest a document into the vector store."""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file_ext} not supported. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Ingest document
            metadata = {
                "uploaded_at": str(os.path.getctime(temp_file_path)),
                "original_filename": file.filename,
                "file_size": len(content)
            }
            
            result = chroma_store.ingest_document(temp_file_path, metadata)
            
            return UploadResponse(
                message=f"Successfully uploaded and processed {file.filename}",
                chunks_created=result["chunks_created"],
                filename=result["filename"],
                file_size=result["file_size"]
            )
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_file_path}: {e}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.post("/upload-text")
async def upload_text(text: str, filename: str = "text_input.txt"):
    """Upload raw text content."""
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text content provided")
        
        # Save text to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as temp_file:
            temp_file.write(text)
            temp_file_path = temp_file.name
        
        try:
            metadata = {
                "uploaded_at": str(os.path.getctime(temp_file_path)),
                "original_filename": filename,
                "file_size": len(text),
                "type": "text_input"
            }
            
            result = chroma_store.ingest_document(temp_file_path, metadata)
            
            return UploadResponse(
                message=f"Successfully processed text input",
                chunks_created=result["chunks_created"],
                filename=filename,
                file_size=result["file_size"]
            )
            
        finally:
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {temp_file_path}: {e}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Text upload failed: {str(e)}")