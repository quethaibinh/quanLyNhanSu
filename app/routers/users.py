from fastapi import APIRouter, Depends, status, UploadFile, File
from .. import schemas, database, oauth2
from sqlalchemy.orm import session

from ..repo.repo_user import changeRole, createUser, createUserByExcel, selectUser, addMemberTeam, updatePersonalInfo, kickMemberTeam, updatePassword

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_users(user: schemas.UserCreate, db: session = Depends(database.get_db)):
    return await createUser.create_user(user, db)
    

@router.post("/upload_excel/")
async def upload_excel(file: UploadFile = File(...), db: session = Depends(database.get_db)):
    return await createUserByExcel.upload_excel(file, db)

@router.get("/select_all", response_model=list[schemas.SelectUserAll])
async def select_user_all(db: session = Depends(database.get_db)):
    return await selectUser.selectAll(db)

@router.post("/select_by_team_id", response_model=list[schemas.SelectUserByTeam])
async def select_user_by_team(team_id: schemas.Team, current_user: int = Depends(oauth2.get_current_user),
                              db: session = Depends(database.get_db)):
    return await selectUser.selectUserByTeam(team_id, current_user, db)

@router.post("/add_member_team")
async def add_member_team(add_member: schemas.AddMemberTeam,
                            current_user: int = Depends(oauth2.get_current_user),
                            db: session = Depends(database.get_db)):
    return await addMemberTeam.add_member(add_member.members, add_member.team, current_user, db)

@router.put("/kick_member_team")
async def kick_member_team(kick_member: schemas.KickMemberTeam,
                     current_user: int = Depends(oauth2.get_current_user),
                     db: session = Depends(database.get_db)):
    return await kickMemberTeam.kick_member(kick_member.members, kick_member.team, current_user, db)

@router.put("/update_role")
async def update_role(role: schemas.UpdateRoleMember,
                      current_user: int = Depends(oauth2.get_current_user),
                      db: session = Depends(database.get_db)):
    return await changeRole.update_role(role, current_user, db)

@router.put("/downgrade_role")
async def downgrade_role(downgrade: schemas.DowngradeRoleMember,
                         current_user: int = Depends(oauth2.get_current_user),
                         db: session = Depends(database.get_db)):
    return await changeRole.downgrade_role(downgrade, current_user, db)

@router.put("/update_personal_info")
async def update_personal_info(info_update: schemas.UpdatePersonInfo,
                              current_user: int = Depends(oauth2.get_current_user),
                              db: session = Depends(database.get_db)):
    return await updatePersonalInfo.update_person_info(info_update, current_user, db)

@router.put("/update_password")
async def update_password(password: schemas.PasswordU,
                          current_user: int = Depends(oauth2.get_current_user),
                          db: session = Depends(database.get_db)):
    return await updatePassword.update_password(password, current_user, db)

@router.get("/get_personal_info", response_model= schemas.SelectUserAll)
async def get_personal_info(current_user: int = Depends(oauth2.get_current_user),
                            db: session = Depends(database.get_db)):
    return current_user