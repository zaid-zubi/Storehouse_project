from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api.v1.models.product import Product
from app.api.v1.models.user import User

# This is file for example and apply any new idea


def get_product_data(id: int, db: Session):
    product = (
        db.query(
            Product.user,
            Product.product_name,
            Product.product_creator,
            Product.price,
        )
        .filter(Product.id == id)
        .first()
    )

    data = dict(product)
    data.update(get_username_by_id(product["product_creator"], db))
    data.pop("product_creator")

    return jsonable_encoder(data)


def get_username_by_id(id: int, db: Session):
    username = db.query(User.username).filter(User.id == id).first()
    return username
