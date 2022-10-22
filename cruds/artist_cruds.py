from sqlalchemy import update
from sqlalchemy.orm import Session

from cruds.helpers import save_image
from cruds.model_cruds import get_model_by_id
from db import SessionLocal
from models import Artist
from scalars.artist_type import ArtistInput, ArtistUpdateInput


def create_artist(
    artist_input: ArtistInput, db_session: Session = SessionLocal()
) -> Artist:
    with db_session as session:
        artist_data = artist_input.to_dict()
        image = artist_data.pop("image")
        artist = Artist(**artist_data)
        session.add(artist)
        session.flush()
        session.refresh(artist)
        image_url = save_image(
            image,
            artist_id=artist.id,
            filename=f"{artist.first_name}_{artist.last_name}_id_{artist.id}",
        )
        artist.image_url = image_url
        session.commit()
        session.refresh(artist)
    return get_model_by_id(id=artist.id, model=Artist)


def update_artist(
    artist_input: ArtistUpdateInput, db_session: Session = SessionLocal()
) -> Artist:
    with db_session as session:
        update_data = artist_input.to_dict()
        pk = update_data.pop("id")
        image = update_data.pop("image", None)
        if image:
            first_name = update_data["first_name"]
            last_name = update_data["last_name"]
            update_data["image_url"] = save_image(
                image,
                artist_id=pk,
                filename=f"{first_name}_{last_name}_id_{pk}",
            )
        update_sql = (
            update(Artist).where(Artist.id == pk).values(**update_data)
        )
        session.execute(update_sql)
        session.commit()
    return get_model_by_id(id=pk, model=Artist)
