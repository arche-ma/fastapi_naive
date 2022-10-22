from sqlalchemy import select, update
from sqlalchemy.orm import Session, joinedload, subqueryload
from sqlalchemy.util._collections import immutabledict

from db import SessionLocal
from models import Artwork, Cart, Customer, Order, OrderArtwork
from scalars.order_type import CustomerInput, OrderInput, OrderStatus


def get_subqueries(sql, selections: list[str]):
    if "customer" in selections:
        sql = sql.options(joinedload(Order.customer))
    if "artworks" in selections:
        sql = sql.options(
            subqueryload(Order.artworks).joinedload(OrderArtwork.artwork)
        )
    return sql


def get_order_by_id(
    id: int, selections: list[str], db_session: Session = SessionLocal()
) -> Order:
    with db_session as session:
        sql = select(Order).where(Order.id == id)
        sql = get_subqueries(sql, selections)
        order = session.execute(sql).scalars().first()
        return order


def get_all_orders(
    selections, db_session: Session = SessionLocal()
) -> list[Order]:
    with db_session as session:
        sql = select(Order)
        sql = get_subqueries(sql, selections)
        orders = session.execute(sql).scalars().all()
        return orders


def create_order(
    cart_uuid: str,
    customer: CustomerInput,
    selections: list[str],
    commentary: str = "",
    db_session: Session = SessionLocal(),
) -> Order:
    with db_session as session:
        order_customer = Customer(
            first_name=customer.first_name,
            last_name=customer.last_name,
            phone=customer.phone,
            address=customer.address,
        )
        order = Order(
            commentary=commentary, status="NEW", customer=order_customer
        )
        session.add(order)
        session.flush()
        session.refresh(order)
        cart: Cart = (
            session.execute(select(Cart).where(Cart.uuid == cart_uuid))
            .scalars()
            .first()
        )
        for artwork in cart.artworks:
            order_artwork = OrderArtwork(
                artwork_id=artwork.id, order_id=order.id
            )
            session.add(order_artwork)
        for artwork in cart.artworks:
            artwork.on_sale = False
        cart.artworks.clear()
        session.commit()
        session.refresh(order)
    order = get_order_by_id(id=order.id, selections=selections)
    return order


def update_customer_by_id(
    customer_id: int,
    customer_input: CustomerInput,
    db_session: Session = SessionLocal(),
) -> Customer:
    with db_session as session:
        session.execute(
            update(Customer)
            .where(Customer.id == int(customer_id))
            .values(**customer_input.to_dict())
        )
        session.commit()
        customer_query = select(Customer).where(Customer.id == customer_id)
        customer = session.execute(customer_query).scalar()
        return customer


def cancel_order_by_id(order_id, db_session: Session = SessionLocal()):
    with db_session as session:
        set_on_sale_query = (
            update(Artwork)
            .where(
                Artwork.id.in_(
                    select(OrderArtwork.artwork_id).where(
                        OrderArtwork.order_id == order_id
                    )
                )
            )
            .values(on_sale=True)
        )
        session.execute(
            set_on_sale_query,
            execution_options=immutabledict({"synchronize_session": "fetch"}),
        )
        change_order_status_query = (
            update(Order)
            .where(Order.id == order_id)
            .values(status=OrderStatus.CANCELLED)
        )
        session.execute(change_order_status_query)
        session.commit()
    return True


def update_order_by_id(
    order_id,
    order_input: OrderInput,
    selections: list[str],
    db_session: Session = SessionLocal(),
) -> Order:
    order_data = order_input.to_dict()
    status = order_data.get("status", None)
    if status == OrderStatus.CANCELLED:
        cancelled = cancel_order_by_id(order_id=order_id)
        if cancelled:
            return get_order_by_id(id=order_id, selections=selections)
    with db_session as session:
        session.execute(
            update(Order).where(Order.id == order_id).values(**order_data)
        )
        session.commit()
    order = get_order_by_id(id=order_id, selections=selections)
    return order
