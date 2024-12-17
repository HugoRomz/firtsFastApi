# app/utils/roles.py
from bson import ObjectId
from fastapi import HTTPException, status
from app.db.client import db

async def verify_role_exists(role_id: str):
    if not ObjectId.is_valid(role_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El role_id proporcionado no es un ObjectId válido."
        )
    role = await db["roles"].find_one({"_id": ObjectId(role_id)})
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El rol especificado no existe."
        )
    return role
