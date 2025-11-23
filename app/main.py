from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routes import auth, users, services

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(services.router, prefix=settings.API_V1_STR, tags=["services"])

@app.get("/")
def root():
    return {"message": "Welcome to the Gym Management API", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}