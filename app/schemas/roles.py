# app/schemas/role.py
from pydantic import BaseModel, Field
from typing import Optional

class RoleBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nombre del rol")

class RoleCreate(RoleBase):
    description: Optional[str] = Field(None, max_length=255, description="Descripción del rol")

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=255)

class RoleOut(RoleBase):
    id: str
    description: Optional[str]
