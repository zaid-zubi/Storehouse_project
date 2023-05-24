from fastapi import APIRouter, Depends

from app.api.v1.repositories.common import CRUD
from core.constants.response_messages import ResponseConstants
from core.mongo.mongo_db import get_mongo_database
from utils.http_response import http_response

router = APIRouter()


@router.get('/beat')
def health_check(db=Depends(CRUD().db_conn), mongo_db=Depends(get_mongo_database())):
    return http_response(message=ResponseConstants.RETRIEVED, status=200)
