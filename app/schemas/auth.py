from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing_extensions import Annotated
from typing import Optional, Literal
from datetime import date, datetime

class RegisterSchema(BaseModel):
    nickname: Annotated[str, Field(min_length=2, max_length=20)]
    first_name: Annotated[str, Field(min_length=2, max_length=50)]
    last_name: Annotated[str, Field(min_length=2, max_length=50)]
    date_of_birth: Optional[date] = None
    gendered: Optional[Literal["Male", "Female", "Non-Binary", "Unspecified"]] = None
    email: EmailStr
    phone_number: str
    password: str
    confirm_password: str
    role_id: Optional[str] = None


class RegisterOut(BaseModel):
    id: Optional[str] = None
    nickname: str
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    gendered: Optional[str] = None
    email: EmailStr
    phone_number: str
    is_active: bool
    role_id: Optional[str] = None

    @field_validator("id", "role_id", mode="before")
    def convert_objectid(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponseSchema(BaseModel):
    token: str
    user_id: str
    