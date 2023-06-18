from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.v1.models.product import Favourite, Product
from app.api.v1.serializers.user import UserIn
from app.api.v1.repositories.common import CRUD
from app.api.v1.repositories.product import get_product_by_id
from app.api.v1.dependancies.authorization import *
from core.constants import strings
from core.constants.response_messages import ResponseConstants


def product_in_favourite(id: int, db: Session):
    product = db.query(Product).filter(Favourite.product_id == id).first()
    if not product:
        return False
    else:
        return True


def add_to_favourite(id: int, db: Session, current_user: UserIn):
    user = get_user(db, current_user["email"])
    product = get_product_by_id(id, db)
    if product_in_favourite(id, db):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The product already in favourite list",
        )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product not found"
        )
    favourite_dict = {"product_id": id, "user_id": user.id}

    print(favourite_dict)
    new_favourite = Favourite(**favourite_dict)
    operation = CRUD().add(new_favourite)
    return jsonable_encoder(new_favourite)


def get_favourite_products(db: Session, current_user: UserIn):
    favourites = (
        db.query(Favourite)
        .filter(
            Favourite.user_id == get_user(db, current_user["email"]).id,
            Product.active == True,
        )
        .all()
    )
    return (
        jsonable_encoder(favourites)
        if favourites
        else strings.NO_PRODUCTS_IN_FAVOURITE_LIST
    )


def remove_from_favourite(id: int, db: Session, current_user: UserIn):
    try:
        favourite_product = (
            db.query(Favourite)
            .filter(Favourite.product_id == id, Product.active == True)
            .first()
        )
        if not favourite_product:
            raise error_messages.ProductNotFound
        db.delete(favourite_product)
        db.commit()
        return ResponseConstants.DELETED_MSG
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product doesn't exist"
        )
