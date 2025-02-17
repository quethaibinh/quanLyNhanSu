from fastapi import Depends, HTTPException, status
from ... import schemas, models, database, oauth2
from sqlalchemy.orm import session


async def update_person_info(info_update: schemas.UpdatePersonInfo,
                              current_user: int = Depends(oauth2.get_current_user),
                              db: session = Depends(database.get_db)):
    # update ngày sinh
    birth = db.query(models.Date).filter(current_user.birth_date_id == models.Date.id).first()
    if not birth:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f'error update birthday')
    birth.day = info_update.birthday.day
    birth.mon = info_update.birthday.mon
    birth.year = info_update.birthday.year
    db.commit()
    db.refresh(birth)

    user_record = db.query(models.Users).filter(models.Users.id == current_user.id).first()
    user_record.first_name = info_update.first_name
    user_record.last_name = info_update.last_name
    user_record.email = info_update.email
    user_record.student_code = info_update.student_code
    user_record.class_code = info_update.class_code
    user_record.academic_year = info_update.academic_year
    user_record.hometown = info_update.hometown
    user_record.facebook_link = info_update.facebook_link
    user_record.address = info_update.address
    user_record.phone = info_update.phone
    user_record.is_active = info_update.is_active
    user_record.sex = info_update.sex

    db.commit()
    db.refresh(user_record)

    return {"message": "User information updated successfully.", "user": user_record}


