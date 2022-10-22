from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from db import SessionLocal
from models import Artwork, Cart


def get_subqueryload(sql, selections: list[str]):
    if "artworks" in selections:
        sql = sql.options(joinedload(Cart.artworks))
    return sql


def get_cart_by_uuid(
    uuid: str, selections: list[str], db_session: Session = SessionLocal()
) -> Cart:
    with db_session as session:
        sql = select(Cart).where(uuid == Cart.uuid)
        sql = get_subqueryload(sql, selections)
        cart = session.execute(sql).scalar()
    return cart


def add_items_to_cart(
    cart_uuid: str,
    artwork_ids: list[int],
    selections: list[str],
    db_session: Session = SessionLocal(),
) -> Cart:
    with db_session as session:
        sql = select(Cart).where(Cart.uuid == cart_uuid)
        cart: Cart = session.execute(sql).scalars().first()
        sql = select(Artwork).where(
            Artwork.id.in_(artwork_ids), Artwork.on_sale
        )
        artworks = session.execute(sql).scalars().all()
        cart.artworks.clear()
        cart.artworks.extend(artworks)
        session.commit()
        session.refresh(cart)
    cart = get_cart_by_uuid(uuid=cart.uuid, selections=selections)
    return cart


def create_cart(db_session: Session = SessionLocal()) -> Cart:
    with db_session as session:
        cart = Cart()
        session.add(cart)
        session.flush()
        session.commit()
        session.refresh(cart)
    return cart


def check_cart_items(cart: Cart, db_session: Session = SessionLocal()) -> Cart:
    with db_session as session:
        cart.artworks = [
            artwork for artwork in cart.artworks if artwork.on_sale
        ]
        session.commit()
    return cart
