from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token
from app.services import user_service


def authenticate_user(db: Session, email: str, password: str):
    user = user_service.get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user_token(user):
    """Create an access token for the given user.

    The token `sub` claim contains the user's email so that
    the dependency logic (which looks up users by email) works.
    """
    return create_access_token(data={"sub": str(user.email)})