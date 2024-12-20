from typing import List, Optional
from app.db.client import db
from datetime import datetime
from app.schemas.roles import RoleOut
from app.schemas.auth import RegisterSchema, LoginSchema, TokenResponseSchema, RegisterOut
from app.utils.hashing import get_password_hash, verify_password
from app.utils.jwt import create_access_token
from app.utils.validation import validate_passwords
from app.utils.roles import verify_role_exists
from bson import ObjectId
from fastapi import HTTPException, status


async def register_user(user: RegisterSchema) -> RegisterOut:

    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe.",
        )

    validate_passwords(user.password, user.confirm_password)
    hashed_password = get_password_hash(user.password)

    # Preparar datos del usuario
    user_data = user.model_dump()
    if user_data.get("date_of_birth"):
        user_data["date_of_birth"] = datetime.combine(user_data["date_of_birth"], datetime.min.time())

    if user_data.get("role_id"):
        role = await verify_role_exists(user_data["role_id"])
        user_data["role_id"] = role["_id"]
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El rol es requerido.",
        )


    now = datetime.now()

    user_data.update({
        "hashed_password": hashed_password,
        "created_at": now,
        "is_active": True
    })
    del user_data["password"], user_data["confirm_password"]

    # Insertar en la base de datos
    result = await db["users"].insert_one(user_data)
    return RegisterOut(id=str(result.inserted_id), **user_data)


async def login_user(user: LoginSchema) -> TokenResponseSchema:
    
    existing_user = await db["users"].find_one({"email": user.email})
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )
    if not verify_password(user.password, existing_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta.",
        )
    
    # Crear token de acceso
    access_token = create_access_token({"sub": existing_user["email"], "id": str(existing_user["_id"])})
    await db["users"].update_one({"_id": existing_user["_id"]}, {"$set": {"user_token": access_token}})
    return TokenResponseSchema(token=access_token, user_id=str(existing_user["_id"]))


async def logout_user(user: RegisterOut):
    await db["users"].update_one({"_id": ObjectId(user.id)}, {"$set": {"user_token": None}})
    return {"message": "Sesión cerrada exitosamente."}


async def get_public_roles() -> List[RoleOut]:
    query = {"type": "public"}
    roles = await db["roles"].find(query).to_list(length=None)
    return [RoleOut(id=str(r["_id"]), **r) for r in roles]