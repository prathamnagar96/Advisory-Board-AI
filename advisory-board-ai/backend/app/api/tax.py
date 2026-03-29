from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from datetime import datetime
import logging

from app.core.rag_system import tax_rag
from app.core.database import get_db
from app.models.user import User
from app.models.tax_query import TaxQuery
from app.models.document import Document
from app.utils.security import get_current_user, verify_token

router = APIRouter()
security = HTTPBearer()
logger = logging.getLogger(__name__)

# Pydantic models
class TaxQueryRequest(BaseModel):
    query: str

class TaxQueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    risk_level: str
    confidence: str
    timestamp: str

class DocumentUploadResponse(BaseModel):
    message: str
    document_id: str
    filename: str
    upload_timestamp: str

@router.post("/query", response_model=TaxQueryResponse)
async def ask_tax_question(
    request: TaxQueryRequest,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Ask a tax-related question and get AI-powered advice with citations.
    """
    # Generate response using RAG system with safe fallback
    try:
        response = tax_rag.generate_response(request.query)
    except Exception as exc:
        logger.warning("RAG generation failed, returning safe fallback: %s", exc)
        response = {
            "answer": "We're operating in demo mode right now. Based on common guidance, consider using Section 80C investments (ELSS/PPF) and health insurance under 80D. For personalised advice, consult a CA.",
            "sources": [],
            "risk_level": "LOW",
            "confidence": "MEDIUM",
        }

    tax_query = TaxQuery(
        user_id=current_user.id,
        query=request.query,
        response=response.get("answer"),
        risk_level=response.get("risk_level"),
        confidence=response.get("confidence", "MEDIUM"),
        sources_used=None,
    )
    db.add(tax_query)
    db.commit()

    return TaxQueryResponse(
        answer=response['answer'],
        sources=response['sources'],
        risk_level=response['risk_level'],
        confidence=response['confidence'],
        timestamp=datetime.utcnow().isoformat()
    )

@router.post("/upload-document", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Upload tax-related documents (Form 16, investment proofs, etc.) for processing.
    """
    # Validate file type
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx'}
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
    unique_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, unique_filename)

    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_size = os.path.getsize(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not upload file: {str(e)}"
        )

    # Process document with RAG system (if it's a tax document)
    if file_extension == '.pdf':
        try:
            # Load and add to RAG system for future queries
            documents = tax_rag.load_tax_act(file_path)
            tax_rag.add_documents(documents)
            logger.info(f"Processed and added {len(documents)} chunks from {file.filename} to RAG system")
        except Exception as e:
            logger.warning(f"Could not process document for RAG: {e}")

    document_record = Document(
        user_id=current_user.id,
        filename=file.filename,
        stored_filename=unique_filename,
        file_path=file_path,
        file_type=file_extension,
        file_size=file_size,
        upload_timestamp=datetime.utcnow(),
        processed=True,
    )
    db.add(document_record)
    db.commit()
    db.refresh(document_record)

    return DocumentUploadResponse(
        message="Document uploaded successfully",
        document_id=str(document_record.id),
        filename=file.filename,
        upload_timestamp=datetime.utcnow().isoformat()
    )

@router.get("/tax-sections")
async def get_tax_sections():
    """
    Get available tax sections for reference.
    """
    # In a real implementation, this would return structured tax sections
    return {
        "sections": [
            {"code": "80C", "description": "Deductions for investments, PPF, EPF, life insurance, etc."},
            {"code": "80D", "description": "Deduction for health insurance premiums"},
            {"code": "24", "description": "Deduction for home loan interest"},
            {"code": "10(14)", "description": "Allowances like HRA, LTA, etc."},
            {"code": "80G", "description": "Donations to charitable institutions"},
            {"code": "80E", "description": "Interest on education loan"},
            {"code": "80TTA", "description": "Interest on savings account"},
            {"code": "80GG", "description": "Rent paid when HRA not received"}
        ]
    }

@router.get("/deduction-calculator")
async def calculate_deductions(
    investments_80c: float = 0,
    health_insurance: float = 0,
    home_loan_interest: float = 0,
    donations: float = 0,
    education_loan_interest: float = 0,
    savings_interest: float = 0,
    rent_paid: float = 0,
    hra_received: float = 0,
    basic_salary: float = 0,
    metro_city: bool = False
):
    """
    Simple tax deduction calculator for common sections.
    """
    # Section 80C deduction (max ₹1.5 lakh)
    deduction_80c = min(investments_80c, 150000)

    # Section 80D deduction
    # Self & family: ₹25,000, Parents: ₹25,000 (₹50,000 if parents are senior citizens)
    deduction_80d = min(health_insurance, 25000)  # Simplified

    # Section 24(b) home loan interest
    deduction_24 = min(home_loan_interest, 200000)  # Self-occupied property

    # Section 80G donations (assuming 50% deductible)
    deduction_80g = donations * 0.5

    # Section 80E education loan interest
    deduction_80e = education_loan_interest  # No limit

    # Section 80TTA savings interest
    deduction_80tta = min(savings_interest, 10000)

    # Section 80GG rent deduction
    # Least of: rent paid - 10% of basic salary, ₹5000 per month, 25% of basic salary
    if basic_salary > 0:
        rent_deduction_options = [
            rent_paid - (0.1 * basic_salary),
            5000 * 12,  # ₹5000 per month
            0.25 * basic_salary
        ]
        deduction_80gg = max(0, min(rent_deduction_options))
    else:
        deduction_80gg = 0

    total_deductions = (
        deduction_80c + deduction_80d + deduction_24 +
        deduction_80g + deduction_80e + deduction_80tta + deduction_80gg
    )

    return {
        "deductions": {
            "section_80c": deduction_80c,
            "section_80d": deduction_80d,
            "section_24": deduction_24,
            "section_80g": deduction_80g,
            "section_80e": deduction_80e,
            "section_80tta": deduction_80tta,
            "section_80gg": deduction_80gg
        },
        "total_deductions": total_deductions,
        "assessment_year": "2025-26",
        "note": "This is a simplified calculator. Actual tax liability depends on income slab, other income, and various factors."
    }