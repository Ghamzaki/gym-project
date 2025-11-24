# Gym Management API

A FastAPI backend with PostgreSQL database, JWT authentication, and a minimal static frontend. Deployed on Render with Docker.

## Features

- **FastAPI Backend**: RESTful API with automatic OpenAPI docs
- **PostgreSQL Database**: Production-ready database with Alembic migrations
- **JWT Authentication**: Secure token-based authentication
- **Static Frontend**: Simple HTML/CSS/JavaScript interface
- **Docker Deployment**: Containerized for easy deployment on Render
- **Password Security**: Argon2 or bcrypt hashing

## Quick Start

### Local Development

1. **Clone and setup**:
```bash
git clone <your-repo>
cd gym-project
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your local database and secrets
```

3. **Run locally**:
```bash
# Start the app
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Or use Docker
docker-compose up --build
```

4. **Access**:
- **Frontend**: `http://127.0.0.1:8000/`
- **API Docs**: `http://127.0.0.1:8000/docs`
- **Health Check**: `http://127.0.0.1:8000/health`

### Database Setup

For local development with SQLite:
- Keep `DATABASE_URL=sqlite:///./gym.db` in `.env`

For production with PostgreSQL:
- Use `DATABASE_URL=postgresql://user:pass@host:5432/dbname`
- Run migrations: `alembic upgrade head`

## Deploy to Render

### 1. Prepare Repository
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Create Render Services

**PostgreSQL Database:**
- Go to Render Dashboard → New → PostgreSQL
- Name: `gym-db`
- Copy the **External Database URL**

**Web Service:**
- Go to Render Dashboard → New → Web Service
- Connect your GitHub repository
- **Runtime**: Docker
- **Build Command**: `docker build .`
- **Start Command**: `docker run -p 8000:8000 <image>`

### 3. Configure Environment Variables
In your Render Web Service settings → Environment:

```env
SECRET_KEY=your_strong_random_secret_here
DATABASE_URL=postgresql://your_db_connection_string
BACKEND_CORS_ORIGINS=["https://your-frontend.onrender.com"]
```

### 4. Run Database Migrations
After deployment:
- Go to your service → Shell
- Run: `alembic upgrade head`

### 5. Access Your App
- **Production URL**: `https://your-service-name.onrender.com`
- **API Docs**: `https://your-service-name.onrender.com/docs`

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing secret | Generate with `openssl rand -hex 32` |
| `DATABASE_URL` | Database connection string | `postgresql://user:pass@host:5432/db` |
| `BACKEND_CORS_ORIGINS` | Allowed frontend origins | `["https://frontend.onrender.com"]` |

## API Endpoints

- `GET /health` - Health check
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/services` - List gym services
- `POST /api/v1/services` - Create service (admin)

Full API documentation at `/docs` when running.

## Project Structure

```
gym-project/
├── app/
│   ├── main.py              # FastAPI app
│   ├── core/
│   │   └── config.py        # Settings & configuration
│   ├── api/v1/
│   │   ├── routes/          # API endpoints
│   │   └── dependencies/    # Dependencies
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── db/                  # Database connection
├── frontend/                # Static HTML/CSS/JS
├── alembic/                 # Database migrations
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md
```

## Development Notes

- **Security**: Never commit `.env` to version control
- **Migrations**: Use Alembic for all database schema changes
- **Testing**: Add tests in a `tests/` directory
- **Frontend**: The included frontend is basic; enhance for production use

## Technologies

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Auth**: JWT tokens, Argon2/bcrypt hashing
- **Deployment**: Docker, Render
- **Migrations**: Alembic
- **Validation**: Pydantic
