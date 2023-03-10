from fastapi import APIRouter, Depends, HTTPException
import crud, schemas

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/chatroom",
    tags=["chatroom"],
    responses={
        403: {"description": "Invalid credentials"},
        200: {"description": "Request OK"},
    },
)

from main import get_db, redis_client#, producer

@router.post("/post/", status_code=200, description="Post chatroom messages")
def post_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    if not crud.get_chatroom_uuid(db, message.room_uuid):
        return HTTPException(
            status_code=404, detail=f"Chatroom with UUID {message.room_uuid} not found!",
            headers="Not found"
        )
    if not crud.verify_user_in_chatroom(db, message.room_uuid, message.api_token):
        return HTTPException(
            status_code=409, detail=f"You are not a member of this community",
            headers="Not a member"
        )
    db_user = crud.create_user_message(
        db, text=message.message, api_token=message.api_token, chat_uuid=message.room_uuid
    )
    db_user = True
    if db_user:
        print(message)
        i = 1
        redis_client.publish(message.room_uuid, str(f"{message.user}:{message.message}"))
        # producer.send(message.room_uuid, message.message)
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=403, detail="API token not valid!")

@router.post("/create/", status_code=200, description="Create a chatroom")
def create_chatroom(chatroom: schemas.ChatRoomCreate, db: Session = Depends(get_db)):
    if not crud.verify_user(db, chatroom.api_token):
        raise HTTPException(status_code=403, detail="API token not valid!")

    if crud.verify_chatroom_name(db, chatroom.name):
        return HTTPException(
            status_code=409, detail="Chatroom already exists with this name!"
        )
    chat = crud.create_chatroom(db, api_token=chatroom.api_token, name=chatroom.name)
    if chat:
        return {"name": chat.name, "uuid": chat.uuid}
    else:
        raise HTTPException(status_code=403, detail="API token not valid!")

@router.get("/rooms/")
def get_user_chatrooms(api_token: schemas.ChatRoomGet, db: Session = Depends(get_db)):
    if not crud.verify_user(db, api_token.api_token):
        raise HTTPException(status_code=403, detail="API token not valid!")
    rooms = crud.get_rooms(db, api_token.api_token)
    return rooms

@router.post("/join/", status_code=200, description="Join existing chatroom")
def join_chatroom_by_link(
    chatroom: schemas.ChatRoomJoinUUID, db: Session = Depends(get_db)
):
    if not crud.verify_user(db, chatroom.api_token):
        raise HTTPException(status_code=403, detail="API token not valid!")
    userid = crud.get_id_from_token(db, chatroom.api_token)
    chatid = crud.get_chatroom_uuid(db, chatroom.room_uuid)
    if not chatid:
        raise HTTPException(
            status_code=404, detail=f"Chatroom with name {chatroom.room_uuid} not found!"
        )
    join = crud.join_chatroom(db, userid.id, chatid.id)
    if join:
        return join
    else:
        raise HTTPException(
            status_code=409, detail=f"You are already member of this chatroom!"
        )


@router.post(
    "/leave/", status_code=200, description="Leave a group you are a member of"
)
def leave_chatroom_by_link(
    chatroom: schemas.ChatRoomJoinUUID, db: Session = Depends(get_db)
):
    """Leave an existing group you are part of"""
    if not crud.verify_user(db, chatroom.api_token):
        raise HTTPException(status_code=403, detail="API token not valid!")
    userid = crud.get_id_from_token(db, chatroom.api_token)
    chatid = crud.get_chatroom_uuid(db, chatroom.room_uuid)
    if not chatid:
        raise HTTPException(
            status_code=404, detail=f"Chatroom with uuid {chatroom.uuid} not found!"
        )
    leave = crud.leave_chatroom(db, userid.id, chatid.id)
    if leave:
        return {"status": "ok", "info": "Succesfully left chatroom"}
    else:
        raise HTTPException(
            status_code=409, detail="You are not member of this chatroom!"
        )
