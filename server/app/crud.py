# create, read, update and delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from utility import generate_token, generate_timestamp, generate_chatroom_uuid
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


def get_id_from_token(db: Session, api_token: str):
    """Returns users id from apitoken"""
    return db.query(models.User.id).filter(models.User.api_token == api_token).first()


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


def verify_chatroom_name(db: Session, name: str):
    """Verify that proposed chatroom name is unique"""
    return db.query(models.ChatRoom).filter(models.ChatRoom.name == name).first()


def get_chatroom_uuid(db: Session, chatroom_id: str):
    """Return chatroom id by link uuid"""
    return (
        db.query(models.ChatRoom.id).filter(models.ChatRoom.uuid == chatroom_id).first()
    )


def create_chatroom(db: Session, api_token: str, name: str):
    """Create a new chatroom"""
    chatroom_uuid = generate_chatroom_uuid()
    chatroom = models.ChatRoom(uuid=chatroom_uuid, name=name)
    try:
        db.add(chatroom)
        db.commit()
        db.refresh(chatroom)
        return chatroom
    except IntegrityError:
        # Try to generate a new uuid for the room
        # In case of a duplicate
        Session.rollback()
        chatroom_uuid = generate_chatroom_uuid()
        chatroom = models.ChatRoom(uuid=chatroom_uuid, name=name)
        db.add(chatroom)
        db.commit()
        db.refresh(chatroom)
        return chatroom


def join_chatroom(db: Session, member_id: int, chatroom_id: int):
    """Join existing chatroom"""
    membership = models.Membership(
        member_id=member_id, chatroom_id=chatroom_id, public_key=""
    )
    existing = (
        db.query(models.Membership.member_id)
        .filter(models.Membership.member_id == member_id)
        .filter(models.Membership.chatroom_id == chatroom_id)
        .first()
    )
    if not existing:
        db.add(membership)
        db.commit()
        db.refresh(membership)
        return membership
    else:
        return None


def leave_chatroom(db: Session, member_id: int, chatroom_id: int):
    """Leave an existing chatroom"""
    existing = (
        db.query(models.Membership.member_id)
        .filter(models.Membership.member_id == member_id)
        .filter(models.Membership.chatroom_id == chatroom_id)
        .first()
    )
    if not existing:
        return None
    else:
        leave = (
            db.query(models.Membership)
            .filter(models.Membership.member_id == member_id)
            .filter(models.Membership.chatroom_id == chatroom_id)
            .delete()
        )
        return leave
