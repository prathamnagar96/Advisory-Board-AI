from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
import json
from dotenv import load_dotenv

from app.core.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.reminder import Reminder
from app.utils.security import get_password_hash
from app.api.reminders import TAX_REMINDERS

load_dotenv()

# Import routers
from app.api import auth, tax, documents, reminders, dashboard

# Security
security = HTTPBearer()


def init_db():
    """Create tables and seed a demo user/reminders for the prototype."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        demo_user = db.query(User).filter(User.username == "demo").first()
        if not demo_user:
            demo_user = User(
                email="demo@demo.com",
                username="demo",
                hashed_password=get_password_hash("demo123"),
                full_name="Demo User",
                is_verified=True,
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)

        # Seed reminders if empty
        if db.query(Reminder).count() == 0:
            for reminder in TAX_REMINDERS:
                db.add(
                    Reminder(
                        title=reminder["title"],
                        description=reminder.get("description"),
                        reminder_type=reminder["reminder_type"],
                        due_date=reminder["due_date"],
                        is_recurring=reminder.get("is_recurring", False),
                        recurrence_pattern=reminder.get("recurrence_pattern"),
                        priority=reminder.get("priority", "medium"),
                        metadata_json=json.dumps(reminder.get("metadata", {})),
                        user_id=demo_user.id,
                    )
                )
            db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Advisory Board AI Backend starting up...")
    init_db()
    yield
    # Shutdown
    print("👋 Advisory Board AI Backend shutting down...")

app = FastAPI(
    title="Advisory Board AI",
    description="Democratizing professional advisory services through AI",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tax.router, prefix="/api/tax", tags=["Tax Advisory"])
app.include_router(documents.router, prefix="/api/documents", tags=["Document Processing"])
app.include_router(reminders.router, prefix="/api/reminders", tags=["Reminders & Timeline"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Advisory Board AI - Democratizing Professional Expertise",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "advisory-board-ai"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )