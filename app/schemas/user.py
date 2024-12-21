from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator
from typing_extensions import Annotated
from typing import Dict, List, Optional, Literal
from datetime import date


class ContactInfo(BaseModel):
    correoElectronico: EmailStr
    paginaWeb: Optional[HttpUrl] = None
    telefonos: List[str]
    redes_social: Dict[str, HttpUrl]

class Ubicacion(BaseModel):
    calle: Optional[str] = None
    colonia: Optional[str] = None
    municipio: Optional[str] = None
    estado: str
    cp: Optional[str] = None
    coordenadas: Optional[Dict[str, float]] = None  


class UserCreate(BaseModel):
    nickname: Annotated[str, Field(min_length=2, max_length=20)]
    first_name: Annotated[str, Field(min_length=2, max_length=50)]
    last_name: Annotated[str, Field(min_length=2, max_length=50)]
    date_of_birth: Optional[date] = None
    gendered: Optional[Literal["Male", "Female", "Non-Binary", "Unspecified"]] = None
    email: EmailStr
    phone_number: str
    password: str
    confirm_password: str
    is_active: bool = True
    role_id: Optional[str] = None

class UserComplete(BaseModel):
    img_perfl: Optional[HttpUrl] = None  
    img_portada: Optional[HttpUrl] = None  
    contacto: Optional[ContactInfo] = None
    ubicacion: Optional[Ubicacion] = None

class UserUpdate(BaseModel):
   nickname: Annotated[str, Field(min_length=2, max_length=20)]
   first_name: Annotated[str, Field(min_length=2, max_length=50)]
   last_name: Annotated[str, Field(min_length=2, max_length=50)]
   date_of_birth: Optional[date] = None
   gendered: Optional[Literal["Male", "Female", "Non-Binary", "Unspecified"]] = None
   email: EmailStr
   phone_number: str
   img_perfl: Optional[HttpUrl] = None  # URL de la imagen de perfil
   img_portada: Optional[HttpUrl] = None  # URL de la imagen de portada
   contacto: Optional[ContactInfo] = None
   ubicacion: Optional[Ubicacion] = None


class UserOut(BaseModel):
    id: Optional[str] = None
    nickname: Optional[str] = None
    first_name: str
    last_name: str
    date_of_birth: Optional[date] = None
    gendered: Optional[str] = None
    email: EmailStr
    phone_number: str
    is_active: bool
    role_id: Optional[str] = None
    img_perfl: Optional[HttpUrl] = None
    img_portada: Optional[HttpUrl] = None
    contacto: Optional[ContactInfo] = None
    ubicacion: Optional[Ubicacion] = None


    @field_validator("id", "role_id", mode="before")
    def convert_objectid(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value

    