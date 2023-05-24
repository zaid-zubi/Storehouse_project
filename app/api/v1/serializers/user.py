from pydantic import BaseModel, validator
from typing import Union
import re
from core.exceptions import error_messages
from email_validator import validate_email, EmailNotValidError
from email_validator.exceptions_types import EmailSyntaxError
class UserIn(BaseModel):
    username: str
    email: str
    password: str

    @validator("username")
    def validate_username(cls, v: str):
        try:
            if len(v) < 40:
                return v
        except:
            raise ValueError("Invalid Username")

    @validator("email")
    def validiate_email(cls, v: str):
        try:
            emailinfo = validate_email(v, check_deliverability=False)
            v = emailinfo.normalized
        except EmailSyntaxError as e:
            raise EmailSyntaxError
            
    @validator("password")
    def validate_password(cls, v: str):
        pass


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class ResponseUser(BaseModel):
    username: str
    email: str


class UpdateUserPart(BaseModel):
    username: str
    email: str
    password: str

    @validator("username")
    def validate_username(cls, v: str):
        if len(v) > 40:
            raise ValueError("Username Large Than 40")

        for letter in v:
            if letter == " ":
                raise ValueError("Username has Space")
            if letter.isdigit():
                raise ValueError("Username has Number")

        return v

    @validator("email")
    def validiate_email(cls, v: str):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if re.fullmatch(regex, v):
            return v

        example_email = "alex@example.com"
        raise ValueError(f"Invalid Email, Email must be like {example_email}")

    @validator("password")
    def validate_password(cls, v: str):
        regex = (
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        )
        compile_regex = re.compile(regex)
        search_regex = re.search(compile_regex, v)
        if not search_regex:
            reason = """Invalid Password
        The Length Must Be Large Than 6 and Less Than 20 and,
        It must has at least one number, one Upper case letter
        and one Special symbols """

            raise ValueError(f"{reason}")
        return v
