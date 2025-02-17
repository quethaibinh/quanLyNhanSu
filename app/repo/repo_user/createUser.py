from fastapi import Depends, HTTPException, status
from ... import schemas, models, database, utils
from sqlalchemy.orm import session
from datetime import datetime

async def checkUserExit(user: schemas.UserCreate, db: session = Depends(database.get_db)):
    user_check = db.query(models.Users).filter(models.Users.student_code == user.student_code).first()
    if user_check: return True
    email = db.query(models.Users).filter(models.Users.email == user.email).first()
    if email: return True
    return False


async def create_user(user: schemas.UserCreate, db: session = Depends(database.get_db)):
    if await checkUserExit(user, db):
        print('user was exist!')
        return
    try:
        # Chuyển chuỗi ngày sinh thành đối tượng datetime
        parsed_date = datetime.strptime(user.birthday, "%d/%m/%Y")
        day = parsed_date.day
        mon = parsed_date.month
        year = parsed_date.year

        birth = models.Date(day=day, mon=mon, year=year)
        db.add(birth)
        db.commit()
        db.refresh(birth)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid date format. Expected format is dd/mm/yyyy")

    # Tạo người dùng mới, và liên kết ngày sinh với user
    new_user = models.Users(birth_date_id=birth.id,
                            last_name = user.last_name,
                            first_name = user.first_name,
                            email = user.email,
                            class_code = user.class_code,
                            student_code = user.student_code,
                            academic_year = user.academic_year,
                            facebook_link = user.facebook_link,
                            address = user.address,
                            phone = user.phone,
                            hometown = user.hometown,
                            sex = user.sex,
                            is_active = user.is_active,
                            role_code = user.role_code.upper()
                            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Tạo mật khẩu cho người dùng mới
    password = f"{user.student_code}@123"
    # Thêm thông tin xác thực (Authentication) cho người dùng mới
    auth = models.Authentications(
        id=new_user.id,
        email=new_user.email,
        password=utils.hashed(password)
    )
    db.add(auth)
    db.commit()

    # Trả về thông tin người dùng mới
    # return new_user
    return {"message": "successful!"}