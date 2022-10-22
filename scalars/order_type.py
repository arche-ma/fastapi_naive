from enum import Enum
from typing import TYPE_CHECKING

import strawberry
from strawberry import LazyType

from models import Artwork, Customer, Order
from scalars.artwork_type import ArtworkType
from scalars.generic_input import GenericInput
from serialize import get_data

if TYPE_CHECKING:
    import scalars


@strawberry.enum
class OrderStatus(str, Enum):
    NEW = "NEW"
    ACCEPTED = "ACCEPTED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    CLOSED = "CLOSED"


@strawberry.type
class OrderType:
    id: strawberry.ID
    status: OrderStatus
    commentary: str | None
    customer: LazyType["CustomerType", "scalars.order_type"]
    artworks: list[LazyType["ArtworkType", "scalars.artwork_type"]]

    @classmethod
    def marshal(cls, selections: list[str], model: Order) -> "OrderType":
        customer = None
        artworks = []
        if "customer" in selections:
            customer = CustomerType.marshal(model.customer)
        if "artworks" in selections:
            artworks = [
                ArtworkType(**get_data(artwork.artwork, Artwork))
                for artwork in model.artworks
            ]
        instance = cls(
            id=strawberry.ID(str(model.id)),
            status=model.status.value,
            commentary=model.commentary,
            customer=customer,
            artworks=artworks,
        )
        return instance


@strawberry.type
class CustomerType:
    id: strawberry.ID
    first_name: str
    last_name: str
    phone: str
    address: str

    @classmethod
    def marshal(cls, model: Customer) -> "CustomerType":
        instance = cls(
            id=strawberry.ID(str(model.id)),
            first_name=model.first_name,
            last_name=model.last_name,
            phone=model.phone,
            address=model.address,
        )
        return instance


@strawberry.input
class CustomerInput(GenericInput):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    address: str | None = None


@strawberry.input
class OrderInput(GenericInput):
    status: OrderStatus | None = None
    commentary: str | None = None
