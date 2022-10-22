from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from db import SessionLocal
from models import User


def get_user_by_username(
    username: str, db_session: Session = SessionLocal()
) -> User:
    with db_session as session:
        sql = select(User).where(User.username == username)
        user = session.execute(sql).scalar()
        if not user:
            raise NoResultFound("user with given username doesn't exist")
        return user
