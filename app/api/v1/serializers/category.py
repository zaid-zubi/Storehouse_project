from pydantic import BaseModel, validator


class CategoryIn(BaseModel):
    name: str

    @validator("name")
    def validate_name(cls, v: str):
        v = v.lower()
        if len(v) > 40:
            raise ValueError("Name Large than 40")
        return v
