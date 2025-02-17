from fastapi import Depends, HTTPException, status
from ... import schemas, models, database, oauth2
from sqlalchemy.orm import session


async def selectAll(db: session = Depends(database.get_db)):
    users = db.query(models.Users).filter().all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='users not found!')
    return users


async def selectUserByTeam(id_team: schemas.Team, current_user: int = Depends(oauth2.get_current_user),
                           db: session = Depends(database.get_db)):
    #check xem id team có tồn tại
    team = db.query(models.Teams).filter(models.Teams.id == id_team.id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'team was not exist!')
    members = db.query(models.MemberTeams).filter(models.MemberTeams.team_id == id_team.id).all()
    if not members:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'There is no one in this team')
    return members
    # return [schemas.SelectUserByTeam.from_orm(member) for member in members]