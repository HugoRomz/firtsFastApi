from bson import ObjectId
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date

class UserInDB(BaseModel):
    _id: Optional[str]
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    gendered: Optional[Literal["Male", "Female", "Non-Binary", "Unspecified"]] = None
    email: EmailStr
    phone_number: str
    hashed_password: str
    is_active: bool
    user_token: Optional[str] = None
