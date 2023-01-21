from fastapi import APIRouter, Depends, HTTPException

import crud, schemas
from utility import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/messages",
    tags=["messages"],
    responses={403: {"description": "Invalid credentials"}},
)


@router.post("/post/", status_code=200, description="Saves message to database")
def post_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user_message(
        db, text=message.message, api_token=message.api_token
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
