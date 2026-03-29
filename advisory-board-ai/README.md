# Advisory Board AI

A game-changing app that democratizes professional advisory services for citizens with weak financial knowledge who cannot afford CA/CS/CMA consultants.

## Features

- **Banking-app level UI/UX**: Modern, intuitive interface inspired by banking apps
- **Multi-Agent AI System**: Specialized agents for Tax, Legal, Investment, and Cost advisory
- **Document Management**: Upload, process, and securely store financial documents
- **Smart Reminders**: Tax filing deadlines, investment maturity dates, compliance requirements
- **Financial Dashboard**: Overview of income, deductions, tax liability, and net income
- **Chat Interface**: Conversational AI advisor for real-time queries
- **Security & Privacy**: Bank-level security with encryption and access controls
- **Multi-language Support**: Hinglish and regional Indian languages
- **Proactive Insights**: Predictive advice based on user documents and profile

## Architecture

### Backend (Python/FastAPI)
- **API Layer**: RESTful endpoints for all functionality
- **Core Services**:
  - Tax RAG System (Retrieval-Augmented Generation)
  - Document Processing Pipeline
  - Authentication & Authorization
  - Reminder & Notification System
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Vector Store**: ChromaDB (development) / Pinecone (production)
- **Security**: JWT-based authentication, role-based access control

### Frontend (Next.js/TypeScript)
- **UI Framework**: Tailwind CSS with shadcn/ui components
- **State Management**: React hooks and context
- **Real-time Features**: WebSocket connections for live updates
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG 2.1 compliant

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ and npm
- Python 3.11+

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd advisory-board-ai
```

2. Start the services using Docker Compose
```bash
docker-compose up --build
```

3. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Setup (without Docker)

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create a `.env` file in the backend directory with:
```
DATABASE_URL=sqlite:///./advisory_board_ai.db
SECRET_KEY=your-secret-key-here-change-in-production
```

## Project Structure

```
advisory-board-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core logic (RAG, security, database)
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic services
│   │   └── utils/        # Utility functions
│   ├── requirements.txt  # Python dependencies
│   ├── Dockerfile        # Container definition
│   └── main.py           # Application entry point
├── frontend/
│   ├── src/
│   │   ├── app/          # Next.js pages and layout
│   │   ├── components/   # React components
│   │   ├── widgets/      # Dashboard widgets
│   │   └── lib/          # Utilities and hooks
│   ├── package.json      # Node.js dependencies
│   ├── Dockerfile        # Container definition
│   └── tsconfig.json     # TypeScript configuration
├── docker-compose.yml    # Multi-container setup
└── README.md             # This file
```

## Features Implemented (Hackathon MVP)

### Phase 1: Tax Advisor RAG System
- Retrieval-Augmented Generation over Income Tax Act
- Citation enforcement with explicit source references
- Risk tiering system (Low/Medium/High risk)
- Tax deduction calculator for common sections (80C, 80D, 24, etc.)

### Phase 2: Document Management
- Secure file upload and storage
- PDF and image processing
- Entity extraction from documents
- Integration with RAG system for contextual advice

### Phase 3: Dashboard & UI
- Banking-inspired dashboard with financial overview
- Quick stats and recent activity feed
- Upcoming reminders calendar
- Tax saving tips and insights
- Conversational chat interface

### Phase 4: Reminder System
- Tax filing deadline reminders
- Installment payment alerts
- Compliance requirement notifications
- Customizable recurring reminders

## Future Enhancements (Post-Hackathon)

### Phase 2: Multi-Agent Expansion
- Legal Advisor Agent (Company Law, Contracts)
- Investment Advisor Agent (Portfolio Theory, SEBI Guidelines)
- Cost Advisor Agent (Cost Analysis, Profitability Optimization)
- Agent-to-agent deliberation and consensus building

### Phase 3: Advanced Features
- Human-in-the-loop marketplace for professional verification
- Voice interface for accessibility
- Offline mode with progressive web app capabilities
- Regional language support (Hinglish, Tamil, Telugu, etc.)
- Integration with government APIs (Income Tax Portal, GSTN, MCA)

### Phase 4: Scale & Enterprise
- B2B SaaS for CA/CS firms
- Multi-region deployment
- Advanced analytics and reporting
- AI-powered financial health scoring

## Security Features

- End-to-end encryption for sensitive documents
- Role-based access control (RBAC)
- Audit logging for all transactions
- Secure session management with JWT
- Input validation and sanitization
- Protection against common vulnerabilities (OWASP Top 10)

## Technology Choices

### Backend
- **FastAPI**: High-performance, async-first Python framework
- **SQLAlchemy**: Robust ORM with migration support
- **ChromaDB**: Open-source vector database for RAG
- **Sentence Transformers**: State-of-the-art embedding models
- **PyPDF2/pdfplumber**: Reliable PDF text extraction
- **bcrypt**: Secure password hashing

### Frontend
- **Next.js 14**: React framework with excellent performance
- **TypeScript**: Type safety and developer experience
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide Icons**: Beautiful, consistent icon set
- **shadcn/ui**: Accessible, customizable components

## License

MIT License - feel free to use, modify, and distribute.

## Contact

For questions or support, please open an issue in the repository.

---

*Advisory Board AI: Transforming professional expertise from a luxury to a utility.*