import strawberry
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter

import models
from db import SessionLocal, engine
from schema.mutations import Mutations
from schema.queries import Query
from settings import settings

models.Base.metadata.create_all(bind=engine)
schema = strawberry.Schema(query=Query, mutation=Mutations)

app = FastAPI()
app.mount(
    settings.static_url,
    StaticFiles(directory=settings.static_dir),
    name="static",
)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


@app.middleware("http")
async def cart_middleware(
    request: Request,
    call_next,
    db_session: Session = SessionLocal(),
):
    cart_uuid = request.cookies.get("cart_uuid", None)
    print("cart_uuid:", cart_uuid)
    if not cart_uuid:
        with db_session as session:
            cart = models.Cart()
            session.add(cart)
            session.flush()
            cart_uuid = cart.uuid
            session.commit()
    response = await call_next(request)
    response.set_cookie("cart_uuid", cart_uuid)
    print(request.cookies)
    return response
