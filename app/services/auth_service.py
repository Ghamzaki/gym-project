from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token, get_password_hash, pwd_context
from app.services import user_service


def authenticate_user(db: Session, email: str, password: str):
    user = user_service.get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    # If the stored hash uses an older algorithm or parameters, re-hash with the
    # current preferred algorithm and update the DB. This migrates existing
    # bcrypt hashes to Argon2 over time.
    try:
        if pwd_context.needs_update(user.hashed_password):
            new_hash = get_password_hash(password)
            user.hashed_password = new_hash
            db.add(user)
            db.commit()
            db.refresh(user)
    except Exception:
        # Do not fail authentication if re-hash/update fails; log in silently.
        pass

    return user


def create_user_token(user):
    """Create an access token for the given user.

    The token `sub` claim contains the user's email so that
    the dependency logic (which looks up users by email) works.
    """
    return create_access_token(data={"sub": str(user.email)})