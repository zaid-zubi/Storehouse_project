from fastapi import APIRouter, status, Depends
from app.api.v1.repositories import country
from app.api.v1.repositories.common import CRUD
from app.api.v1.serializers.country import CountryConfSchema, CountryConfOptionalSch, CountryConfGetSchema, \
    CountryResponseModel
from integrations.aws_queue.pusher import Pusher
from utils.http_response import http_response
from core.constants.response_messages import ResponseConstants
# from fastapi_versioning import version

router = APIRouter(
    prefix='',
    tags=["countries"]
)


@router.get("", response_model=CountryResponseModel)
def get_all_countries(db=Depends(CRUD().db_conn)):
    return http_response(data=country.get_all(db), message=ResponseConstants.RETRIEVED,
                         status=status.HTTP_200_OK)


@router.post("", response_model=CountryConfSchema)
def create_country_configuration(request: CountryConfSchema, db=Depends(CRUD().db_conn)):
    """
     This is a quick test to know how to push message to sns
    """
    Pusher.push_country_configurations_to_sns("""{
        "data": [{
            "country": "JO"
        }]
    }""")
    return http_response(data=country.create(request), message=ResponseConstants.CREATED,
                         status=status.HTTP_201_CREATED)


@router.delete("/{alpha_2}", status_code=status.HTTP_204_NO_CONTENT)
def delete(alpha_2: str, db=Depends(CRUD().db_conn)):
    country.destroy(alpha_2, db)
    return http_response(data=[],
                         message=ResponseConstants.DELETED,
                         status=status.HTTP_204_NO_CONTENT)


@router.get("/{alpha_2}", response_model=CountryConfGetSchema, status_code=status.HTTP_200_OK)
def get_country(alpha_2: str, db=Depends(CRUD().db_conn)):
    return http_response(data=country.show_detail(alpha_2, db),
                         message=ResponseConstants.RETRIEVED,
                         status=status.HTTP_200_OK)


@router.patch("/{alpha_2}", status_code=status.HTTP_202_ACCEPTED)
def update(alpha_2: str, request: CountryConfOptionalSch, db=Depends(CRUD().db_conn)):
    return http_response(data=country.patch(alpha_2, request, db),
                         message=ResponseConstants.RETRIEVED,
                         status=status.HTTP_200_OK)
