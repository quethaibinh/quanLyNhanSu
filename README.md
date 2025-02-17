# QuanLyNhanSu-TYP
tải thư viện bằng câu lệnh: pip install -r requirements.txt
cách tạo (cập nhật) db postgresql bằng alembic: alembic upgrade head

# Bảng roles mặc định:

Mặc định là có 4 role tương ứng với id:
                        + 1 - admin (1 tài khoản duy nhất),
					    + 2 - lead,
					    + 3 - user,
					    + 4 - CTV

# Bảng teams mặc đinh:
Mặc định có 5 team:
            + 1 - page,
            + 2 - group,
            + 3 - media,
            + 4 - titok,
            + 5 - dev

# Chức năng

Những chức năng chính là: 
+ hiển thị những thông tin của user (có lọc với tìm kiếm theo filed) 
+ phân quyền cho lead của 1 team(chỉ có quyền với team mình): có quyền đưa CTV lên làm user, đưa user lên làm lead, kick user ra khỏi team, thêm user vào team, với những team khác thì lead cũng có chức năng như user thường (chỉ xem).
+ admin có tất cả các quyền.


# Chi tiết

+ login, create, create by excel
+ hiển thị tất cả user (không cần đăng nhập vẫn hiển thị được)
+ hiển thị user theo team, cần đăng nhập và phải truyền vào 1 body dạng {"id": id_team} để xác định được team cần hiển thị
+ leader và admin có quyền add 1 hoặc nhiều người vào 1 team cũng có quyền kick 1 hoặc nhiều người khỏi 1 team (body chuyền vào dạng JSON (class AddMemberTeam, KickMemberTeam trong file schemas.py))
+ leader và admin có quyền update role cho user từ ctv lên user hoặc user lên leader (body truyền vào dạng classclass UpdateRoleMember trong schemas.py)
+ chỉ có admin mới có quyền hủy role leader của 1 team
+ có chức năng sửa thông tin cá nhân và sửa mật khẩu (body truyền vào dạng JSON class UpdatePersonInfo và class PasswordU trong schemas)