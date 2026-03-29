from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from datetime import datetime
import hashlib

from app.core.database import get_db
from app.models.document import Document
from app.models.user import User
from app.utils.security import get_current_user
from app.core.rag_system import tax_rag

router = APIRouter()
security = HTTPBearer()

# Pydantic models
class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    upload_timestamp: str
    processed: bool
    size: int

class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]
    total: int

class DocumentProcessRequest(BaseModel):
    document_id: str
    extract_entities: bool = True
    summarize: bool = False

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Upload a document for processing and storage.
    """
    # Validate file type
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx', '.txt', '.csv'}
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_extension} not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )

    # Create uploads directory if it doesn't exist
    upload_dir = "./uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_hash = hashlib.md5(file.filename.encode()).hexdigest()[:8]
    unique_filename = f"{timestamp}_{file_hash}_{file.filename}"
    file_path = os.path.join(upload_dir, unique_filename)

    # Save file
    try:
        file_content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        file_size = len(file_content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not upload file: {str(e)}"
        )

    # Create document record
    document_record = Document(
        user_id=current_user.id,
        filename=file.filename,
        stored_filename=unique_filename,
        file_path=file_path,
        file_type=file_extension,
        file_size=file_size,
        upload_timestamp=datetime.utcnow(),
        processed=False
    )

    db.add(document_record)
    db.commit()
    db.refresh(document_record)

    # Process document if it's a PDF (extract text for RAG)
    if file_extension == '.pdf':
        try:
            # Extract text and add to RAG system for context
            text = ""
            try:
                import pdfplumber
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
            except:
                import PyPDF2
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"

            if text.strip():
                # Add extracted text as a document for RAG context
                from langchain.schema import Document as LangchainDocument
                langchain_doc = LangchainDocument(
                    page_content=text,
                    metadata={
                        "source": f"uploaded_document_{document_record.id}",
                        "filename": file.filename,
                        "upload_timestamp": datetime.utcnow().isoformat()
                    }
                )
                tax_rag.add_documents([langchain_doc])

                # Mark as processed
                document_record.processed = True
                document_record.processed_timestamp = datetime.utcnow()
                db.commit()

        except Exception as e:
            # Log error but don't fail the upload
            print(f"Could not process document for RAG: {e}")

    return DocumentResponse(
        id=str(document_record.id),
        filename=document_record.filename,
        file_type=document_record.file_type,
        upload_timestamp=document_record.upload_timestamp.isoformat(),
        processed=document_record.processed,
        size=document_record.file_size
    )

@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    List all uploaded documents.
    """
    documents = db.query(Document).filter(Document.user_id == current_user.id).offset(skip).limit(limit).all()
    total = db.query(Document).filter(Document.user_id == current_user.id).count()

    document_responses = [
        DocumentResponse(
            id=str(doc.id),
            filename=doc.filename,
            file_type=doc.file_type,
            upload_timestamp=doc.upload_timestamp.isoformat(),
            processed=doc.processed,
            size=doc.file_size
        )
        for doc in documents
    ]

    return DocumentListResponse(
        documents=document_responses,
        total=total
    )

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get a specific document by ID.
    """
    document = db.query(Document).filter(
        Document.id == document_id, Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return DocumentResponse(
        id=str(document.id),
        filename=document.filename,
        file_type=document.file_type,
        upload_timestamp=document.upload_timestamp.isoformat(),
        processed=document.processed,
        size=document.file_size
    )

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Delete a document.
    """
    document = db.query(Document).filter(
        Document.id == document_id, Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # Delete file from filesystem
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        print(f"Could not delete file: {e}")

    # Delete from database
    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}

@router.post("/process/{document_id}")
async def process_document(
    document_id: int,
    request: DocumentProcessRequest,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Process a document for entity extraction, summarization, etc.
    """
    document = db.query(Document).filter(
        Document.id == document_id, Document.user_id == current_user.id
    ).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    # In a real implementation, this would use NLP models for entity extraction
    # For now, we'll return a mock response

    processed_data = {
        "document_id": str(document.id),
        "filename": document.filename,
        "processing_timestamp": datetime.utcnow().isoformat(),
        "entities": {
            "dates": ["2024-03-15", "2024-04-30"],
            "amounts": [50000, 75000, 120000],
            "names": ["ABC Company", "XYZ Bank"],
            "tax_related": ["Form 16", "Section 80C", "TDS"]
        } if request.extract_entities else {},
        "summary": "This document appears to be a Form 16 showing salary income and TDS deductions for the financial year 2023-24." if request.summarize else "",
        "suggested_actions": [
            "Verify TDS deductions match Form 26AS",
            "Check if all Section 80C investments are declared",
            "Confirm employer details are correct"
        ]
    }

    # Update document as processed
    document.processed = True
    document.processed_timestamp = datetime.utcnow()
    db.commit()

    return processed_data