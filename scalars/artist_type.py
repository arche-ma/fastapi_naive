import base64
import binascii
from typing import TYPE_CHECKING

import strawberry
from strawberry import LazyType

from cruds.model_cruds import get_model_by_id
from models import Artist
from resolvers.artworks_by_id import user_artworks
from scalars.generic_input import GenericInput

if TYPE_CHECKING:
    import scalars
    from scalars.artwork_type import ArtworkType


@strawberry.type
class ArtistType:
    id: strawberry.ID
    first_name: str
    last_name: str
    patronymic: str
    bio: str | None
    image_url: str
    artworks: list[
        LazyType["ArtworkType", "scalars.artwork_type"]
    ] = strawberry.field(resolver=user_artworks)


@strawberry.input
class ArtistInput(GenericInput):
    first_name: str
    last_name: str
    patronymic: str
    image: str
    bio: str

    def validate_img(self):
        if self.image is None:
            return True
        try:
            image = base64.b64decode(self.image, validate=True)
            self.image = image
        except binascii.Error:
            raise Exception("Image error: Invalid base64 string")


@strawberry.input
class ArtistUpdateInput(ArtistInput):
    id: strawberry.ID
    image: str | None
    first_name: str | None = None
    last_name: str | None = None
    image: str | None = None
    patronymic: str = None
    bio: str | None = None

    def validate_id(self):
        artist = get_model_by_id(id=self.id, model=Artist)
        if not artist:
            raise Exception("Artist with such id doesn't exist")
        if not self.first_name:
            self.first_name = artist.first_name
        if not self.last_name:
            self.last_name = artist.last_name
        return True
