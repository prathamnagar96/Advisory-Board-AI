from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class TaxQuery(Base):
    __tablename__ = "tax_queries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    risk_level = Column(String(10), nullable=True)  # LOW, MEDIUM, HIGH
    confidence = Column(String(10), nullable=True)  # LOW, MEDIUM, HIGH
    sources_used = Column(String, nullable=True)  # JSON string of sources
    created_at = Column(DateTime(timezone=True), server_default=func.now())