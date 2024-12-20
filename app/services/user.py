from typing import List
from fastapi import HTTPException, status
from bson import ObjectId
from app.db.client import db
from app.schemas.user import UserOut


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
