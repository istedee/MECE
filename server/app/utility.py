import secrets, datetime
from db import SessionLocal


def generate_token() -> str:
    return secrets.token_hex(16)


def generate_timestamp() -> str:
    return datetime.datetime.now()


# Init db if not existing
# Database connection function for use in routers
# And accross the REST API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
