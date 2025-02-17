from fastapi import Depends, HTTPException, status
from ... import schemas, models, database, oauth2
from sqlalchemy.orm import session


async def add_member(members: list[schemas.AddMember],
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
        # lấy user_id từ student_code
        us = db.query(models.Users).filter(models.Users.student_code == member.student_code).first()
        if not us:
            print({"message": "user was not exist!"})
            continue

        # check xem user đã tồn tại trong bảng memberteam chưa
        user = db.query(models.MemberTeams).filter(models.MemberTeams.team_id == team.id,
                                                    models.MemberTeams.user_id == us.id).first()
        if user:
            if user.status == False: # nếu user đã từng ở trong team
                user.status = True
                db.commit()
                db.refresh(user)
                print({"message": "successful!"})
            else: print({"message": "user was exist!"})
            continue
        if member.role == 'ctv': # thêm 1 ctv mới (role_id = 4)
            new_member = models.MemberTeams(
                user_id = us.id,
                role_id = 4,
                team_id = team.id,
                status = True
            )
            db.add(new_member)
            db.commit()
            db.refresh(new_member)
            print({"message": "successful!"})
        else: # thêm 1 user (thành viên) mới (role_id = 3)
            new_member = models.MemberTeams(
                user_id = us.id,
                role_id = 3,
                team_id = team.id,
                status = True
            )
            db.add(new_member)
            db.commit()
            db.refresh(new_member)
            print({"message": "successful!"})
    return {"message": "add members successfull!"}