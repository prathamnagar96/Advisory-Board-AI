from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)  # Original filename
    stored_filename = Column(String, nullable=False)  # Actual filename on disk
    file_path = Column(String, nullable=False)  # Full path to file
    file_type = Column(String, nullable=False)  # Extension (pdf, jpg, etc.)
    file_size = Column(Integer, nullable=False)  # Size in bytes
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    processed_timestamp = Column(DateTime(timezone=True), nullable=True)
    processed = Column(Boolean, default=False)  # Whether text has been extracted
    user_id = Column(Integer, nullable=True)  # For future user association