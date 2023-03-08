from fastapi import APIRouter, Depends, HTTPException

import crud, schemas

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    responses={
        403: {"description": "Invalid credentials"},
        200: {"description": "Request OK"},
    },
)

from main import get_db


@router.post("/post/", status_code=200, description="Saves message to database")
def post_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user_message(
        db,
        text=message.message,
        api_token=message.api_token,
        chat_uuid=message.room_uuid,
    )
    if db_user:
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=403, detail="API token not valid!")


@router.get(
    "/get/", status_code=200, description="Returns 100 last messages from the server"
)
async def get_messages(db: Session = Depends(get_db)):
    msg_list = crud.get_messages(db)
    messages = []
    for msg in msg_list:
        messages.append(msg.__dict__)
    messages.reverse()
    return messages


@router.get(
    "/get/{limit}",
    status_code=200,
    description="Returns custom amount of messages from the server",
)
async def get_x_messages(db: Session = Depends(get_db), limit=str):
    msg_list = crud.get_messages(db, limit=limit)
    messages = []
    for msg in msg_list:
        messages.append(msg.__dict__)
    messages.reverse()
    return messages
