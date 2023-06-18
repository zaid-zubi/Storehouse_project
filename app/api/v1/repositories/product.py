from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from utils.time import Time
from cloudinary import CloudinaryImage
from core.exceptions import error_messages
from core.constants.response_messages import ResponseConstants
from core.constants import strings
from app.api.v1.models import Product, Category
from app.api.v1.serializers.product import ProductIn, UpdateProductPart
from app.api.v1.dependancies.authorization import *


def delete(product_id: int, db: Session, current_user: UserIn):
    try:
        product = (
            db.query(Product)
            .filter(
                Product.id == product_id,
                Product.active == True,
                Product.product_creator
                == get_user(db, current_user["email"].lower()).id,
            )
            .first()
        )

        product.active = False
        product.deleted_at = Time.currently_date_utcnow()
        db.add(product)
        db.commit()
        return ResponseConstants.DELETED_MSG
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )


def update(product_id: int, req: UpdateProductPart, db: Session, current_user: UserIn):
    try:
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
        return jsonable_encoder(product)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product not found"
        )


def get_all(db: Session, current_user: UserIn):
    products = (
        db.query(Product)
        .filter(Product.product_creator == current_user["id"], Product.active == True)
        .all()
    )
    res = []
    for product in products:
        product = jsonable_encoder(product)
        res.append(Product(**product))
    return jsonable_encoder(res)


def get_one(id: int, db: Session, current_user: UserIn):
    try:
        product = get_product_by_id(id, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Product Id not existed!"
        )
    return jsonable_encoder(product)


def get_all_by_category(category_id: int, db: Session, current_user: UserIn):
    category_x = db.query(Category).filter(Category.id == category_id).first()

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
        return strings.NO_PRODUCTS_FOR_DISPLAY
    return jsonable_encoder(products)


def create(req: ProductIn, current_user):
    req.product_name = req.product_name.lower()
    product_dict = req.dict()
    product_dict["product_creator"] = current_user["id"]
    print(product_dict)
    new_product = Product(**product_dict)
    try:
        operation = CRUD().add(new_product)
    except:
        raise ValueError("Error")
    return jsonable_encoder(new_product)


def get_username_by_id(id: int, db: Session):
    username = db.query(User.username).filter(User.id == id).first()
    return username


def get_product_by_id(id: int, db: Session):
    # product with username
    try:
        product = (
            db.query(
                Product.product_name,
                Product.id,
                Product.description,
                Product.price,
                Product.quantity,
                Product.product_creator,
            )
            .filter(Product.id == id, Product.active == True)
            .first()
        )

        if not product:
            raise error_messages.ProductNotFound

        data = dict(product)
        data.update(get_username_by_id(product["product_creator"], db))
        data.pop("product_creator")
        return data
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product doesn't exist"
        )


def show_product_image_from_cloudinary(
    product_id: id, db: Session, current_user: UserIn
):
    try:
        product = (
            db.query(Product)
            .filter(
                Product.id == product_id,
                Product.active == True,
                Product.product_creator == get_user(db, current_user["email"]).id,
            )
            .first()
        )
        if not product:
            raise error_messages.ProductNotFound
        print("Image URL:", product.image)
        return CloudinaryImage(product.image).build_url(
            width=600, height=500, crop="fill"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo not found"
        )
