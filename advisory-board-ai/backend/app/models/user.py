from __future__ import annotations

from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    # Profile information
    date_of_birth: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    pan_number: Mapped[str | None] = mapped_column(String, nullable=True)  # For Indian users
    aadhaar_number: Mapped[str | None] = mapped_column(String, nullable=True)  # For Indian users
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String, nullable=True)
    state: Mapped[str | None] = mapped_column(String, nullable=True)
    pincode: Mapped[str | None] = mapped_column(String, nullable=True)

    # Financial profile
    annual_income: Mapped[int | None] = mapped_column(Integer, nullable=True)
    occupation: Mapped[str | None] = mapped_column(String, nullable=True)
    employer_name: Mapped[str | None] = mapped_column(String, nullable=True)