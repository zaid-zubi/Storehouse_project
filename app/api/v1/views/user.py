from fastapi import APIRouter, status
from app.api.v1.repositories.user import *
from app.api.v1.dependancies.authorization import *
from app.api.v1.serializers.user import UserIn, Token, ResponseUser
from utils.http_response import http_response
from core.constants.response_messages import ResponseConstants
from core.exceptions import error_messages

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


@router.get("/me", response_model=ResponseUser)
async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db=Depends(CRUD().db_conn)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print("username extracted is ", username)
        if username is None:
            raise error_messages.InvalidUserName
    except JWTError as e:
        raise error_messages.InvalidCredentials from e
    user = get_user_by_name(username=username, db=db)
    if user is None:
        raise error_messages.InvalidUserName
    return jsonable_encoder(user)
