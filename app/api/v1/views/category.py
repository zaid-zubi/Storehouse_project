from fastapi import APIRouter, status
from utils.http_response import http_response
from core.constants.response_messages import ResponseConstants
from app.api.v1.dependancies.authorization import *
from app.api.v1.serializers.category import CategoryIn
from app.api.v1.repositories.category import create, delete, get_all_categories
from app.api.v1.views.user import get_current_user_from_token

router = APIRouter(prefix="")
create_response_list = [
    ResponseConstants.CREATED_MSG["en"],
    ResponseConstants.CREATED_MSG["ar"],
]
delete_response_list = [
    ResponseConstants.DELETED_MSG["en"],
    ResponseConstants.DELETED_MSG["ar"],
]


@router.get("/")
async def retrieve_all_categories(
    db: Session = Depends(CRUD().db_conn),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    return http_response(
        message=ResponseConstants.RETRIEVED_MSG,
        status=status.HTTP_200_OK,
        data=get_all_categories(db, current_user),
    )


@router.post("/")
async def add_category(
    req: CategoryIn, current_user: UserIn = Depends(get_current_user_from_token)
):
    return http_response(
        message=create_response_list,
        status=status.HTTP_201_CREATED,
        data=create(req, current_user),
    )


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db=Depends(CRUD().db_conn),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    return http_response(
        message=delete_response_list,
        status=status.HTTP_200_OK,
        data=delete(category_id, db, current_user),
    )
