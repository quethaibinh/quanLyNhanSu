from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    email: EmailStr
    last_name: str
    first_name: str
    class_code: str
    student_code: str
    academic_year: int
    facebook_link: str
    address: str
    phone:str
    hometown: str
    sex:str
    is_active: bool


class UserCreate(User):
    birthday: str
    role_code: str
    
    class Config:
        orm_mode: True
    

class Datee(BaseModel):
    day: int
    mon: int
    year: int

    class Config:
        orm_mode: True


class Role(BaseModel):
    id: int
    detail: str

    class Config:
        orm_mode = True
        from_attributes = True


class Team(BaseModel):
    id: int


class TeamOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        from_attributes = True


class AddMember(BaseModel):
    student_code: str
    role: str # ctv hoặc tv
    

class AddMemberTeam(BaseModel):
    members: list[AddMember]
    team: Team


class KickMember(BaseModel):
    user_id: int


class KickMemberTeam(BaseModel):
    members: list[KickMember]
    team: Team


class UpdateRoleMember(BaseModel):
    user_id: int
    team_id: int
    role: str # 'tv' hoặc 'leader'


class DowngradeRoleMember(BaseModel):
    user_id: int
    team_id: int

    
class UserOut(User):
    id: int
    birthday: Datee

    class Config:
        orm_mode: True


class SelectMemberTeam(BaseModel):
    role_id: int
    team_id: int
    status: bool

    class Config:
        orm_mode: True

class SelectUserAll(BaseModel):
    id: int
    first_name: str
    last_name: str
    student_code: str
    class_code: str
    academic_year: int
    hometown: str
    birthday: Datee
    facebook_link: str
    email: EmailStr
    address: str
    phone: str
    is_active: bool
    sex: str
    member_teams: list[SelectMemberTeam]

    class Config:
        orm_mode = True
        from_attributes = True


class SelectUserByTeam(BaseModel):
    user: UserOut
    role: Role
    team: TeamOut

    class Config:
        orm_mode = True
        from_attributes = True


class UpdatePersonInfo(BaseModel):
    first_name: str
    last_name: str
    email: str
    student_code: str
    class_code: str
    academic_year: int
    hometown: str
    birthday: Datee
    facebook_link: str
    address: str
    phone: str
    is_active: bool
    sex: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: str | None


class Token(BaseModel): # dinh dang tra ra ma va kieu token trong ham tao ma token(login)
    access_token: str
    token_type: str


class PasswordU(BaseModel):
    old_password: str
    new_password: str