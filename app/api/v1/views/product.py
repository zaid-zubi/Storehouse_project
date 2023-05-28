from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse
from utils.http_response import http_response
from app.api.v1.repositories.product import *
from app.api.v1.dependancies.authorization import *
from app.api.v1.serializers.product import ProductIn, UpdateProductPart
from app.api.v1.views.user import get_current_user_from_token
from core.constants.response_messages import ResponseConstants

router = APIRouter(prefix="", tags=["products"])


@router.post("/")
async def add_product(
    product=Depends(ProductIn.as_form),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    """
Try to use postman, don't forget to use token
    """
    return http_response(
        message=ResponseConstants.CREATED_MSG,
        status=status.HTTP_201_CREATED,
        data=create(product, current_user),
    )


@router.patch("/{product_id}")
async def update_product(
    product_id: int,
    req: UpdateProductPart,
    db=Depends(CRUD().db_conn),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    return http_response(
        message=ResponseConstants.UPDATED_MSG,
        status=status.HTTP_201_CREATED,
        data=update(product_id, req, db, current_user),
    )


@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db=Depends(CRUD().db_conn),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    return http_response(
        message=ResponseConstants.DELETED_MSG,
        status=status.HTTP_200_OK,
        data=delete(product_id, db, current_user),
    )


@router.get("/")
async def retrieve_products(
    product_id: int = None,
    db=Depends(CRUD().db_conn),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    if not product_id:
        return http_response(
            message=ResponseConstants.RETRIEVED_MSG,
            status=status.HTTP_200_OK,
            data=get_all(db, current_user),
        )
    return http_response(
        message=ResponseConstants.RETRIEVED_MSG,
        status=status.HTTP_200_OK,
        data=get_one(product_id, db, current_user),
    )


@router.get("/category/{category}")
async def retrieve_user_products(
    category: int | None = None,
    db=Depends(CRUD().db_conn),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    if not category:
        return http_response(
            message=ResponseConstants.RETRIEVED_MSG,
            status=status.HTTP_200_OK,
            data=get_all(db,current_user),
        )
    else:
        return http_response(message=ResponseConstants.RETRIEVED_MSG,status=status.HTTP_200_OK,data=get_all_by_category(category, db, current_user))
    


@router.get("/{product_id}/image", response_class=RedirectResponse)
async def show_image(
    product_id: int,
    db: Session = Depends(CRUD().db_conn),
    current_user: UserIn = Depends(get_current_user_from_token),
):
    return show_product_image_from_cloudinary(product_id, db, current_user)
