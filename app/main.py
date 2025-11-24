from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.routes import auth, users, services
from app.db.base_class import Base
from app.db.session import engine

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Enable CORS (configured via settings)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(services.router, prefix=settings.API_V1_STR, tags=["services"])

# Serve the minimal frontend from the `frontend/` folder. API routes take precedence.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

