from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# We use pool_pre_ping to avoid "server has gone away" errors
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True, 
    echo=True # Set to False in production
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency injection for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()