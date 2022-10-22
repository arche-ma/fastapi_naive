from sqlalchemy import select

from db import SessionLocal
from models import Artwork
from serialize import get_data


def user_artworks(root):
    from scalars.artwork_type import ArtworkType

    db_session = SessionLocal()
    with db_session as session:
        sql = select(Artwork).where(Artwork.artist_id == root.id)
        results = session.execute(sql).scalars().all()
    result_list = [
        ArtworkType(**get_data(result, Artwork)) for result in results
    ]
    return result_list
