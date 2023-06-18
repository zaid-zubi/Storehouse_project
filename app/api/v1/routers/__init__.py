from fastapi import APIRouter
from app.api.v1.views import (
    countries_router,
    beat_router,
    users_router,
    products_router,
    categories_router,
    favourite_router,
    user2_router,
)

api_router = APIRouter(prefix="/v1")
# api_router.include_router(countries_router, tags=["countries"], prefix="/countries/v1")
# api_router.include_router(beat_router, tags=["beat"])
api_router.include_router(users_router, tags=["auth"], prefix="/users")
api_router.include_router(products_router, tags=["products"], prefix="/products")
api_router.include_router(categories_router, tags=["category"], prefix="/categories")
api_router.include_router(favourite_router, tags=["favourite"], prefix="/favourites")
api_router.include_router(user2_router, tags=["user2"], prefix="/user2")
