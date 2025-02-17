from fastapi import Depends, HTTPException, status
from ... import schemas, models, database, oauth2
from sqlalchemy.orm import session

async def update_role(role: schemas.UpdateRoleMember,
                      current_user: int = Depends(oauth2.get_current_user),
                      db: session = Depends(database.get_db)):
    #check user hiện tại có quyền không
    check1 = db.query(models.MemberTeams).filter(models.MemberTeams.user_id == current_user.id,
                                                models.MemberTeams.team_id == role.team_id,
                                                models.MemberTeams.role_id == 2).first()
    check2 = db.query(models.Users).filter(models.Users.id == current_user.id,
                                            models.Users.role_code == 'ADMIN').first()
    if not check1 and not check2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f'you are not leader!')
    # check user đã tồn tại trong team chưa
    check = db.query(models.MemberTeams).filter(models.MemberTeams.user_id == role.user_id,
                                                models.MemberTeams.team_id == role.team_id).first()
    if not check:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f'user was not exist!')
    if role.role == "leader":
        if check.role_id == 2:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                                detail= f'this user was leader!')
        check.role_id = 2
        db.commit()
        db.refresh(check)
    elif role.role == "tv":
        if check.role_id == 2 or check.role_id == 3:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                                detail= f'this user was exist!')
        check.role_id = 3
        db.commit()
        db.refresh(check)
    else: 
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                            detail= f'type role: tv or leader')
    return {"message": "successful!"}


async def downgrade_role(downgrade: schemas.DowngradeRoleMember,
                         current_user: int = Depends(oauth2.get_current_user),
                         db: session = Depends(database.get_db)):
    #check xem current_user có phải là admin hay không
    admin = db.query(models.Users).filter(models.Users.id == current_user.id,
                                        models.Users.role_code == 'ADMIN').first()
    if not admin:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f'you are not admin!')
    user = db.query(models.MemberTeams).filter(models.MemberTeams.user_id == downgrade.user_id,
                                               models.MemberTeams.team_id == downgrade.team_id,
                                               models.MemberTeams.role_id == 2).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail= f'user are not leader!')
    user.role_id = 3
    db.commit()
    db.refresh(user)

    return {"message": "downgrade role user successful!"}