# app/services/role.py
from bson import ObjectId
from fastapi import HTTPException, status
from app.db.client import db
from app.schemas.roles import RoleCreate, RoleUpdate, RoleOut


async def list_roles(skip: int = 0, limit: int = 10):
    roles = await db["roles"].find().skip(skip).limit(limit).to_list(limit)
    return [RoleOut(id=str(r["_id"]), **r) for r in roles]


async def get_role_by_id(role_id: str) -> RoleOut:
    if not ObjectId.is_valid(role_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de rol inválido."
        )

    role = await db["roles"].find_one({"_id": ObjectId(role_id)})
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado."
        )
    return RoleOut(id=str(role["_id"]), **role)


async def create_role(role_data: RoleCreate) -> RoleOut:
    role_dict = role_data.model_dump()
    # Verificar si ya existe un rol con ese nombre
    existing_role = await db["roles"].find_one({"name": role_dict["name"]})
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un rol con ese nombre."
        )
    result = await db["roles"].insert_one(role_dict)
    return RoleOut(id=str(result.inserted_id), **role_dict)

