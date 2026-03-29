from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    reminder_type = Column(String, nullable=False)  # tax_filing, investment, compliance, custom
    due_date = Column(DateTime(timezone=True), nullable=False)
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String, nullable=True)  # daily, weekly, monthly, yearly
    priority = Column(String, default="medium")  # low, medium, high
    metadata_json = Column("metadata", Text, nullable=True)  # JSON string stored as text
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, nullable=True)  # For future user association