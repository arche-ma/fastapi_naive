import strawberry
from strawberry import LazyType

from models import Artwork, Cart
from resolvers.artworks_by_id import get_data

from .artwork_type import ArtworkType


@strawberry.type
class CartType:
    uuid: str
    artworks: list[LazyType["ArtworkType", "scalars.artwork_type"]]

    @classmethod
    def marshal(cls, model: Cart, selections: list[str]) -> "CartType":
        artworks = []
        if "artworks" in selections:
            artworks = [
                ArtworkType(**get_data(artwork, Artwork))
                for artwork in model.artworks
            ]
        instance = cls(uuid=model.uuid, artworks=artworks)
        return instance
