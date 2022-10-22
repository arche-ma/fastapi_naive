import enum
import uuid

from sqlalchemy import (Boolean, Column, Enum, ForeignKey, Integer, Numeric,
                        String, Table, Text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from db import Base


class OrderStatus(enum.Enum):
    NEW = "NEW"
    ACCEPTED = "ACCEPTED"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    CLOSED = "CLOSED"


cart_table = Table(
    "user_carts",
    Base.metadata,
    Column("arworks_id", ForeignKey("artworks.id")),
    Column("carts_id", ForeignKey("carts.uuid")),
)

tag_table = Table(
    "tag_artworks",
    Base.metadata,
    Column("tags_id", ForeignKey("tags.id")),
    Column("artworks_id", ForeignKey("artworks.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    patronymic = Column(String, nullable=True)
    bio = Column(Text)
    image_url = Column(String)

    artworks = relationship("Artwork", back_populates="artist")


class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    title = Column(String)
    description = Column(Text)
    on_sale = Column(Boolean, default=True, nullable=False)
    price = Column(Numeric(12, 2))
    image_url = Column(String)
    artist = relationship("Artist", back_populates="artworks")
    tags = relationship(
        "Tag", back_populates="artworks", secondary="tag_artworks"
    )


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    slug = Column(String)
    artworks = relationship(
        "Artwork", back_populates="tags", secondary="tag_artworks"
    )


class Cart(Base):
    __tablename__ = "carts"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    artworks = relationship("Artwork", secondary=cart_table)


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    address = Column(Text)
    order = relationship("Order", back_populates="customer", uselist=False)


class OrderArtwork(Base):
    __tablename__ = "order_artwork"
    __table_args__ = (
        UniqueConstraint("artwork_id", name="one_item_for_order"),
    )
    id = Column(Integer, primary_key=True, index=True)
    artwork_id = Column(Integer, ForeignKey("artworks.id"), unique=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", back_populates="artworks")
    artwork = relationship("Artwork")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(Enum(OrderStatus))
    commentary = Column(Text)
    artworks = relationship("OrderArtwork", back_populates="order")
    customer = relationship("Customer", back_populates="order")
