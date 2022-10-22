from sqlalchemy import select
from sqlalchemy.orm import Session

from db import Base, SessionLocal


def get_models_list(
    model: Base, db_session: Session = SessionLocal()
) -> list[Base]:
    with db_session as session:
        artists = session.execute(select(model)).scalars().all()
    return artists


def get_model_by_id(
    id: int, model: Base, db_session: Session = SessionLocal()
) -> Base:
    with db_session as session:
        sql = select(model).where(model.id == id)
        model = session.execute(sql).scalar()
    return model
