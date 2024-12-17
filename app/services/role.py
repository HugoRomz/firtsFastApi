# app/services/role.py
from bson import ObjectId
from fastapi import HTTPException, status
from app.db.client import db
from app.schemas.roles import RoleCreate, RoleUpdate, RoleOut

async def create_role(role_data: RoleCreate) -> RoleOut:
    role_dict = role_data.dict()
    # Verificar si ya existe un rol con ese nombre
    existing_role = await db["roles"].find_one({"name": role_dict["name"]})
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un rol con ese nombre."
        )
    result = await db["roles"].insert_one(role_dict)
    return RoleOut(id=str(result.inserted_id), **role_dict)

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

async def list_roles(skip: int = 0, limit: int = 10):
    cursor = db["roles"].find().skip(skip).limit(limit)
    roles = await cursor.to_list(length=limit)
    return [RoleOut(id=str(r["_id"]), **r) for r in roles]

async def update_role(role_id: str, role_data: RoleUpdate) -> RoleOut:
    if not ObjectId.is_valid(role_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de rol inválido."
        )

    update_fields = {k: v for k, v in role_data.dict(exclude_unset=True).items() if v is not None}

    if "name" in update_fields:
        # Verificar duplicados al actualizar nombre
        existing_role = await db["roles"].find_one({"name": update_fields["name"], "_id": {"$ne": ObjectId(role_id)}})
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un rol con ese nombre."
            )

    result = await db["roles"].update_one({"_id": ObjectId(role_id)}, {"$set": update_fields})
    if result.modified_count == 0:
        # Podría ser que no se modificó nada porque el rol no existe o no cambió ningún campo
        existing_role = await db["roles"].find_one({"_id": ObjectId(role_id)})
        if not existing_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado."
            )
        # Rol existe pero no hubo cambios
        return RoleOut(id=str(existing_role["_id"]), **existing_role)

    updated_role = await db["roles"].find_one({"_id": ObjectId(role_id)})
    return RoleOut(id=str(updated_role["_id"]), **updated_role)

async def delete_role(role_id: str) -> dict:
    if not ObjectId.is_valid(role_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de rol inválido."
        )

    result = await db["roles"].delete_one({"_id": ObjectId(role_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado."
        )
    return {"message": "Rol eliminado con éxito."}
