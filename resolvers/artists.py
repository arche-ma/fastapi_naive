from sqlalchemy import select

from db import SessionLocal
from models import Artist
from serialize import get_data


def get_artist(root):
    from scalars.artist_type import ArtistType

    db_session = SessionLocal()
    with db_session as session:
        sql = select(Artist).where(Artist.id == root.artist_id)
        result = session.execute(sql).scalars().first()

    result = ArtistType(**get_data(result, Artist))
    return result
