# CyberGuard AI Advisor

AI-powered cybersecurity threat intelligence platform that transforms reactive alert management into proactive, explainable threat intelligence.

## Product Vision

To become the trusted AI advisor that transforms cybersecurity from reactive alert management to proactive, explainable threat intelligence, empowering every security professional with clarity and confidence.

## Target Audience

Enterprise security teams including:
- CISOs (Chief Information Security Officers)
- SOC (Security Operations Center) analysts
- Security engineers
- IT administrators managing complex digital infrastructures

## Core Features

- **Threat Management**: Create, read, update, and delete threat intelligence records
- **Alert Management**: Track and manage security alerts with severity levels
- **Threat Analysis**: AI-powered analysis and recommendations for threats

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **Architecture**: Modular Monolith

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Clone the repository or navigate to the project directory:
```bash
cd /app/user_workspace/team_062/477782eb-516d-41e7-824e-4fe944ce40e9
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` file and update the configuration values, especially:
- `SECRET_KEY`: Use a strong random string for production
- `DATABASE_URL`: Update if using PostgreSQL instead of SQLite

## Running the Application

### Development Mode

Run the application with auto-reload enabled:

```bash
python -m backend.main
```

Or using uvicorn directly:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Threats

- `POST /api/v1/threats/` - Create a new threat
- `GET /api/v1/threats/` - List all threats (with optional filters)
- `GET /api/v1/threats/{threat_id}` - Get a specific threat
- `PUT /api/v1/threats/{threat_id}` - Update a threat
- `DELETE /api/v1/threats/{threat_id}` - Delete a threat

### Alerts

- `POST /api/v1/alerts/` - Create a new alert
- `GET /api/v1/alerts/` - List all alerts (with optional filters)
- `GET /api/v1/alerts/{alert_id}` - Get a specific alert
- `PUT /api/v1/alerts/{alert_id}` - Update an alert
- `DELETE /api/v1/alerts/{alert_id}` - Delete an alert

### Analysis

- `POST /api/v1/analysis/` - Create a new threat analysis
- `GET /api/v1/analysis/` - List all analyses (with optional filters)
- `GET /api/v1/analysis/{analysis_id}` - Get a specific analysis
- `PUT /api/v1/analysis/{analysis_id}` - Update an analysis
- `DELETE /api/v1/analysis/{analysis_id}` - Delete an analysis

## Project Structure

```
.
├── backend/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── __init__.py
│       ├── threats.py       # Threat endpoints
│       ├── alerts.py        # Alert endpoints
│       └── analysis.py      # Analysis endpoints
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Database Models

### Threat
- Threat intelligence records with severity levels, confidence scores, and mitigation steps
- Status tracking: active, investigating, mitigated, resolved, false_positive

### Alert
- Security alerts with source/destination IPs and affected systems
- Status tracking: new, acknowledged, in_progress, resolved, dismissed

### Analysis
- AI-powered threat analysis with findings and recommendations
- Risk scoring and analyst attribution

## Environment Variables

Key environment variables (see `.env.example` for full list):

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT tokens
- `DEBUG`: Enable/disable debug mode
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `ALLOWED_ORIGINS`: CORS allowed origins

## Security Features

- Input validation using Pydantic schemas
- SQL injection prevention through SQLAlchemy ORM
- CORS configuration for API security
- Environment-based configuration (no hardcoded secrets)
- Structured logging for audit trails

## Development

### Adding New Features

1. Create new models in `backend/models.py`
2. Define schemas in `backend/schemas.py`
3. Create router in `backend/routers/`
4. Register router in `backend/main.py`

### Database Migrations

For production use, consider implementing Alembic for database migrations:

```bash
pip install alembic
alembic init alembic
```

## Production Deployment

For production deployment:

1. Use PostgreSQL instead of SQLite
2. Set `DEBUG=False` in environment variables
3. Use a strong `SECRET_KEY`
4. Configure proper CORS origins
5. Set up HTTPS/TLS
6. Implement rate limiting
7. Add monitoring and logging
8. Use a production ASGI server (uvicorn with workers)

Example production command:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## License

Proprietary - Enterprise Security Platform

## Support

For support and questions, contact your security team administrator.
