from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core.exceptions import error_messages


from app.api.v1.serializers.category import CategoryIn
from app.api.v1.models.category import Category
from app.api.v1.repositories.common import CRUD
from app.api.v1.serializers.user import UserIn


def create(req: CategoryIn, current_user: UserIn):
    try:
        req.name = req.name.lower()
        new_category = Category(**req.dict())
        operation = CRUD().add(new_category)
        return jsonable_encoder(new_category)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{str(e)}")


def delete(id: int, db: Session, current_user: UserIn):
    try:
        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise error_messages.CategoryNotFound
        db.delete(category)
        db.commit()
        return f"{category.name} is deleted"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="cannot delete category")


def get_all_categories(db: Session, current_user: UserIn):
    categories = db.query(Category).all()
    return jsonable_encoder(categories)
