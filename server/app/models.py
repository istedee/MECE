from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    """Database model for Users"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True)
    hashed_password = Column(String(256))
    api_token = Column(String(64))
    is_admin = Column(Boolean, default=False)

    messages = relationship("Message", back_populates="owner")
    memberships = relationship("Membership", back_populates="member")


class Message(Base):
    """Database model for user sent messages"""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String(2048))
    owner_id = Column(Integer, ForeignKey("users.id"))
    chatroom_uuid = Column(String(32), ForeignKey("chatrooms.uuid"))
    timestamp = Column(String(64))

    owner = relationship("User", back_populates="messages")
    room = relationship("ChatRoom", back_populates="chatrooms")


class Membership(Base):
    """Database model for ChatRoom membership"""

    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("users.id"))
    chatroom_id = Column(Integer, ForeignKey("chatrooms.id"))
    public_key = Column(String(2048), nullable=True)

    member = relationship("User", back_populates="memberships")
    chatroom = relationship("ChatRoom", back_populates="members")


class ChatRoom(Base):
    """Database model for created chat rooms"""

    __tablename__ = "chatrooms"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(64), unique=True, index=True)
    name = Column(String(32), unique=True)

    chatrooms = relationship("Message", back_populates="room")
    members = relationship("Membership", back_populates="chatroom")
