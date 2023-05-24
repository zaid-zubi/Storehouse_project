from app.api.v1.serializers.category import CategoryIn
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from app.api.v1.models.category import Category
from app.api.v1.repositories.common import CRUD
from sqlalchemy.orm import Session
from core.exceptions import error_messages
from app.api.v1.serializers.user import UserIn


def create(req: CategoryIn, current_user: UserIn):
    if not req:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bad Request")
    name_with_underscore = req.name.replace(" ", "_")
    req.name = name_with_underscore
    new_category = Category(**req.dict())
    operation = CRUD().add(new_category)
    return jsonable_encoder(new_category)


def delete(category_name: str, db: Session, current_user: UserIn):
    category_name = category_name.upper()
    name_with_underscore = category_name.replace(" ", "_")
    category = db.query(Category).filter(Category.name == name_with_underscore).first()
    if not category:
        raise error_messages.CategoryNotFound
    db.delete(category)
    db.commit()
    return f"{category_name} is deleted"


def get_all_categories(db: Session, current_user: UserIn):
    categories = db.query(Category).all()
    return jsonable_encoder(categories)
