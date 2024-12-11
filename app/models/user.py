from typing_extensions import Annotated
from pydantic import BaseModel, Field, EmailStr, StringConstraints
from typing import Optional, Literal
from datetime import date

class UserInDB(BaseModel):
    _id: Optional[str] = None
    first_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    last_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    date_of_birth: Optional[date] = None
    gendered: Optional[Literal["Male", "Female", "Non-Binary", "Unspecified"]] = None
    email: EmailStr
    phone_number: str
    hashed_password: str
    is_active: bool = True

class UserCreate(BaseModel):
    first_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    last_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    date_of_birth: Optional[date] = None
    gendered: Optional[Literal["Male", "Female", "Non-Binary", "Unspecified"]] = None
    email: EmailStr
    phone_number: str
    password: str
    confirm_password: str

class UserOut(BaseModel):
    id: Optional[str] = None
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    gendered: str
    email: EmailStr
    phone_number: str
    is_active: bool

class UserLogin(BaseModel):
    email: EmailStr
    password: str