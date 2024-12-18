from fastapi import Depends, HTTPException, status
from app.utils.jwt import verify_token
from app.db.client import db
from app.schemas.user import UserOut
from bson import ObjectId


async def get_current_user(token: str = Depends(verify_token)) -> UserOut:
    # Decodificar token
    user_data = token.get("sub")
    user_id = token.get("id")

    if not user_data or not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado.",
        )

    # Verificar usuario en la base de datos
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado."
        )

    return UserOut(
        id=str(user["_id"]),
        first_name=user["first_name"],
        last_name=user["last_name"],
        email=user["email"],
        phone_number=user.get("phone_number"),
        date_of_birth=user.get("date_of_birth"),
        gendered=user.get("gendered"),
        is_active=user["is_active"],
        role_id=str(user["role_id"]) if user.get("role_id") else None
    )
