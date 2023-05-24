from pydantic import BaseModel, Field
from typing import Any


class BaseResponse(BaseModel):
    """
    the base schema for http_response
    """
    status: str
    message_key: str = None
    message: str
    data: Any = None
    meta: dict = None
    request_id: str = Field(..., alias="request-id")

