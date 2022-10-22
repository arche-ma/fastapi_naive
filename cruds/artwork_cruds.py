from sqlalchemy import update
from sqlalchemy.orm import Session

from cruds.helpers import save_image
from cruds.model_cruds import get_model_by_id
from db import SessionLocal
from models import Artwork
from scalars.artwork_type import ArtworkInput, ArtworkUpdate


def add_artwork(
    artwork_input: ArtworkInput,
    db_session: Session = SessionLocal(),
) -> Artwork:
    with db_session as session:
        artwork_data = artwork_input.to_dict()
        image = artwork_data.pop("image")
        image = save_image(
            image,
            artist_id=artwork_data["artist_id"],
            filename=artwork_data["title"],
        )
        artwork = Artwork(**artwork_data, image_url=image)
        session.add(artwork)
        session.commit()
        session.refresh(artwork)
    artwork = get_model_by_id(id=artwork.id, model=Artwork)
    return artwork


def update_artwork(
    artwork_input: ArtworkUpdate,
    db_session: Session = SessionLocal(),
):
    update_data = artwork_input.to_dict()
    image = update_data.pop("image", None)
    artwork_id = update_data.pop("id")
    artist_id = update_data.get("artist_id")
    title = update_data.get("title")

    if image:
        update_data["image_url"] = save_image(
            image, artist_id=artist_id, filename=title
        )

    with db_session as session:
        session.execute(
            update(Artwork)
            .where(Artwork.id == artwork_id)
            .values(**update_data)
        )
        session.commit()
    artwork = get_model_by_id(id=artwork_id, model=Artwork)
    return artwork
