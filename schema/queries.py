import strawberry
from strawberry.types import Info

from cruds.cart_cruds import get_cart_by_uuid
from cruds.model_cruds import get_model_by_id, get_models_list
from cruds.order_cruds import get_all_orders, get_order_by_id
from models import Artist, Artwork
from scalars.artist_type import ArtistType
from scalars.artwork_type import ArtworkType
from scalars.cart_type import CartType
from scalars.order_type import OrderType
from serialize import get_data


@strawberry.type
class Query:
    @classmethod
    def get_selected_fields(cls, info: Info):
        selections = [
            selection.name
            for field in info.selected_fields
            for selection in field.selections
        ]
        return selections

    @strawberry.field
    def all_artists(self, info: Info) -> list[ArtistType]:
        artists = get_models_list(Artist)
        artists_data = []
        for artist in artists:
            artist_dict = get_data(artist, Artist)
            artists_data.append(ArtistType(**artist_dict))
        return artists_data

    @strawberry.field
    def all_artworks(self) -> list[ArtworkType]:
        artworks = get_models_list(Artwork)
        artwork_data = []
        for artwork in artworks:
            artwork_dict = get_data(artwork, Artwork)
            artwork_data.append(ArtworkType(**artwork_dict))
        return artwork_data

    @strawberry.field
    def get_cart(self, uuid: str, info: Info) -> CartType:
        selections = Query.get_selected_fields(info)
        cart = get_cart_by_uuid(uuid, selections)
        return CartType.marshal(cart, selections)

    @strawberry.field
    def artwork_by_id(self, id: strawberry.ID) -> ArtworkType:
        artwork_model = get_model_by_id(model=Artwork, id=id)
        if artwork_model:
            return ArtworkType(**get_data(artwork_model, Artwork))
        return None

    @strawberry.field
    def artist_by_id(self, artist_id: strawberry.ID) -> ArtistType:
        artist_model = get_model_by_id(model=Artist, id=int(artist_id))
        if artist_model:
            return ArtistType(**get_data(artist_model, Artist))
        return None

    @strawberry.field
    def all_orders(self, info: Info) -> list[OrderType]:
        selections = Query.get_selected_fields(info)
        orders = get_all_orders(selections)
        return [OrderType.marshal(selections, order) for order in orders]

    @strawberry.field
    def order_by_id(self, id: strawberry.ID, info: Info) -> OrderType:
        selections = Query.get_selected_fields(info)
        order = get_order_by_id(id, selections)
        if order:
            return OrderType.marshal(selections, order)
        return None
