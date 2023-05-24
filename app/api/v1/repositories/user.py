from app.api.v1.dependancies.authorization import *
from fastapi.encoders import jsonable_encoder
from app.api.v1.serializers.user import UserIn
from app.api.v1.dependancies.hash import Hasher


def create(request: UserIn):
    request.password = Hasher().get_password_hash(request.password)
    new_user = User(**request.dict())
    operation = CRUD().add(new_user)
    return jsonable_encoder(new_user)
