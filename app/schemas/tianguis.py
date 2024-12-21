from bson import ObjectId
from pydantic import BaseModel, EmailStr, HttpUrl, field_validator
from typing import Optional
from datetime import date


class tianguisOut(BaseModel):
    id: Optional[str] = None
    nickname: Optional[str] = None
    first_name: str
    last_name: str
    phone_number: str
    img_perfl: Optional[HttpUrl] = None
    img_portada: Optional[HttpUrl] = None
    


    @field_validator("id", mode="before")
    def convert_objectid(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    