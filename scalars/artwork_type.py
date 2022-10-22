import base64
import binascii
from decimal import Decimal
from typing import TYPE_CHECKING

import strawberry
from strawberry import LazyType

from cruds.model_cruds import get_model_by_id
from models import Artist, Artwork
from resolvers.artists import get_artist
from scalars.generic_input import GenericInput

if TYPE_CHECKING:
    import scalars
    from scalars.artist_type import ArtistType


@strawberry.type
class ArtworkType:
    id: strawberry.ID
    artist_id: int
    title: str
    description: str
    price: Decimal
    on_sale: bool
    image_url: str | None
    artist: LazyType["ArtistType", "scalars.artist_type"] = strawberry.field(
        resolver=get_artist
    )


@strawberry.input
class ArtworkInput(GenericInput):
    artist_id: int
    title: str
    description: str
    price: Decimal
    on_sale: bool
    image: str

    def validate_price(self):
        if self.price is not None and self.price <= 0:
            raise Exception("price should be bigger than 0")
        return

    def validate_artist(self):
        if self.artist_id is None:
            return True
        artist = get_model_by_id(id=self.artist_id, model=Artist)
        if not artist:
            raise Exception("artist with given id doesn't exist")
        return True

    def validate_img(self):
        if self.image is None:
            return True
        try:
            image = base64.b64decode(self.image, validate=True)
            self.image = image
        except binascii.Error:
            raise Exception("Image error: Invalid base64 string")


@strawberry.input
class ArtworkUpdate(ArtworkInput):
    id: strawberry.ID
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    image: str | None = None
    on_sale: bool | None = None
    artist_id: int | None = None

    def validate_id(self):
        artwork = get_model_by_id(id=self.id, model=Artwork)
        if not artwork:
            raise Exception("artwork with given id doesn't exist")
        if not self.title:
            self.title = artwork.title
        if not self.artist_id:
            self.artist_id = artwork.artist_id
        return True
