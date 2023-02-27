import crud, schemas
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from main import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.verify_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already in use!")
    return crud.create_user(db=db, user=user)


@router.post("/check-api-token/", response_model=schemas.User)
def check_user_apitoken(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_token = crud.get_user_token(db, username=user.username, password=user.password)
    if user_token:
        return user_token
    else:
        raise HTTPException(status_code=403, detail="Invalid username or password!")


# Sanity check users for development purposes
@router.get("/{username}")
def get_user_info(username: str, db: Session = Depends(get_db)):
    db_user = crud.user(db, username=username)
    return db_user
