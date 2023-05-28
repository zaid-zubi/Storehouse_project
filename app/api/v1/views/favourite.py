from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from utils.http_response import http_response
from app.api.v1.repositories.common import CRUD
from app.api.v1.serializers.user import UserIn
from app.api.v1.views.user import get_current_user_from_token
from core.constants.response_messages import ResponseConstants
from app.api.v1.repositories.product import (
    add_to_favourite,
    get_favourite_products,
    remove_from_favourite,
)

router = APIRouter()


@router.post("/")
async def add_product_into_favourite_list(
    product_id: int,
    db=Depends(CRUD().db_conn),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    return http_response(
        message=ResponseConstants.CREATED_MSG,
        status=status.HTTP_200_OK,
        data=add_to_favourite(product_id, db, current_user),
    )


@router.get("/")
async def retrieve_list_favourite_products(
    db: Session = Depends(CRUD().db_conn),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    return http_response(
        message=ResponseConstants.RETRIEVED_MSG,
        status=status.HTTP_200_OK,
        data=get_favourite_products(db, current_user),
    )


@router.delete("/{product_id}")
async def delete_product_from_favourite(
    product_id: int,
    db: Session = Depends(CRUD().db_conn),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    return http_response(
        message=ResponseConstants.DELETED_MSG,
        status=status.HTTP_200_OK,
        data=remove_from_favourite(id=product_id, db=db, current_user=current_user),
    )


