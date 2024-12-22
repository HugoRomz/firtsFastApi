from typing import Any, List
from fastapi import HTTPException, status
from bson import ObjectId
from pydantic import HttpUrl
from app.db.client import db
from app.schemas.user import UserOut, UserUpdate, UserComplete


async def list_users(skip: int = 0, limit: int = 10):
    users = await db["users"].find().skip(skip).limit(limit).to_list(limit)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron usuarios."
        )
    
    return [UserOut(id=str(u["_id"]), **u) for u in users]


async def get_user_by_id(user_id: str) -> UserOut:
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de Usuario inválido."
        )

    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    return UserOut(id=str(user["_id"]), **user)


async def handle_complete_user(user_id: str, user_data: UserComplete):
# LAS MIMAS VALIDACIONES
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de Usuario inválido."
        )

    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )

    # funcion para preparar los datos como httpurl
    update_data = prepare_update_data(user_data.model_dump(exclude_unset=True))


    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron datos para completar el perfil."
        )

    result = await db["users"].update_one({"_id": ObjectId(user_id)},{"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo completr el usuario."
        )

   
    updated_user = await db["users"].find_one({"_id": ObjectId(user_id)})
    return UserOut(id=str(updated_user["_id"]), **updated_user)

async def deactivate_user(user_id: str):
    # LAS MIMAS VALIDACIONES
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de Usuario inválido."
        )
    
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    
    result = await db["users"].update_one({"_id": ObjectId(user_id)},{"$set": {"is_active": False}})
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo desactivar el usuario."
        )
    
    return {"message": "Usuario desactivado."}


def prepare_update_data(data: dict) -> dict:
    def convert(value: Any) -> Any:
        if isinstance(value, HttpUrl):
            return str(value)
        if isinstance(value, list):
            return [convert(item) for item in value]
        if isinstance(value, dict):
            return {key: convert(val) for key, val in value.items()}
        return value

    return {key: convert(val) for key, val in data.items()}

async def update_user_role(user_id: str, role_id: str):
    # Validar user_id
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de Usuario inválido."
        )
    
    # Validar role_id
    if not ObjectId.is_valid(role_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de Rol inválido."
        )
    
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado."
        )
    
    role = await db["roles"].find_one({"_id": ObjectId(role_id)})
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado."
        )
    
    result = await db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role_id": str(role_id)}}  # Almacenar el ID del rol
    )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo actualizar el rol del usuario."
        )
    
    return {"message": "Rol de usuario actualizado."}