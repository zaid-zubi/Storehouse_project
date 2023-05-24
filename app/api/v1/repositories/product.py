import random
from app.api.v1.models import Product, Category, Favourite
from app.api.v1.serializers.product import ProductIn, UpdateProductPart
from fastapi.encoders import jsonable_encoder
from app.api.v1.dependancies.authorization import *
from utils.time import Time
from core.exceptions import error_messages
from core.constants.response_messages import ResponseConstants
from core.settings.cloudinary import *
from cloudinary import CloudinaryImage
from utils.generate_random_code import RandomNumBillion


def delete(product_id: int, db: Session, current_user: UserIn):
    product = (
        db.query(Product)
        .filter(
            Product.id == product_id,
            Product.active == True,
            Product.product_creator
            == get_user_by_name(db, current_user["username"]).id,
        )
        .first()
    )

    if not product:
        raise error_messages.ProductNotFound

    product_name = product.product_name
    product.active = False
    product.deleted_at = Time.currently_date_utcnow()
    db.add(product)
    db.commit()
    return ResponseConstants.DELETED_MSG


def update(product_id: int, req: UpdateProductPart, db: Session, current_user: UserIn):
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.active == True)
        .first()
    )

    if not product:
        raise error_messages.ProductNotFound

    new_data = req.dict(exclude_none=True)
    new_data.update({"product_creator": current_user["id"]})
    for key, value in new_data.items():
        setattr(product, key, value)
        print(key, value)
    db.add(product)
    db.commit()
    db.refresh(product)
    return ResponseConstants.CREATED_MSG


def get_all(db: Session, current_user: UserIn):
    products = (
        db.query(Product)
        .filter(Product.product_creator == current_user["id"], Product.active == True)
        .all()
    )
    return jsonable_encoder(products) if products else "No product"


def get_one(name: str, db: Session, current_user: UserIn):
    product = get_product_by_name(name, db)
    return jsonable_encoder(product)


def get_all_by_category(category: str, db: Session, current_user: UserIn):
    category = category.upper()
    category_x = db.query(Category).filter(Category.name == category).first()
    if not category_x:
        raise error_messages.CategoryNotFound

    products = (
        db.query(Product)
        .filter(
            Product.category_id == category_x.id,
            Product.product_creator == current_user["id"],
            Product.active == True,
        )
        .all()
    )
    if not products:
        raise error_messages.ProductNotFound
    return jsonable_encoder(products)


def create(req: ProductIn, current_user: UserIn):
    product_dict = req.dict()
    product_dict["product_creator"] = current_user["id"]
    print(product_dict)
    new_product = Product(**product_dict)
    operation = CRUD().add(new_product)
    return jsonable_encoder(new_product)


def get_product_by_id(id: int, db: Session):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise error_messages.ProductNotFound
    return product


def get_product_by_name(name: str, db: Session):
    product = db.query(Product).filter(Product.product_name == name).first()
    if not product:
        raise error_messages.ProductNotFound
    return product


def add_to_favourite(id: int, db: Session, current_user: UserIn):
    user = get_user_by_name(db, current_user["username"])
    product = get_product_by_id(id, db)
    favourite_dict = {"product_id": id, "user_id": user.id}
    print(favourite_dict)
    new_favourite = Favourite(**favourite_dict)
    operation = CRUD().add(new_favourite)
    return jsonable_encoder(new_favourite)


def get_favourite_products(db: Session, current_user: UserIn):
    favourites = (
        db.query(Favourite)
        .filter(
            Favourite.user_id == get_user_by_name(db, current_user["username"]).id,
        )
        .all()
    )

    return jsonable_encoder(favourites) if favourites else "Empty List"


def remove_from_favourite(id: int, db: Session, current_user: UserIn):
    favourite_product = db.query(Favourite).filter(Favourite.product_id == id).first()
    if not favourite_product:
        raise error_messages.ProductNotFound
    db.delete(favourite_product)
    db.commit()
    return ResponseConstants.DELETED_MSG


def show_product_image_from_cloudinary(
    product_name: str, db: Session, current_user: UserIn
):
    if not current_user:
        raise error_messages.UnAuthorizedUser
    product = (
        db.query(Product)
        .filter(
            Product.product_name == product_name,
            Product.product_creator
            == get_user_by_name(db, current_user["username"]).id,
        )
        .first()
    )
    if not product:
        raise error_messages.ProductNotFound
    print("Image URL:", product.image)
    return CloudinaryImage(product.image).build_url(width=600, height=500, crop="fill")
