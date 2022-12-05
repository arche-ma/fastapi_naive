import strawberry
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from strawberry.fastapi import GraphQLRouter
from cruds.cart_cruds import check_cart_items, create_cart, get_cart_by_uuid
import models
from schema.mutations import Mutations
from schema.queries import Query
from db import SessionLocal, engine
from settings import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
origins = ["*"]

schema = strawberry.Schema(query=Query, mutation=Mutations)
app = FastAPI()
app.mount(
    settings.static_url,
    StaticFiles(directory=settings.static_dir),
    name="static",
)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def cart_middleware(request: Request, call_next):
    cart_uuid = request.cookies.get("cart_uuid", None)
    print("cart_uuid:", cart_uuid)
    if not cart_uuid or cart_uuid == "None":
        cart = create_cart()
    else:
        with SessionLocal() as session:
            cart = get_cart_by_uuid(cart_uuid, selections=["artworks"])
            if cart:
                cart = check_cart_items(cart)
            else:
                cart = create_cart()
            session.commit()
    cart_uuid = cart.uuid
    response = await call_next(request)
    response.set_cookie("cart_uuid", cart_uuid)
    print(request.cookies)
    return response
