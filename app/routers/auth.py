from fastapi import APIRouter, HTTPException, Response, Depends, status
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from ..database import engine, get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..repo import repo_login

router = APIRouter(
    tags = ["authentication"]
)

@router.post("/login", response_model = schemas.Token) 
async def login(user_confirm: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await repo_login.login(user_confirm, db)

