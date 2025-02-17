from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from .. import models, utils, oauth2
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


async def login(user_confirm: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.Authentications).filter(models.Authentications.email == user_confirm.username).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "email was incorrect!")
    
    password = utils.verify(user_confirm.password, user.password)
    if not password:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            detail = "password was incorrect")
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return{"access_token": access_token, "token_type": "bearer"}