# More info on:
# https://fastapi.tiangolo.com/tutorial/sql-databases/

from pydantic import BaseModel


class MessageBase(BaseModel):
    user_id: int
    recipient_id: int
    message: str

    class Config:
        orm_mode = True


class MessageCreate(MessageBase):
    api_token: str
    room_uuid: str


class Message(MessageBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    api_token: str

    class Config:
        orm_mode = True


class ChatroomBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ChatRoomCreate(ChatroomBase):
    api_token: str


class ChatRoomJoinUUID(BaseModel):
    room_uuid: str
    api_token: str


class MessageGet(MessageBase):
    pass
