from fastapi import Depends, HTTPException, status
from ... import schemas, models, database, oauth2, utils
from sqlalchemy.orm import session


async def update_password(password: schemas.PasswordU,
                          current_user: int = Depends(oauth2.get_current_user),
                          db: session = Depends(database.get_db)):
    #tìm user trong bảng authentications
    auth = db.query(models.Authentications).filter(models.Authentications.id == current_user.id).first()
    if not auth:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f'account was not exist!')
    check = utils.verify(password.old_password, auth.password)
    if not check:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                            detail= f'password was incorrect')
    if not utils.validate(password.new_password):
        raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail= f'weak password!')
    auth.password = utils.hashed(password.new_password)
    db.commit()
    db.refresh(auth)
    return {"message": "update password successful!"}