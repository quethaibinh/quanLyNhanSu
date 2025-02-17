from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base


class Date(Base):
    __tablename__ = "date"

    id = Column(Integer, primary_key=True, nullable=False)
    day = Column(Integer, nullable=False)
    mon = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)

    user = relationship("Users", back_populates="birthday", foreign_keys="Users.birth_date_id")


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    class_code = Column(String, nullable=False)
    student_code = Column(String, nullable=False)
    academic_year = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    facebook_link = Column(String, nullable=False)
    address = Column(String, nullable=False)
    hometown = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
    birth_date_id = Column(Integer, ForeignKey("date.id", ondelete="CASCADE"), nullable=False)
    role_code = Column(String, nullable=False)

    authentication = relationship("Authentications", back_populates="user", uselist=False)
    birthday = relationship("Date", back_populates="user")
    member_teams = relationship("MemberTeams", back_populates="user")


class Authentications(Base):
    __tablename__ = "authentications"

    id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    user = relationship("Users", back_populates="authentication")


class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False)
    detail = Column(String, nullable=False)

    member_teams = relationship("MemberTeams", back_populates="role")


class Teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    member_teams = relationship("MemberTeams", back_populates="team")


class MemberTeams(Base):
    __tablename__ = "member_teams"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    status = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))

    user = relationship("Users", back_populates="member_teams")
    role = relationship("Roles", back_populates="member_teams")
    team = relationship("Teams", back_populates="member_teams")
