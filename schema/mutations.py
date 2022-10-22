import strawberry
from sqlalchemy.orm.exc import NoResultFound
from strawberry.types import Info

from auth import issue_token, validate_password
from cruds import artist_cruds, artwork_cruds
from cruds.cart_cruds import add_items_to_cart
from cruds.order_cruds import (
    create_order,
    update_customer_by_id,
    update_order_by_id,
)
from cruds.user_cruds import get_user_by_username
from models import Artist, Artwork
from permissions.admin_permission import AdminPermission
from scalars.artist_type import ArtistInput, ArtistType, ArtistUpdateInput
from scalars.artwork_type import ArtworkInput, ArtworkType, ArtworkUpdate
from scalars.cart_type import CartType
from scalars.order_type import (
    CustomerInput,
    CustomerType,
    OrderInput,
    OrderType,
)
from scalars.validation_type import (
    AuthenticationFailed,
    TokenType,
    UserAuthResponse,
    UserInput,
    UserNotFound,
)
from schema.queries import Query
from serialize import get_data


@strawberry.type
class Mutations:
    @strawberry.mutation
    def create_order(
        self,
        commentary: str,
        cart_uuid: str,
        customer: CustomerInput,
        info: Info,
    ) -> OrderType:
        selections = Query.get_selected_fields(info)
        order = create_order(
            selections=selections,
            commentary=commentary,
            cart_uuid=cart_uuid,
            customer=customer,
        )
        representation = OrderType.marshal(selections, order)

        return representation

    @strawberry.mutation
    def add_to_cart(
        self, cart_uuid: str, artwork_ids: list[int], info: Info
    ) -> CartType:
        selections = Query.get_selected_fields(info)
        cart = add_items_to_cart(
            cart_uuid=cart_uuid, artwork_ids=artwork_ids, selections=selections
        )
        cart_output = CartType.marshal(cart, selections)
        return cart_output

    @strawberry.mutation(permission_classes=[AdminPermission])
    def update_customer(
        self, customer_id: strawberry.ID, customer: CustomerInput
    ) -> CustomerType:
        customer = update_customer_by_id(
            customer_id=int(customer_id), customer_input=customer
        )
        return CustomerType.marshal(customer)

    @strawberry.mutation(permission_classes=[AdminPermission])
    def update_order(
        self, order_id: strawberry.ID, order: OrderInput, info: Info
    ) -> OrderType:
        selections = Query.get_selected_fields(info)
        order = update_order_by_id(
            order_id=order_id, order_input=order, selections=selections
        )
        return OrderType.marshal(selections, order)

    @strawberry.mutation(permission_classes=[AdminPermission])
    def add_artwork(self, artwork_input: ArtworkInput) -> ArtworkType:
        artwork = artwork_cruds.add_artwork(artwork_input=artwork_input)
        return ArtworkType(**get_data(artwork, Artwork))

    @strawberry.mutation(permission_classes=[AdminPermission])
    def add_artist(self, artist_input: ArtistInput) -> ArtistType:
        artist = artist_cruds.create_artist(artist_input)
        return ArtistType(**get_data(artist, Artist))

    @strawberry.mutation(permission_classes=[AdminPermission])
    def update_artwork(self, artwork_input: ArtworkUpdate) -> ArtworkType:
        artwork = artwork_cruds.update_artwork(artwork_input=artwork_input)
        return ArtworkType(**get_data(artwork, Artwork))

    @strawberry.mutation(permission_classes=[AdminPermission])
    def update_artist(self, artist_input: ArtistUpdateInput) -> ArtistType:
        artist = artist_cruds.update_artist(artist_input)
        return ArtistType(**get_data(artist, Artist))

    @strawberry.mutation
    def authorize(self, user_input: UserInput) -> UserAuthResponse:

        try:
            user = get_user_by_username(user_input.username)
        except NoResultFound:
            return UserNotFound
        if not validate_password(user_input.password, user.hashed_password):
            return AuthenticationFailed
        return TokenType(token=issue_token(user))
