from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import uuid
import json

from app.core.database import get_db
from app.models.reminder import Reminder

router = APIRouter()
security = HTTPBearer()

# Pydantic models
class ReminderBase(BaseModel):
    title: str
    description: Optional[str] = None
    reminder_type: str  # tax_filing, investment, compliance, custom
    due_date: datetime
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None  # daily, weekly, monthly, yearly
    priority: str = "medium"  # low, medium, high
    metadata: Optional[dict] = None

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    reminder_type: Optional[str] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    priority: Optional[str] = None
    is_completed: Optional[bool] = None
    metadata: Optional[dict] = None

class ReminderResponse(ReminderBase):
    id: str
    is_completed: bool
    created_at: datetime
    completed_at: Optional[datetime] = None

class ReminderListResponse(BaseModel):
    reminders: List[ReminderResponse]
    total: int
    upcoming_count: int

@router.post("/", response_model=ReminderResponse)
async def create_reminder(
    reminder: ReminderCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
):
    """
    Create a new reminder.
    """
    # In a real app, you would get user ID from token
    # For now, we'll create a reminder without user association for simplicity

    db_reminder = Reminder(
        id=str(uuid.uuid4()),
        title=reminder.title,
        description=reminder.description,
        reminder_type=reminder.reminder_type,
        due_date=reminder.due_date,
        is_recurring=reminder.is_recurring,
        recurrence_pattern=reminder.recurrence_pattern,
        priority=reminder.priority,
        metadata_json=json.dumps(reminder.metadata or {}),
        is_completed=False
    )

    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)

    return ReminderResponse(
        id=db_reminder.id,
        title=db_reminder.title,
        description=db_reminder.description,
        reminder_type=db_reminder.reminder_type,
        due_date=db_reminder.due_date,
        is_recurring=db_reminder.is_recurring,
        recurrence_pattern=db_reminder.recurrence_pattern,
        priority=db_reminder.priority,
        metadata=json.loads(db_reminder.metadata_json) if isinstance(db_reminder.metadata_json, str) else db_reminder.metadata_json,
        is_completed=db_reminder.is_completed,
        created_at=db_reminder.created_at,
        completed_at=db_reminder.completed_at
    )

@router.get("/", response_model=ReminderListResponse)
async def list_reminders(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    upcoming_only: bool = False,
    completed: Optional[bool] = None
):
    """
    List reminders with filtering options.
    """
    query = db.query(Reminder)

    if completed is not None:
        query = query.filter(Reminder.is_completed == completed)

    if upcoming_only:
        query = query.filter(Reminder.due_date >= datetime.utcnow())

    reminders = query.offset(skip).limit(limit).all()
    total = query.count()
    upcoming_count = db.query(Reminder).filter(
        Reminder.due_date >= datetime.utcnow(),
        Reminder.is_completed == False
    ).count()

    reminder_responses = [
        ReminderResponse(
            id=r.id,
            title=r.title,
            description=r.description,
            reminder_type=r.reminder_type,
            due_date=r.due_date,
            is_recurring=r.is_recurring,
            recurrence_pattern=r.recurrence_pattern,
            priority=r.priority,
            metadata=json.loads(r.metadata_json) if isinstance(r.metadata_json, str) else r.metadata_json,
            is_completed=r.is_completed,
            created_at=r.created_at,
            completed_at=r.completed_at
        )
        for r in reminders
    ]

    return ReminderListResponse(
        reminders=reminder_responses,
        total=total,
        upcoming_count=upcoming_count
    )

@router.get("/{reminder_id}", response_model=ReminderResponse)
async def get_reminder(
    reminder_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
):
    """
    Get a specific reminder by ID.
    """
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    return ReminderResponse(
        id=reminder.id,
        title=reminder.title,
        description=reminder.description,
        reminder_type=reminder.reminder_type,
        due_date=reminder.due_date,
        is_recurring=reminder.is_recurring,
        recurrence_pattern=reminder.recurrence_pattern,
        priority=reminder.priority,
        metadata=json.loads(reminder.metadata_json) if isinstance(reminder.metadata_json, str) else reminder.metadata_json,
        is_completed=reminder.is_completed,
        created_at=reminder.created_at,
        completed_at=reminder.completed_at
    )

@router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: str,
    reminder_update: ReminderUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
):
    """
    Update a reminder.
    """
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    update_data = reminder_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "metadata" and value is not None:
            setattr(reminder, "metadata_json", json.dumps(value))
        elif field != "metadata":
            setattr(reminder, field, value)

    if reminder_update.is_completed and not reminder.is_completed:
        reminder.completed_at = datetime.utcnow()
    elif not reminder_update.is_completed and reminder.is_completed:
        reminder.completed_at = None

    db.commit()
    db.refresh(reminder)

    return ReminderResponse(
        id=reminder.id,
        title=reminder.title,
        description=reminder.description,
        reminder_type=reminder.reminder_type,
        due_date=reminder.due_date,
        is_recurring=reminder.is_recurring,
        recurrence_pattern=reminder.recurrence_pattern,
        priority=reminder.priority,
        metadata=json.loads(reminder.metadata_json) if isinstance(reminder.metadata_json, str) else reminder.metadata_json,
        is_completed=reminder.is_completed,
        created_at=reminder.created_at,
        completed_at=reminder.completed_at
    )

@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
):
    """
    Delete a reminder.
    """
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    db.delete(reminder)
    db.commit()

    return {"message": "Reminder deleted successfully"}

@router.post("/{reminder_id}/complete")
async def complete_reminder(
    reminder_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
):
    """
    Mark a reminder as completed.
    """
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )

    reminder.is_completed = True
    reminder.completed_at = datetime.utcnow()
    db.commit()

    return {"message": "Reminder marked as completed"}

# Predefined tax reminders for initialization
TAX_REMINDERS = [
    {
        "title": "File Income Tax Return",
        "description": "File your annual income tax return for the financial year",
        "reminder_type": "tax_filing",
        "due_date": datetime(2024, 7, 31),  # July 31st typically
        "is_recurring": True,
        "recurrence_pattern": "yearly",
        "priority": "high",
        "metadata": {"assessment_year": "2024-25"}
    },
    {
        "title": "Pay Advance Tax Installment",
        "description": "Pay your advance tax installment to avoid interest penalties",
        "reminder_type": "tax_payment",
        "due_date": datetime(2024, 6, 15),  # June 15th
        "is_recurring": True,
        "recurrence_pattern": "yearly",
        "priority": "medium",
        "metadata": {"installment": 1}
    },
    {
        "title": "Review Form 26AS",
        "description": "Check your tax credit statement for TDS details",
        "reminder_type": "compliance",
        "due_date": datetime(2024, 4, 30),  # April 30th
        "is_recurring": True,
        "recurrence_pattern": "yearly",
        "priority": "medium",
        "metadata": {"form": "26AS"}
    }
]