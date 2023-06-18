from app.api.v1.views.health_check import router as beat_router
from app.api.v1.views.countries import router as countries_router
from app.api.v1.views.user import router as users_router
from app.api.v1.views.product import router as products_router
from app.api.v1.views.category import router as categories_router
from app.api.v1.views.favourite import router as favourite_router
from app.api.v1.views.user2 import router as user2_router

__all__ = (
    "countries_router",
    "beat_router",
    "users_router",
    "products_router",
    "categories_router",
    "favourite_router",
    "user2_router",
)
