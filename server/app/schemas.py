# More info on:
# https://fastapi.tiangolo.com/tutorial/sql-databases/

from pydantic import BaseModel


class MessageBase(BaseModel):
    message: str
    api_token: str


class MessageCreate(MessageBase):
    pass


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
    uuid: str
    api_token: str
