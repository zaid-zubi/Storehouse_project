from pydantic import BaseModel, validator
import re
from email_validator import validate_email,EmailNotValidError
class UserIn(BaseModel):
    username: str
    email: str
    password: str

    @validator("username")
    def validate_username(cls, v: str):
        try:
            username = v.lower()
            return username
        except:
            raise ValueError("Username is invalid")
            

    @validator("email")
    def validate_email(cls, v: str):
        try:
            emailinfo = validate_email(v, check_deliverability=False)
            email = emailinfo.normalized
            return email.lower()
        except EmailNotValidError as e:
            raise ValueError(str(e))
            
        
        
            
    @validator("password")
    def validate_password(cls, v: str):
        regex = (
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        )
        compile_regex = re.compile(regex)
        search_regex = re.search(compile_regex, v)
        if not search_regex:
            reason = "Invalid Password"
            raise ValueError(f"{reason}")
        return v
            


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class ResponseUser(BaseModel):
    username: str
    email: str
