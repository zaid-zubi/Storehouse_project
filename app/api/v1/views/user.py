from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from utils.http_response import http_response
from core.constants.response_messages import ResponseConstants
from app.api.v1.repositories.user import create
from app.api.v1.dependancies.authorization import *
from app.api.v1.serializers.user import UserIn, Token, ResponseUser


router = APIRouter(prefix="", tags=["auth"])


@router.post("/", response_model=ResponseUser)
async def create_user(req: UserIn):
    return http_response(
        message=ResponseConstants.CREATED_MSG,
        status=status.HTTP_201_CREATED,
        data=jsonable_encoder(ResponseUser(**create(req))),
    )


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(CRUD().db_conn)
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise error_messages.InvalidCredentials

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
def get_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print("username extracted is ", email)
        if email is None:
            raise error_messages.InvalidUserName
    except JWTError as e:
        raise error_messages.InvalidCredentials from e
    user = get_user(email=email, db=db)
    if user is None:
        raise error_messages.InvalidUserName
    return jsonable_encoder(user)

@router.get("/me", response_model=ResponseUser)
async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db=Depends(CRUD().db_conn)
):
    return get_token(token,db)

