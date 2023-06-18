from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.api.v1.dependancies.authorization import *
from app.api.v1.serializers.user import UserIn
from app.api.v1.dependancies.hash import Hasher


def check_if_user_exist(email: str):
    db: Session = CRUD().db_conn()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return True
    else:
        return False


def create(request: UserIn):
    if check_if_user_exist(request.email) == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail= "User already exists"
        )
    else:
        request.password = Hasher().get_password_hash(request.password)
        request.email = request.email.lower()
        new_user = User(**request.dict())
        operation = CRUD().add(new_user)
        return jsonable_encoder(new_user)
