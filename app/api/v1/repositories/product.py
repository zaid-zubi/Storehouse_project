from fastapi import HTTPException,status
from fastapi.encoders import jsonable_encoder
from utils.time import Time
from cloudinary import CloudinaryImage
from core.exceptions import error_messages
from core.constants.response_messages import ResponseConstants
from core.constants import strings
from app.api.v1.models import Product, Category, Favourite
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
        
        product_name = product.product_name
        product.active = False
        product.deleted_at = Time.currently_date_utcnow()
        db.add(product)
        db.commit()
        return ResponseConstants.DELETED_MSG
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")
    


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product not found")


def get_all(db: Session, current_user: UserIn):
    try:
        products = (
            db.query(Product)
            .filter(Product.product_creator == current_user["id"], Product.active == True)
            .all()
        )
        return jsonable_encoder(products) if products else "No product"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERRR, detail=f"{str(e)}")


def get_one(id: int, db: Session, current_user: UserIn):
    try:
        product = get_product_by_id(id, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product Id not existed!")
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


def create(req: ProductIn, current_user: UserIn):
    try:
        req.product_name = req.product_name.lower()
        product_dict = req.dict()
        product_dict["product_creator"] = current_user["id"]
        print(product_dict)
        new_product = Product(**product_dict)
        operation = CRUD().add(new_product)
        return jsonable_encoder(new_product)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Product data is not valid")


def get_product_by_id(id: int, db: Session):
    try:
        product = db.query(Product).filter(Product.id == id,Product.active == True).first()
        if not product:
            raise error_messages.ProductNotFound
        return product
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product doesn't exist")
        


def add_to_favourite(id: int, db: Session, current_user: UserIn):
    try:
        user = get_user(db, current_user["email"])
        product = get_product_by_id(id, db)
        favourite_dict = {"product_id": id, "user_id": user.id}
        if not product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Product not found")
        print(favourite_dict)
        new_favourite = Favourite(**favourite_dict)
        operation = CRUD().add(new_favourite)
        return jsonable_encoder(new_favourite)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Product doesn't exist")


def get_favourite_products(db: Session, current_user: UserIn):
    favourites = (
            db.query(Favourite)
            .filter(
                Favourite.user_id == get_user(db, current_user["email"]).id,
                Product.active == True
            )
            .all()
        )
    return jsonable_encoder(favourites) if favourites else strings.NO_PRODUCTS_IN_FAVOURITE_LIST


def remove_from_favourite(id: int, db: Session, current_user: UserIn):
    try:
        favourite_product = db.query(Favourite).filter(Favourite.product_id == id,Product.active == True).first()
        if not favourite_product:
            raise error_messages.ProductNotFound
        db.delete(favourite_product)
        db.commit()
        return ResponseConstants.DELETED_MSG
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product doesn't exist")


def show_product_image_from_cloudinary(
    product_id: id, db: Session, current_user: UserIn
):
    try:
        product = (
            db.query(Product)
            .filter(
                Product.id == product_id,Product.active == True,
                Product.product_creator
                == get_user(db, current_user["email"]).id,
            )
            .first()
        )
        if not product:
            raise error_messages.ProductNotFound
        print("Image URL:", product.image)
        return CloudinaryImage(product.image).build_url(width=600, height=500, crop="fill")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Photo not found")
