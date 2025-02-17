from fastapi import Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import session
import pandas as pd
from io import BytesIO  # Import BytesIO
from . import createUser
from ... import schemas, models, database, utils
import logging

# Cấu hình logger để dễ dàng debug
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def upload_excel(file: UploadFile = File(...), db: session = Depends(database.get_db)):
    # Kiểm tra định dạng file
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The uploaded file must be an Excel file with .xlsx or .xls extension.")

    try:
        # Đọc dữ liệu từ file Excel bằng BytesIO
        contents = await file.read()  # Đọc toàn bộ nội dung file vào bộ nhớ
        file_like = BytesIO(contents)  # Tạo đối tượng BytesIO từ nội dung file
        data = pd.read_excel(file_like, engine='openpyxl')  # Đọc dữ liệu Excel

        # Xử lý cột birthday
        data["birthday"] = pd.to_datetime(data["birthday"], errors="coerce", dayfirst=True)

        # Kiểm tra nếu có giá trị NaT (không hợp lệ)
        if data["birthday"].isnull().any():
            invalid_rows = data[data["birthday"].isnull()].index.tolist()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Invalid birthday values at rows: {invalid_rows}")

        # Chuyển sang định dạng dd/mm/yyyy trước khi trả về hoặc lưu vào database
        data["birthday"] = data["birthday"].dt.strftime('%d/%m/%Y')

        # Kiểm tra nếu các cột cần thiết bị thiếu
        required_columns = ["name", "class_code", "student_code", "academic_year", "email", "facebook_link", "hometown",
                            "is_active", "sex", "address", "phone", "role"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Missing required columns: {', '.join(missing_columns)}")

        success_count = 0  # Biến đếm số lượng người dùng được tạo thành công

        for index, row in data.iterrows():
            # Xử lý tên đầy đủ, chia tách thành họ và tên
            name = list(row['name'].split())
            last_name = name[-1].strip().title()
            first_name = " ".join(name[:-1]).strip().title()
            class_code = str(row['class_code'])
            student_code = str(row['student_code'])
            academic_year = row['academic_year']
            email = str(row['email'])
            address = str(row['address'])
            phone = str(row['phone'])
            facebook_link = str(row['facebook_link'])
            hometown = row['hometown']
            is_active = row['is_active']
            birthday = row['birthday']
            sex = row['sex']
            role = row['role']

            # Tạo đối tượng user từ schema
            new_user = schemas.UserCreate(**{
                'last_name': last_name,
                'first_name': first_name,
                'class_code': class_code,
                'student_code': student_code,
                'academic_year': academic_year,
                'email': email,
                'address': address,
                'phone': phone,
                'facebook_link': facebook_link,
                'hometown': hometown,
                'is_active': is_active,
                'birthday': birthday,
                'sex': sex,
                'role_code': role
            })

            try:
                # Tạo người dùng và lưu vào cơ sở dữ liệu
                await createUser.create_user(new_user, db)
                success_count += 1
                logger.debug(f"User created successfully: {new_user}")
            except Exception as e:
                logger.error(f"Error creating user for row {index + 1}: {str(e)}")
                # Nếu có lỗi khi tạo người dùng, có thể tiếp tục với các dòng khác

        # Trả về thông báo thành công
        return {"message": f"File processed successfully. {success_count} users created."}

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred while processing the file: {str(e)}")