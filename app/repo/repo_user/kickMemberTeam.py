from fastapi import Depends, HTTPException, status
from ... import schemas, models, database, oauth2
from sqlalchemy.orm import session

async def kick_member(members: list[schemas.KickMember],
                     team: schemas.Team,
                     current_user: int = Depends(oauth2.get_current_user),
                     db: session = Depends(database.get_db)):
    # check xem nguời dùng hiện tại có quyền add không (admin, leader)
    check1 = db.query(models.MemberTeams).filter(models.MemberTeams.user_id == current_user.id,
                                                models.MemberTeams.team_id == team.id,
                                                models.MemberTeams.role_id == 2).first()
    check2 = db.query(models.Users).filter(models.Users.id == current_user.id,
                                            models.Users.role_code == 'ADMIN').first()
    if not check1 and not check2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail= f'you are not leader!')
    for member in members:
        # check xem user đã tồn tài trong bảng memberteam chưa
        user = db.query(models.MemberTeams).filter(models.MemberTeams.team_id == team.id,
                                                    models.MemberTeams.user_id == member.user_id).first()
        if not user:
            print({"message": "user was not exist in this team!"})
            continue
        # nếu muốn huỷ leader thì chỉ có admin mới có quyền
        if user.role_id == 2 and not check2: 
            print({"message": "no authentication!"})
            continue
        user.status = False
        db.commit()
        db.refresh(user)
        print({"message": "successful!"})
    return {"message": "kick members successfull!"}