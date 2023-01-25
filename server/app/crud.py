# create, read, update and delete
from sqlalchemy.orm import Session
from utility import generate_token, generate_timestamp
import models, schemas


def verify_user(db: Session, api_token: str):
    return db.query(models.User).filter(models.User.api_token == api_token).first()


def get_user_token(db: Session, username: str, password: str):
    token = (
        db.query(models.User)
        .filter(
            models.User.username == username, models.User.hashed_password == password
        )
        .first()
    )
    return token


def user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def verify_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_messages(db: Session, limit: int = 100):
    return (
        db.query(models.Message).order_by(models.Message.id.desc()).limit(limit).all()
    )


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password
    generated_token = generate_token()
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        api_token=generated_token,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_admin(db: Session, api_token: str, username: str):
    User = db.query(models.User).filter(models.User.api_token == api_token).first()
    if User.is_admin == True:
        promoted_user = (
            db.query(models.User).filter(models.User.username == username).first()
        )
        if promoted_user is None:
            return None
        promoted_user.is_admin = True
        db.commit()
        db.refresh(promoted_user)


def create_user_message(db: Session, text: str, api_token: str):
    # Fetch User from database using API token (unique)
    user = verify_user(db, api_token)
    time = generate_timestamp()
    if user:
        db_item = models.Message(message=text, owner_id=user.id, timestamp=time)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    return None
