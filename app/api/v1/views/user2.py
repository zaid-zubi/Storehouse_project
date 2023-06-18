from fastapi import APIRouter, Depends, status
from app.api.v1.repositories.common import CRUD
from app.api.v1.repositories.user2 import get_product_data


router = APIRouter()


@router.get("/user2/{id}")
async def get_user2(id: int, db=Depends(CRUD().db_conn)):
    return get_product_data(id, db)
