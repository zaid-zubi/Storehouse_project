from core.constants import strings
from fastapi import HTTPException, status

# Error Messages


class InvalidCredentials(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=strings.INVALID_CREDENTIALS
        )


class InvalidUserName(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INVALID_USERNAME
        )


class InvalidUserPhoneNumber(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INVALID_PHONE_NUMBER
        )


class InvalidUserEmail(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INVALID_EMAIL
        )


class UserNameNotFound(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_NOT_FOUND
        )


class UserNameExisted(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.USERNAME_EXISTED
        )


class PhoneNumberExisted(Exception):
    def __init__(self):
        raise HTTPException(status_code=strings.PHONE_NUMBER_EXISTED)


class EmailExisted(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.EMAIL_EXISTED
        )


class UnAuthorizedUser(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=strings.UNAUTHORIZED_USER
        )


class ProductNotFound(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.PRODUCT_NOT_FOUND
        )


class InvalidProductName(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INVALID_PRODUCT_NAME
        )


class InvalidProductPrice(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.INVALID_PRODUCT_PRICE,
        )


class CategoryNotFound(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.CATEGORY_NOT_FOUND
        )


class UnactiveUser(Exception):
    def __init__(self):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.UNACTIVE_USER
        )
