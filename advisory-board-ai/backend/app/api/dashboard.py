from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random

from app.core.database import get_db
from app.models.user import User
from app.models.tax_query import TaxQuery
from app.models.document import Document
from app.models.reminder import Reminder
from app.utils.security import get_current_user

router = APIRouter()
security = HTTPBearer()

# Pydantic models
class FinancialOverview(BaseModel):
    total_income: float
    total_deductions: float
    tax_liability: float
    net_income: float
    assessment_year: str

class QuickStats(BaseModel):
    documents_uploaded: int
    queries_asked: int
    reminders_pending: int
    tax_savings_estimate: float

class RecentActivity(BaseModel):
    id: str
    type: str  # query, document, reminder
    title: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

class DashboardResponse(BaseModel):
    financial_overview: FinancialOverview
    quick_stats: QuickStats
    recent_activities: List[RecentActivity]
    upcoming_reminders: List[Dict[str, Any]]
    tax_tips: List[str]

@router.get("/overview", response_model=DashboardResponse)
async def get_dashboard_overview(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Get dashboard overview with financial summary, stats, and recent activities.
    """
    # In a real implementation, you would get user-specific data
    # For now, we'll return mock/demo data that showcases the app's capabilities

    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    tax_queries = db.query(TaxQuery).filter(TaxQuery.user_id == current_user.id).all()
    reminders = db.query(Reminder).filter(Reminder.user_id == current_user.id).all()

    # Financial overview (still demo numbers but calculable fields for wow factor)
    total_income = 850000
    total_deductions = 185000 + (len(documents) * 1500)  # playful uplift with doc count
    tax_liability = max(total_income - total_deductions, 0) * 0.18
    net_income = total_income - tax_liability
    financial_overview = FinancialOverview(
        total_income=total_income,
        total_deductions=total_deductions,
        tax_liability=round(tax_liability, 2),
        net_income=round(net_income, 2),
        assessment_year="2025-26"
    )

    reminders_pending = db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.is_completed == False
    ).count()

    quick_stats = QuickStats(
        documents_uploaded=len(documents),
        queries_asked=len(tax_queries),
        reminders_pending=reminders_pending,
        tax_savings_estimate=42000 + (len(reminders) * 750)
    )

    recent_activities: List[RecentActivity] = []
    for q in tax_queries[-5:]:
        recent_activities.append(
            RecentActivity(
                id=f"query_{q.id}",
                type="query",
                title=q.query[:120],
                timestamp=q.created_at or datetime.utcnow(),
                metadata={"risk_level": q.risk_level, "confidence": q.confidence},
            )
        )
    for doc in documents[-5:]:
        recent_activities.append(
            RecentActivity(
                id=f"doc_{doc.id}",
                type="document",
                title=doc.filename,
                timestamp=doc.upload_timestamp,
                metadata={"processed": doc.processed, "size": doc.file_size},
            )
        )
    for r in reminders[-5:]:
        recent_activities.append(
            RecentActivity(
                id=f"rem_{r.id}",
                type="reminder",
                title=r.title,
                timestamp=r.created_at,
                metadata={"priority": r.priority, "due_date": r.due_date.isoformat()},
            )
        )

    # Sort by timestamp desc
    recent_activities = sorted(
        recent_activities, key=lambda item: item.timestamp, reverse=True
    )[:8]

    upcoming_reminders = [
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "due_date": r.due_date.isoformat(),
            "priority": r.priority,
            "type": r.reminder_type,
        }
        for r in reminders
        if r.due_date >= datetime.utcnow() and not r.is_completed
    ]

    # Tax tips
    tax_tips = [
        "Consider investing in ELSS for Section 80C benefits with potential market-linked returns",
        "Health insurance premiums for parents can be claimed under Section 80D (additional ₹25,000 if they are senior citizens)",
        "Don't forget to claim HRA exemption if you're living in rented accommodation",
        "Interest on education loan for higher studies is deductible under Section 80E with no upper limit",
        "Consider opting for the new tax regime if your deductions are less than ₹2.5 lakhs annually"
    ]

    return DashboardResponse(
        financial_overview=financial_overview,
        quick_stats=quick_stats,
        recent_activities=recent_activities,
        upcoming_reminders=upcoming_reminders,
        tax_tips=tax_tips
    )

@router.get("/financial-health-score")
async def get_financial_health_score(
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Calculate and return a financial health score based on user's financial profile.
    """
    # Mock implementation - in reality this would analyze user's actual data
    score = random.randint(65, 95)  # Score between 65-95

    # Determine health level
    if score >= 85:
        level = "Excellent"
        color = "green"
    elif score >= 70:
        level = "Good"
        color = "lightgreen"
    elif score >= 55:
        level = "Fair"
        color = "yellow"
    else:
        level = "Needs Improvement"
        color = "red"

    # Factors affecting score (mock)
    factors = {
        "tax_compliance": random.randint(70, 100),
        "investment_diversification": random.randint(60, 90),
        "emergency_fund": random.randint(50, 95),
        "debt_management": random.randint(65, 90),
        "retirement_planning": random.randint(55, 85)
    }

    recommendations = [
        "Consider increasing your emergency fund to cover 6 months of expenses",
        "Review your insurance coverage - ensure adequate life and health insurance",
        "Start a SIP in equity mutual funds for long-term wealth creation",
        "Consider tax-loss harvesting to offset capital gains",
        "Review your nominatons on all financial accounts and investments"
    ]

    return {
        "score": score,
        "level": level,
        "color": color,
        "factors": factors,
        "recommendations": recommendations[:3],  # Top 3 recommendations
        "assessment_date": datetime.utcnow().isoformat()
    }

@router.get("/spending-insights")
async def get_spending_insights(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_db)
):
    """
    Provide insights into spending patterns and tax optimization opportunities.
    """
    # Mock spending insights
    insights = {
        "monthly_income": 70833,  # ₹70,833 monthly
        "monthly_expenses": 45000,  # ₹45,000 monthly
        "savings_rate": 36.5,  # 36.5% savings rate
        "top_expense_categories": [
            {"category": "Rent/Housing", "amount": 15000, "percentage": 33.3},
            {"category": "Food & Groceries", "amount": 8000, "percentage": 17.8},
            {"category": "Transportation", "amount": 6000, "percentage": 13.3},
            {"category": "Utilities", "amount": 4000, "percentage": 8.9},
            {"category": "Entertainment", "amount": 3000, "percentage": 6.7},
            {"category": "Healthcare", "amount": 2500, "percentage": 5.6},
            {"category": "Others", "amount": 6500, "percentage": 14.4}
        ],
        "tax_optimization_opportunities": [
            {
                "opportunity": "Section 80C Investments",
                "current": 12000,
                "potential": 12500,  # Max ₹1.5 lakh annually = ₹12,500 monthly
                "benefit": "Save up to ₹3,750 in taxes annually (assuming 30% tax bracket)"
            },
            {
                "opportunity": "Health Insurance (Section 80D)",
                "current": 0,
                "potential": 2500,  # ₹30,000 annually
                "benefit": "Save up to ₹7,500 in taxes annually"
            },
            {
                "opportunity": "Home Loan Interest (Section 24)",
                "current": 0,
                "potential": 8333,  # If you have home loan
                "benefit": "Save up to ₹25,000 in taxes annually"
            }
        ],
        "recommendations": [
            "Consider increasing your monthly SIP to maximize Section 80C benefits",
            "Review your employer's medical insurance coverage - consider topping up if needed",
            "If you have a home loan, ensure you're claiming interest deduction properly",
            "Maintain proper documentation for all tax-saving investments and expenses"
        ]
    }

    return insights